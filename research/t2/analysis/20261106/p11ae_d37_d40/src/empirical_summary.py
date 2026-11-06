"""Descriptive summary at the episode (not frame) level."""
import json
from pathlib import Path
from statistics import mean, median


def load_manifest(path: str|Path)->list[dict]:
    data=json.loads(Path(path).read_text())
    out=data['records']
    if len({x['github_blob_sha1'] for x in out})!=len(out):
        raise ValueError('duplicate original sample')
    for x in out:
        if x['frames']<=0 or not 0<=x['frames_below_0p5_mps']<=x['frames']:
            raise ValueError('invalid frame counting')
        if x['red_or_red_arrow_frames']+x['green_or_green_arrow_frames']>x['frames']:
            raise ValueError('red + green frames > total')
    return out


def describe(records: list[dict]) -> list[dict]:
    result=[]
    for c in sorted(set(x['category'] for x in records)):
        group=[x for x in records if x['category']==c]
        result.append({'group':c,'episodes':len(group),'frames':sum(x['frames'] for x in group),
          'stopped_frames':sum(x['frames_below_0p5_mps'] for x in group),
          'stop_fraction_descriptive':sum(x['frames_below_0p5_mps'] for x in group)/sum(x['frames'] for x in group),
          'mean_episode_speed_mps':mean(x['mean_speed_mps'] for x in group),
          'median_episode_speed_mps':median(x['mean_speed_mps'] for x in group),
          'red_frames':sum(x['red_or_red_arrow_frames'] for x in group),
          'green_frames':sum(x['green_or_green_arrow_frames'] for x in group),
          'unclear_phase_episodes':sum(any(s in (0,-1) for s in x['observed_state_codes']) for x in group)})
    return result
