// DLR-UT P33 independent time-fidelity gate. Academic, observation-only: NO signal control.
// Signal-head IDs and trajectory-object IDs are disjoint namespaces; do not join by ID.
package main

import (
	"crypto/sha256"
	"encoding/csv"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

const signalSHA = "95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c"
const trajectorySHA = "6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50"
const timeLayout = "2006-01-02 15:04:05.999999999-07:00"
const signalGap = 1500 * time.Millisecond
const trajectoryGap = 100 * time.Millisecond

var signalsHeader = []string{"timestamp", "id", "state"}
var trajectoriesHeader = []string{"timestamp", "id", "center_easting", "center_northing", "velocity_easting", "velocity_northing", "velocity_magnitude", "acceleration_easting", "acceleration_northing", "acceleration_magnitude", "yaw", "dimension_length", "dimension_width", "dimension_height", "classifications_pedestrian", "classifications_bicycle", "classifications_motorbike", "classifications_car", "classifications_van", "classifications_truck", "interpolated"}
var classNames = []string{"pedestrian", "bicycle", "motorbike", "car", "van", "truck"}

func readTimestamp(s string) (time.Time, error) {
	t, err := time.Parse(timeLayout, s)
	if err != nil || s == "" {
		return time.Time{}, fmt.Errorf("bad offset-aware timestamp %q: %v", s, err)
	}
	return t.UTC(), nil
}
func positiveID(s string) (int64, error) {
	x, e := strconv.ParseInt(s, 10, 64)
	if e != nil || x < 1 {
		return 0, fmt.Errorf("bad positive ID %q", s)
	}
	return x, nil
}
func number(s string) (float64, error) {
	v, e := strconv.ParseFloat(s, 64)
	if e != nil || math.IsNaN(v) || math.IsInf(v, 0) {
		return 0, fmt.Errorf("bad finite number %q", s)
	}
	return v, nil
}

func csvRows(path string, schema []string, use func([]string) error) error {
	f, e := os.Open(path)
	if e != nil {
		return e
	}
	defer f.Close()
	r := csv.NewReader(f)
	r.ReuseRecord = true
	r.FieldsPerRecord = len(schema)
	header, e := r.Read()
	if e != nil {
		return fmt.Errorf("header: %w", e)
	}
	if strings.Join(header, "\x00") != strings.Join(schema, "\x00") {
		return fmt.Errorf("CSV schema mismatch: %v", header)
	}
	for line := 2; ; line++ {
		row, e := r.Read()
		if errors.Is(e, io.EOF) {
			break
		}
		if e != nil {
			return fmt.Errorf("row %d: %w", line, e)
		}
		if e := use(row); e != nil {
			return fmt.Errorf("row %d: %w", line, e)
		}
	}
	return nil
}
func fileSHA(path string) (string, error) {
	f, e := os.Open(path)
	if e != nil {
		return "", e
	}
	defer f.Close()
	h := sha256.New()
	if _, e = io.Copy(h, f); e != nil {
		return "", e
	}
	return hex.EncodeToString(h.Sum(nil)), nil
}
func boundsUpdate(first, last *time.Time, t time.Time) {
	if first.IsZero() || t.Before(*first) {
		*first = t
	}
	if last.IsZero() || t.After(*last) {
		*last = t
	}
}

type SignalID struct {
	ID                 int64  `json:"id"`
	Samples            int    `json:"samples"`
	Transitions        int    `json:"observed_state_changes"`
	GapsOver1500ms     int    `json:"sample_gaps_gt_1500ms"`
	MaxGapMs           int64  `json:"max_gap_ms"`
	GreenRuns          int    `json:"sampled_green_runs"`
	MaxGreenRunSamples int    `json:"max_green_run_samples"`
	First              string `json:"first_utc"`
	Last               string `json:"last_utc"`
}
type SynchronizedGap struct {
	LastObservedUTC       string  `json:"last_observed_utc"`
	NextObservedUTC       string  `json:"next_observed_utc"`
	GapMs                 int64   `json:"gap_ms"`
	AffectedSignalHeads   int     `json:"affected_signal_heads"`
	ChangedStateSignalIDs []int64 `json:"changed_state_signal_ids_across_gap"`
}

type SignalSummary struct {
	Rows                  int               `json:"rows"`
	IDs                   int               `json:"ids"`
	SnapshotTimes         int               `json:"distinct_sample_timestamps"`
	MinHeadsPerSnapshot   int               `json:"min_heads_per_timestamp"`
	MaxHeadsPerSnapshot   int               `json:"max_heads_per_timestamp"`
	SynchronizedGaps      []SynchronizedGap `json:"shared_timestamp_gaps"`
	CodeCounts            map[string]int    `json:"code_counts"`
	ObservedTransitions   int               `json:"observed_state_changes"`
	GapsOver1500ms        int               `json:"sample_gaps_gt_1500ms"`
	MaxGapMs              int64             `json:"max_gap_ms"`
	GreenRuns             int               `json:"sampled_green_runs"`
	GreenRunLengthSamples []int             `json:"green_run_length_samples_sorted"`
	FirstUTC              string            `json:"first_utc"`
	LastUTC               string            `json:"last_utc"`
	PerID                 []SignalID        `json:"per_id"`
}
type signalState struct {
	report              SignalID
	last                time.Time
	previous            int
	run                 int
	first, lastObserved time.Time
}

func (s *signalState) finalRun(lens *[]int) {
	if s.run > 0 {
		*lens = append(*lens, s.run)
		s.report.GreenRuns++
		if s.run > s.report.MaxGreenRunSamples {
			s.report.MaxGreenRunSamples = s.run
		}
		s.run = 0
	}
}
func parseSignals(path string) (SignalSummary, time.Time, time.Time, error) {
	out := SignalSummary{CodeCounts: map[string]int{}}
	gapGroups := map[string]*SynchronizedGap{}
	snapshotCounts := map[string]int{}
	ids := map[int64]*signalState{}
	var low, high time.Time
	err := csvRows(path, signalsHeader, func(row []string) error {
		t, e := readTimestamp(row[0])
		if e != nil {
			return e
		}
		id, e := positiveID(row[1])
		if e != nil {
			return e
		}
		state, e := strconv.Atoi(row[2])
		if e != nil || state < 0 || state > 9 {
			return fmt.Errorf("unknown signal state %q", row[2])
		}
		s := ids[id]
		if s == nil {
			s = &signalState{report: SignalID{ID: id}, previous: state}
			ids[id] = s
		}
		if !s.last.IsZero() {
			dt := t.Sub(s.last)
			if dt <= 0 {
				return fmt.Errorf("duplicate/nonmonotone signal id=%d time=%s", id, t)
			}
			if dt > signalGap {
				start, end := s.last.Format(time.RFC3339Nano), t.Format(time.RFC3339Nano)
				key := start + "/" + end
				g := gapGroups[key]
				if g == nil {
					g = &SynchronizedGap{LastObservedUTC: start, NextObservedUTC: end, GapMs: dt.Milliseconds()}
					gapGroups[key] = g
				}
				g.AffectedSignalHeads++
				if state != s.previous {
					g.ChangedStateSignalIDs = append(g.ChangedStateSignalIDs, id)
				}
				s.report.GapsOver1500ms++
				if dt.Milliseconds() > s.report.MaxGapMs {
					s.report.MaxGapMs = dt.Milliseconds()
				}
				s.finalRun(&out.GreenRunLengthSamples)
			}
			if state != s.previous {
				s.report.Transitions++
			}
		}
		isGreen := state == 5 || state == 6
		if isGreen {
			if s.run == 0 {
				s.run = 1
			} else {
				s.run++
			}
		} else {
			s.finalRun(&out.GreenRunLengthSamples)
		}
		if s.first.IsZero() {
			s.first = t
		}
		s.last = t
		s.previous = state
		s.report.Samples++
		out.Rows++
		snapshotCounts[t.Format(time.RFC3339Nano)]++
		out.CodeCounts[row[2]]++
		boundsUpdate(&low, &high, t)
		return nil
	})
	if err != nil {
		return out, low, high, err
	}
	for _, s := range ids {
		s.finalRun(&out.GreenRunLengthSamples)
		s.report.First = s.first.Format(time.RFC3339Nano)
		s.report.Last = s.last.Format(time.RFC3339Nano)
		out.PerID = append(out.PerID, s.report)
		out.ObservedTransitions += s.report.Transitions
		out.GapsOver1500ms += s.report.GapsOver1500ms
		out.GreenRuns += s.report.GreenRuns
		if s.report.MaxGapMs > out.MaxGapMs {
			out.MaxGapMs = s.report.MaxGapMs
		}
	}
	sort.Slice(out.PerID, func(i, j int) bool { return out.PerID[i].ID < out.PerID[j].ID })
	for _, g := range gapGroups {
		sort.Slice(g.ChangedStateSignalIDs, func(i, j int) bool { return g.ChangedStateSignalIDs[i] < g.ChangedStateSignalIDs[j] })
		out.SynchronizedGaps = append(out.SynchronizedGaps, *g)
	}
	sort.Slice(out.SynchronizedGaps, func(i, j int) bool {
		return out.SynchronizedGaps[i].LastObservedUTC < out.SynchronizedGaps[j].LastObservedUTC
	})
	out.SnapshotTimes = len(snapshotCounts)
	for _, n := range snapshotCounts {
		if out.MinHeadsPerSnapshot == 0 || n < out.MinHeadsPerSnapshot {
			out.MinHeadsPerSnapshot = n
		}
		if n > out.MaxHeadsPerSnapshot {
			out.MaxHeadsPerSnapshot = n
		}
	}
	sort.Ints(out.GreenRunLengthSamples)
	out.IDs = len(ids)
	if !low.IsZero() {
		out.FirstUTC = low.Format(time.RFC3339Nano)
		out.LastUTC = high.Format(time.RFC3339Nano)
	}
	return out, low, high, nil
}

type TrajectoryID struct {
	ID                      int64  `json:"id"`
	Samples                 int    `json:"samples"`
	GapsOver100ms           int    `json:"gaps_gt_100ms"`
	MaxGapMs                int64  `json:"max_gap_ms"`
	First                   string `json:"first_utc"`
	Last                    string `json:"last_utc"`
	ObservedTopClassChanges int    `json:"observed_top_class_changes"`
}
type TrajectorySummary struct {
	Rows                       int            `json:"rows"`
	IDs                        int            `json:"ids"`
	InterpolatedSamples        int            `json:"interpolated_samples"`
	SamplesOutsideSignalBounds int            `json:"samples_outside_signal_global_bounds"`
	GapsOver100ms              int            `json:"gaps_gt_100ms"`
	MedianInterSampleMs        float64        `json:"median_per_id_inter_sample_ms"`
	MaxGapMs                   int64          `json:"max_gap_ms"`
	SpeedMagnitudeDiffOver01   int            `json:"speed_component_disagreements_gt_0_1_mps"`
	SpeedMagnitudeDiffOver05   int            `json:"speed_component_disagreements_gt_0_5_mps"`
	MaxSpeedMagnitudeDiff      float64        `json:"max_speed_magnitude_difference_mps"`
	TopClassChanges            int            `json:"observed_top_class_changes"`
	FirstUTC                   string         `json:"first_utc"`
	LastUTC                    string         `json:"last_utc"`
	PerID                      []TrajectoryID `json:"per_id"`
}
type trajState struct {
	report   TrajectoryID
	last     time.Time
	first    time.Time
	cls      string
	hasClass bool
}

func topClass(row []string) (string, error) {
	best := -1.0
	label := "unassigned"
	for k := 0; k < 6; k++ {
		v, e := number(row[14+k])
		if e != nil {
			return "", e
		}
		if v < 0 || v > 1 {
			return "", fmt.Errorf("invalid class confidence %v", v)
		}
		if v > best {
			best = v
			label = classNames[k]
		}
	}
	if best == 0 {
		label = "unassigned"
	}
	return label, nil
}
func medianMillis(x []int64) float64 {
	if len(x) == 0 {
		return 0
	}
	sort.Slice(x, func(i, j int) bool { return x[i] < x[j] })
	a := x[(len(x)-1)/2]
	b := x[len(x)/2]
	return float64(a+b) / 2
}
func parseTrajectories(path string, signalFirst, signalLast time.Time) (TrajectorySummary, time.Time, time.Time, error) {
	out := TrajectorySummary{}
	ids := map[int64]*trajState{}
	var low, high time.Time
	intervals := []int64{}
	err := csvRows(path, trajectoriesHeader, func(row []string) error {
		t, e := readTimestamp(row[0])
		if e != nil {
			return e
		}
		id, e := positiveID(row[1])
		if e != nil {
			return e
		}
		// Validate every numeric trajectory coordinate/kinematics/size and class field.
		nums := [18]float64{}
		for i := 2; i < 20; i++ {
			v, e := number(row[i])
			if e != nil {
				return fmt.Errorf("column %d: %w", i, e)
			}
			nums[i-2] = v
		}
		cls, e := topClass(row)
		if e != nil {
			return e
		}
		interpolated, e := strconv.ParseBool(strings.ToLower(row[20]))
		if e != nil {
			return fmt.Errorf("invalid interpolated field %q", row[20])
		}
		s := ids[id]
		if s == nil {
			s = &trajState{report: TrajectoryID{ID: id}}
			ids[id] = s
		}
		if !s.last.IsZero() {
			dt := t.Sub(s.last)
			if dt <= 0 {
				return fmt.Errorf("duplicate/nonmonotone vehicle id=%d time=%s", id, t)
			}
			dms := dt.Milliseconds()
			intervals = append(intervals, dms)
			if dt > trajectoryGap {
				s.report.GapsOver100ms++
			}
			if dms > s.report.MaxGapMs {
				s.report.MaxGapMs = dms
			}
			if s.hasClass && s.cls != cls {
				s.report.ObservedTopClassChanges++
			}
		}
		if s.first.IsZero() {
			s.first = t
		}
		s.last = t
		s.cls = cls
		s.hasClass = true
		s.report.Samples++
		out.Rows++
		if interpolated {
			out.InterpolatedSamples++
		}
		if !signalFirst.IsZero() && (t.Before(signalFirst) || t.After(signalLast)) {
			out.SamplesOutsideSignalBounds++
		}
		v := math.Hypot(nums[2], nums[3])
		delta := math.Abs(v - nums[4])
		if delta > 0.1 {
			out.SpeedMagnitudeDiffOver01++
		}
		if delta > 0.5 {
			out.SpeedMagnitudeDiffOver05++
		}
		if delta > out.MaxSpeedMagnitudeDiff {
			out.MaxSpeedMagnitudeDiff = delta
		}
		boundsUpdate(&low, &high, t)
		return nil
	})
	if err != nil {
		return out, low, high, err
	}
	for _, s := range ids {
		s.report.First = s.first.Format(time.RFC3339Nano)
		s.report.Last = s.last.Format(time.RFC3339Nano)
		out.PerID = append(out.PerID, s.report)
		out.GapsOver100ms += s.report.GapsOver100ms
		out.TopClassChanges += s.report.ObservedTopClassChanges
		if s.report.MaxGapMs > out.MaxGapMs {
			out.MaxGapMs = s.report.MaxGapMs
		}
	}
	sort.Slice(out.PerID, func(i, j int) bool { return out.PerID[i].ID < out.PerID[j].ID })
	out.IDs = len(ids)
	out.MedianInterSampleMs = medianMillis(intervals)
	if !low.IsZero() {
		out.FirstUTC = low.Format(time.RFC3339Nano)
		out.LastUTC = high.Format(time.RFC3339Nano)
	}
	return out, low, high, nil
}

type Report struct {
	Protocol               string            `json:"protocol"`
	Status                 string            `json:"status"`
	Sha256                 map[string]string `json:"sha256"`
	Signals                SignalSummary     `json:"signals"`
	Trajectories           TrajectorySummary `json:"trajectories"`
	GlobalOverlapMs        int64             `json:"global_signal_trajectory_time_overlap_ms"`
	OfficialP24CountsEqual bool              `json:"official_p24_count_regression_pass"`
	Limitation             []string          `json:"limitations"`
}

func analyse(signalPath, trajectoryPath string) (Report, error) {
	r := Report{Protocol: "P33_GO_DLR_TEMPORAL_FIDELITY", Status: "REAL_FIELD_CSV_QC_NOT_CONTROL_OR_CAUSAL_INFERENCE", Sha256: map[string]string{}, Limitation: []string{
		"Signal ID != vehicle ID: no lane/stopline join certified",
		"Sample-to-sample state changes and green runs do not determine exact actuation or legal clearance",
		"Recorded trajectory samples are not independent traffic days or complete vehicle census",
		"Interpolation and classification changes are measurement diagnostics, not ground-truth errors",
	}}
	for name, path := range map[string]struct{ path, want string }{"signals": {signalPath, signalSHA}, "trajectories": {trajectoryPath, trajectorySHA}} {
		got, e := fileSHA(path.path)
		if e != nil {
			return r, e
		}
		r.Sha256[name] = got
		if got != path.want {
			return r, fmt.Errorf("%s raw source sha256 mismatch expected %s got %s", name, path.want, got)
		}
	}
	sig, lo, hi, e := parseSignals(signalPath)
	if e != nil {
		return r, e
	}
	r.Signals = sig
	traj, tlo, thi, e := parseTrajectories(trajectoryPath, lo, hi)
	if e != nil {
		return r, e
	}
	r.Trajectories = traj
	if lo.IsZero() || tlo.IsZero() {
		return r, errors.New("empty observation stream")
	}
	left, right := lo, hi
	if tlo.After(left) {
		left = tlo
	}
	if thi.Before(right) {
		right = thi
	}
	if !right.After(left) {
		return r, errors.New("no signal-trajectory global temporal overlap")
	}
	r.GlobalOverlapMs = right.Sub(left).Milliseconds()
	r.OfficialP24CountsEqual = sig.Rows == 26970 && sig.IDs == 30 && sig.ObservedTransitions == 869 && traj.Rows == 8624 && traj.IDs == 37
	if !r.OfficialP24CountsEqual {
		return r, fmt.Errorf("frozen P24/P20 raw count mismatch signals=%d IDs=%d changes=%d trajectories=%d IDs=%d", sig.Rows, sig.IDs, sig.ObservedTransitions, traj.Rows, traj.IDs)
	}
	return r, nil
}
func main() {
	signals := flag.String("signals", "", "frozen DLR signals CSV path")
	trajectories := flag.String("trajectories", "", "frozen DLR trajectories CSV path")
	out := flag.String("out", "", "output JSON path (must not overwrite an existing file)")
	flag.Parse()
	if *signals == "" || *trajectories == "" || *out == "" {
		fmt.Fprintln(os.Stderr, "require --signals --trajectories --out")
		os.Exit(2)
	}
	r, e := analyse(*signals, *trajectories)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
	bytes, e := json.MarshalIndent(r, "", "  ")
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
	bytes = append(bytes, '\n')
	f, e := os.OpenFile(*out, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0644)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
	defer f.Close()
	if _, e = f.Write(bytes); e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
}
