"""RF10: offline converter for FIRST-PARTY Espressif CSV CSI packet exports.

No radio capture, MAC export, device fingerprinting, or measured-signal claims.
Requires authorized lab inventory and *independently assigned* trial labels.
This is an interface to rf_pilot_evaluator (not a claimed original WiTraffic
replication). Pass output to the existing RF05 sessionÃplacement evaluator.
"""
from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import statistics
from pathlib import Path

# Whitelisted wire-compatible subset of rf_pilot_evaluator.REQUIRED.
# Keeping this standalone lets the importer undergo unit tests without
# installing a radio driver or cloning the full T2 environment.
LABELS = ('no_demand', 'free', 'pocket', 'downstream', 'both')
REQUIRED = ('trial_id','session_id','placement_id','trial_origin','label',
            'ground_truth_source','quality','rssi_1_dbm','rssi_2_dbm',
            'csi_1_amp_dispersion','csi_2_amp_dispersion')


def validate_bridge_rows(rows: list[dict]):
    if not rows or len({r['trial_id'] for r in rows}) != len(rows):
        raise ValueError('empty or duplicate output trials')
    origins={r['trial_origin'] for r in rows}
    if len(origins)!=1:
        raise ValueError('mixed trial provenance')
    for r in rows:
        if r['label'] not in LABELS or r['quality'] not in ('ok','missing'):
            raise ValueError('invalid trial output')
        if r['ground_truth_source'] != 'manual_model_state':
            raise ValueError('non-independent label')
        if any(k not in r for k in REQUIRED):
            raise ValueError('wire schema differs from RF pilot evaluator')
        for k in REQUIRED[7:]:
            if r[k] not in ('',None) and not math.isfinite(float(r[k])):
                raise ValueError('nonfinite trial output feature')

META = ('trial_id', 'session_id', 'placement_id', 'label', 'ground_truth_source',
        'trial_origin')
LINKS = ('1', '2')
BASE_COLUMNS = ('type', 'rssi', 'local_timestamp', 'len', 'first_word', 'data')
TRIAL_COLUMNS = ('trial_id','session_id','placement_id','label','ground_truth_source',
                 'trial_origin','link_id','start_us','stop_us')
FEATURE_KEYS = ('rssi_1_dbm','rssi_2_dbm','csi_1_amp_dispersion',
                'csi_2_amp_dispersion')


def parse_iq(raw: str, announced_len: str, invalid_word: str, *,
             invalid_policy: str='reject') -> tuple[float, ...]:
    """Reject ambiguous CSI framing instead of silently shifting I/Q bins."""
    try:
        length = int(announced_len)
        invalid = int(invalid_word)
    except (ValueError, TypeError) as exc:
        raise ValueError('bad CSI length/first_word') from exc
    if invalid not in (0, 1) or length < 8 or length % 2 or length > 8192:
        raise ValueError('unsupported CSI frame descriptor')
    if invalid_policy not in ('reject','esp32_drop_first_four'):
        raise ValueError('unsupported invalid-word policy')
    if invalid and invalid_policy=='reject':
        raise ValueError('first_word_invalid requires chip-specific handling')
    try:
        data = ast.literal_eval(raw)
    except (ValueError, SyntaxError, TypeError, MemoryError) as exc:
        raise ValueError('CSI data not a numeric list') from exc
    if not isinstance(data, list) or len(data) != length:
        raise ValueError('CSI list length mismatch')
    if any(type(v) is not int or v < -128 or v > 127 for v in data):
        raise ValueError('not signed 8-bit I/Q data (chip-specific format unsupported)')
    if invalid:
        # ESP-IDF WiFi driver documented first four invalid bytes on ESP32.
        # This is a specific, explicitly selected legacy device profile;
        # do not use for C5/C61 packed/compensated format without audit.
        if length < 12:
            raise ValueError('not enough CSI bytes after invalid four-byte prefix')
        data=data[4:]
    return tuple(math.hypot(data[i], data[i+1]) for i in range(0,len(data),2))


def _safe_int(value: str, field: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'{field}: invalid integer') from exc
    return result


def load_owned_csv(path: str | Path, *, lab_authorized: bool,
                   invalid_policy: str='reject') -> list[dict]:
    """Only offline exports from operator-owned experimental transmitters.

    MAC/ID fields are never returned, including on malformed-record errors.
    The caller must independently verify hardware/network permission and
    source provenance; a command-line flag is NOT proof of permission.
    """
    if not lab_authorized:
        raise PermissionError('first-party authorized lab CSV only')
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in BASE_COLUMNS):
            raise ValueError('missing official Espressif CSI columns')
        packets=[]
        for row in reader:
            if row['type'] != 'CSI_DATA':
                continue
            timestamp = _safe_int(row['local_timestamp'], 'local_timestamp')
            rssi = _safe_int(row['rssi'], 'rssi')
            if timestamp < 0 or not -128 <= rssi <= 20:
                raise ValueError('bad timestamp or RSSI')
            amp = parse_iq(row['data'], row['len'], row['first_word'],
                           invalid_policy=invalid_policy)
            packets.append({'timestamp_us':timestamp, 'rssi':rssi,
                            'mean_amplitude':statistics.fmean(amp),
                            'subcarrier_dispersion':statistics.pstdev(amp)})
    if not packets:
        raise ValueError('no CSI frames')
    if any(b['timestamp_us'] <= a['timestamp_us'] for a,b in zip(packets,packets[1:])):
        raise ValueError('nonmonotone/duplicate timestamps; split clock resets')
    return packets


def aggregate_trials(manifest: list[dict], per_link: dict[str, list[dict]], *,
                     min_packets: int = 2) -> list[dict]:
    """Map independently labeled reset windows to the existing RF05 schema.

    Do not fill absent links with zeros: quality='missing' and empty feature
    columns enforce evaluator abstention and retain intention-to-test counts.
    """
    if min_packets < 2:
        raise ValueError('min_packets must be >=2')
    if not manifest:
        raise ValueError('no trial manifest')
    seen_window=set()
    occupied_windows={k:[] for k in LINKS}
    grouped={}
    origins=set()
    for row in manifest:
        if any(k not in row or not str(row[k]).strip() for k in TRIAL_COLUMNS):
            raise ValueError('incomplete trial manifest')
        origin=row['trial_origin']
        if origin not in ('synthetic_test_fixture','measured_authorized_lab'):
            raise ValueError('invalid origin')
        origins.add(origin)
        if row['label'] not in LABELS:
            raise ValueError('unknown ground truth label')
        if row['ground_truth_source']!='manual_model_state':
            raise ValueError('labels must be manual and independent of RF')
        lid=row['link_id']
        if lid not in LINKS or lid not in per_link:
            raise ValueError('unknown or unavailable receiver link')
        start=_safe_int(row['start_us'],'start_us')
        stop=_safe_int(row['stop_us'],'stop_us')
        if start<0 or start>=stop:
            raise ValueError('bad trial window')
        tid=row['trial_id']
        key=(tid,lid)
        if key in seen_window:
            raise ValueError('duplicate trial/window/link')
        for previous_start,previous_stop,previous_id in occupied_windows[lid]:
            if start < previous_stop and previous_start < stop and previous_id != tid:
                raise ValueError('overlapping reset trials on one link')
        occupied_windows[lid].append((start,stop,tid))
        seen_window.add(key)
        metadata={k:row[k] for k in META}
        if tid not in grouped:
            grouped[tid]={'meta':metadata, 'links':{}}
        elif grouped[tid]['meta']!=metadata:
            raise ValueError('inconsistent trial truth across receiver links')
        observations=[p for p in per_link[lid]
                      if start <= p['timestamp_us'] < stop]
        grouped[tid]['links'][lid]=observations
    if len(origins)!=1:
        raise ValueError('mixed provenance in one analysis')
    result=[]
    for tid,info in grouped.items():
        row={**info['meta'], 'quality':'ok'}
        for key in FEATURE_KEYS:
            row[key]=''
        for lid in LINKS:
            samples=info['links'].get(lid,[])
            if len(samples)<min_packets:
                row['quality']='missing'
                continue
            row[f'rssi_{lid}_dbm']=round(statistics.fmean(p['rssi'] for p in samples),8)
            # Per-trial temporal movement of subcarrier amplitude; cannot by
            # itself prove stationary vehicle position or RF causal attribution.
            row[f'csi_{lid}_amp_dispersion']=round(
                statistics.pstdev(p['mean_amplitude'] for p in samples),8)
        result.append(row)
    validate_bridge_rows(result)
    return result


def read_manifest(path: str | Path) -> list[dict]:
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def export_trials(rows: list[dict], path: str | Path):
    """Whitelisted schema intentionally excludes any device identifier."""
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=REQUIRED,extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    parser=argparse.ArgumentParser(description='OFFLINE owned ESP-CSI CSV -> anonymized RF trial rows')
    parser.add_argument('--link-1', required=True)
    parser.add_argument('--link-2', required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--out',required=True)
    parser.add_argument('--invalid-word-policy', choices=('reject','esp32_drop_first_four'),
                        default='reject',help='select only after confirming exact ESP32 format')
    parser.add_argument('--authorized-lab',action='store_true',
                        help='operator declaration; not a substitute for school approval')
    args=parser.parse_args(argv)
    a=load_owned_csv(args.link_1,lab_authorized=args.authorized_lab,
                     invalid_policy=args.invalid_word_policy)
    b=load_owned_csv(args.link_2,lab_authorized=args.authorized_lab,
                     invalid_policy=args.invalid_word_policy)
    rows=aggregate_trials(read_manifest(args.manifest),{'1':a,'2':b})
    export_trials(rows,args.out)
    print(json.dumps({'status':'OFFLINE_TRIAL_BRIDGE_NOT_SENSOR_VALIDATION',
          'trials':len(rows),'quality_ok':sum(r['quality']=='ok' for r in rows),
          'quality_missing':sum(r['quality']=='missing' for r in rows),
          'raw_device_identifiers_exported':False},ensure_ascii=False))


if __name__ == '__main__':
    main()
