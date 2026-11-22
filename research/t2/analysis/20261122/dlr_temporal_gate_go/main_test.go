package main

import (
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
	"time"
)

func fixture(t *testing.T, header []string, rows ...[]string) string {
	t.Helper()
	var b strings.Builder
	b.WriteString(strings.Join(header, ",") + "\n")
	for _, r := range rows {
		b.WriteString(strings.Join(r, ",") + "\n")
	}
	path := filepath.Join(t.TempDir(), "data.csv")
	if e := os.WriteFile(path, []byte(b.String()), 0600); e != nil {
		t.Fatal(e)
	}
	return path
}
func ts(s string) time.Time {
	t, e := readTimestamp(s)
	if e != nil {
		panic(e)
	}
	return t
}
func trajectoryRow(timestamp, id, speed, vr, interpolated, classIdx string) []string {
	row := make([]string, len(trajectoriesHeader))
	row[0] = timestamp
	row[1] = id
	for i := 2; i < 20; i++ {
		row[i] = "0"
	}
	row[4] = "3"
	row[5] = "4"
	row[6] = speed
	row[14] = "1"
	if classIdx == "car" {
		row[14] = "0"
		row[17] = "1"
	}
	row[20] = interpolated
	_ = vr
	return row
}
func TestTimestampOffsetRequired(t *testing.T) {
	for _, s := range []string{"2023-09-24 23:31:44.010000+00:00", "2023-09-24 23:31:44.01+00:00"} {
		if _, e := readTimestamp(s); e != nil {
			t.Fatal(e)
		}
	}
	if _, e := readTimestamp("2023-09-24 23:31:44.010000"); e == nil {
		t.Fatal("accepted timezone-free date")
	}
}
func TestSharedGapDoesNotInventGreenContinuity(t *testing.T) {
	f := fixture(t, signalsHeader,
		[]string{"2023-09-24 23:30:00+00:00", "1", "5"},
		[]string{"2023-09-24 23:30:01+00:00", "1", "5"},
		[]string{"2023-09-24 23:30:03.004+00:00", "1", "5"},
	)
	r, _, _, e := parseSignals(f)
	if e != nil {
		t.Fatal(e)
	}
	if r.ObservedTransitions != 0 || r.GreenRuns != 2 || !reflect.DeepEqual(r.GreenRunLengthSamples, []int{1, 2}) || r.GapsOver1500ms != 1 {
		t.Fatalf("gap did not split sampled green runs: %+v", r)
	}
	if len(r.SynchronizedGaps) != 1 || r.SynchronizedGaps[0].GapMs != 2004 || r.SynchronizedGaps[0].AffectedSignalHeads != 1 {
		t.Fatalf("bad gap group %+v", r.SynchronizedGaps)
	}
}
func TestSignalSchemaFailsClosed(t *testing.T) {
	f := fixture(t, []string{"timestamp", "state", "id"}, []string{"2023-09-24 23:30:00+00:00", "5", "1"})
	if _, _, _, e := parseSignals(f); e == nil {
		t.Fatal("wrong header accepted")
	}
}
func TestSignalDuplicateTimestampRejected(t *testing.T) {
	row := []string{"2023-09-24 23:30:00+00:00", "1", "5"}
	f := fixture(t, signalsHeader, row, row)
	if _, _, _, e := parseSignals(f); e == nil {
		t.Fatal("duplicate timestamp accepted")
	}
}
func TestSignalReverseTimestampRejected(t *testing.T) {
	f := fixture(t, signalsHeader, []string{"2023-09-24 23:30:01+00:00", "1", "5"}, []string{"2023-09-24 23:30:00+00:00", "1", "3"})
	if _, _, _, e := parseSignals(f); e == nil {
		t.Fatal("reverse signal accepted")
	}
}
func TestUnknownSignalStateRejected(t *testing.T) {
	f := fixture(t, signalsHeader, []string{"2023-09-24 23:30:00+00:00", "1", "99"})
	if _, _, _, e := parseSignals(f); e == nil {
		t.Fatal("unknown code accepted")
	}
}
func TestTwoHeadsSnapshotAlignment(t *testing.T) {
	f := fixture(t, signalsHeader,
		[]string{"2023-09-24 23:30:00+00:00", "1", "3"}, []string{"2023-09-24 23:30:00+00:00", "2", "5"},
		[]string{"2023-09-24 23:30:01+00:00", "1", "5"}, []string{"2023-09-24 23:30:01+00:00", "2", "5"},
	)
	r, _, _, e := parseSignals(f)
	if e != nil {
		t.Fatal(e)
	}
	if r.SnapshotTimes != 2 || r.MinHeadsPerSnapshot != 2 || r.MaxHeadsPerSnapshot != 2 || r.ObservedTransitions != 1 {
		t.Fatalf("bad alignment: %+v", r)
	}
}
func TestTrajectorySampleSpeedAndClassDrift(t *testing.T) {
	f := fixture(t, trajectoriesHeader,
		trajectoryRow("2023-09-24 23:30:00+00:00", "100", "5", "", "False", "bicycle"),
		trajectoryRow("2023-09-24 23:30:00.050+00:00", "100", "5", "", "True", "car"),
	)
	r, _, _, e := parseTrajectories(f, ts("2023-09-24 23:29:59+00:00"), ts("2023-09-24 23:31:00+00:00"))
	if e != nil {
		t.Fatal(e)
	}
	if r.Rows != 2 || r.IDs != 1 || r.InterpolatedSamples != 1 || r.GapsOver100ms != 0 || r.MedianInterSampleMs != 50 || r.TopClassChanges != 1 || r.SpeedMagnitudeDiffOver01 != 0 {
		t.Fatalf("unexpected trajectory result %+v", r)
	}
}
func TestTrajectoryDuplicateRejected(t *testing.T) {
	row := trajectoryRow("2023-09-24 23:30:00+00:00", "100", "5", "", "false", "car")
	f := fixture(t, trajectoriesHeader, row, row)
	if _, _, _, e := parseTrajectories(f, time.Time{}, time.Time{}); e == nil {
		t.Fatal("duplicate object observation accepted")
	}
}
func TestTrajectoryProbabilityOutOfRange(t *testing.T) {
	row := trajectoryRow("2023-09-24 23:30:00+00:00", "100", "5", "", "false", "car")
	row[17] = "1.5"
	f := fixture(t, trajectoriesHeader, row)
	if _, _, _, e := parseTrajectories(f, time.Time{}, time.Time{}); e == nil {
		t.Fatal("invalid class confidence accepted")
	}
}
func TestSpeedDisagreementOnlyDiagnostic(t *testing.T) {
	row := trajectoryRow("2023-09-24 23:30:00+00:00", "100", "0", "", "false", "car")
	f := fixture(t, trajectoriesHeader, row)
	r, _, _, e := parseTrajectories(f, time.Time{}, time.Time{})
	if e != nil {
		t.Fatal(e)
	}
	if r.SpeedMagnitudeDiffOver01 != 1 || r.SpeedMagnitudeDiffOver05 != 1 {
		t.Fatalf("speed not flagged: %+v", r)
	}
}
func TestSourceByteTamperingRejected(t *testing.T) {
	a := fixture(t, signalsHeader, []string{"2023-09-24 23:30:00+00:00", "1", "5"})
	b := fixture(t, trajectoriesHeader, trajectoryRow("2023-09-24 23:30:00+00:00", "100", "5", "", "false", "car"))
	if _, e := analyse(a, b); e == nil || !strings.Contains(e.Error(), "sha256 mismatch") {
		t.Fatalf("source tamper not caught: %v", e)
	}
}
func TestRawRealWorldIntegration(t *testing.T) {
	dir := os.Getenv("P33_SOURCE_DIR")
	if dir == "" {
		t.Skip("set P33_SOURCE_DIR for exact raw-data integration")
	}
	signals := filepath.Join(dir, "traffic-lights_230924-233000_230924-234500.csv")
	traj := filepath.Join(dir, "trajectories_230924-233000_230924-234500.csv")
	r, e := analyse(signals, traj)
	if e != nil {
		t.Fatal(e)
	}
	if r.Signals.Rows != 26970 || r.Signals.IDs != 30 || r.Signals.ObservedTransitions != 869 || r.Trajectories.Rows != 8624 || r.Trajectories.IDs != 37 {
		t.Fatalf("frozen count drift: %+v", r)
	}
	if r.Signals.SnapshotTimes != 899 || r.Signals.MinHeadsPerSnapshot != 30 || r.Signals.MaxHeadsPerSnapshot != 30 {
		t.Fatalf("signal head synchronization mismatch: %+v", r.Signals)
	}
	if len(r.Signals.SynchronizedGaps) != 1 {
		t.Fatalf("not one shared gap: %+v", r.Signals.SynchronizedGaps)
	}
	g := r.Signals.SynchronizedGaps[0]
	if g.AffectedSignalHeads != 30 || g.GapMs != 2004 || g.LastObservedUTC != "2023-09-24T23:31:44.01Z" || g.NextObservedUTC != "2023-09-24T23:31:46.014Z" {
		t.Fatalf("shared gap changed: %+v", g)
	}
	if r.Trajectories.MedianInterSampleMs != 50 || r.Trajectories.GapsOver100ms != 0 {
		t.Fatalf("trajectory frequency drift: %+v", r.Trajectories)
	}
	second, e := analyse(signals, traj)
	if e != nil || !reflect.DeepEqual(second, r) {
		t.Fatalf("non-deterministic run %v", e)
	}
	fmt.Println("Raw field-data SHA-verified Go integration: 30 synchronized signal heads, one 2.004s shared sampling gap, 37 tracks")
}
