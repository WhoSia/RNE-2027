// Independent cumulative-flow oracle for the P150A integer model.
package main

import (
	"fmt"
)

func arrival(tape string, t int) int {
	switch tape {
	case "uniform":
		if t < 24 {
			return 1
		}
	case "pairs":
		if t < 24 && t%2 == 0 {
			return 2
		}
	case "clustered":
		if t < 36 && t%6 < 2 {
			return 2
		}
	default:
		panic("unknown tape")
	}
	return 0
}

func run(tape string, D, p, phi, reuse int) (int, int, int) {
	A, E, F, Z, cost, denied := 0, 0, 0, 0, 0, 0
	for t := 0; t < 200; t++ {
		A += arrival(tape, t)
		green := (t+phi)%p < p/2
		sink := 0
		if t%8 < 4 {
			sink = 2
		}
		nextZ := min(F, Z+sink)
		nextE := min(A, E+2, 6+F)
		available := D + Z
		if reuse == 1 {
			available = D + nextZ
		}
		nextF := F
		if green {
			nextF = min(E, F+2, available)
		}
		if green && E > F && F == available {
			denied++
		}
		if nextE < E || nextF < F || nextZ < Z || nextE > A || nextF > E || nextZ > F || nextE-nextF > 6 || nextF-nextZ > D {
			panic("invariant")
		}
		E, F, Z = nextE, nextF, nextZ
		cost += A - Z
	}
	if A != 24 || E != 24 || F != 24 || Z != 24 {
		panic("clearance")
	}
	return cost, denied, Z
}
func main() {
	for _, tape := range []string{"uniform", "pairs", "clustered"} {
		for D := 1; D <= 6; D++ {
			for _, p := range []int{4, 8} {
				for phi := 0; phi < p; phi++ {
					for reuse := 0; reuse < 2; reuse++ {
						c, d, z := run(tape, D, p, phi, reuse)
						fmt.Printf("%s,%d,%d,%d,%d,%d,%d,%d\n", tape, D, p, phi, reuse, c, d, z)
					}
				}
			}
		}
	}
}
