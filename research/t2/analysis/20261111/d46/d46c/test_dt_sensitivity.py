import unittest
from corridor import run

class TimeGridSensitivity(unittest.TestCase):
 def simulate(self,dt):
  n=round(40/dt)
  arrivals=[(3. if k*dt<25 else 0.)*dt for k in range(n)]
  exits=[(0. if k*dt<10 else 1. if k*dt<30 else 4.)*dt for k in range(n)]
  return run(arrivals,[4*dt]*n,exits,6)
 def test_inflow_invariant(self):
  for h in (1,.5,.25,.125,.0625):
   self.assertAlmostEqual(self.simulate(h)[-1].state.cumul_arrivals,75)
 def test_large_grid_is_biased(self):
  self.assertAlmostEqual(self.simulate(1)[-1].state.cumul_exits,50)
  self.assertAlmostEqual(self.simulate(.5)[-1].state.cumul_exits,60)
 def test_small_grid_exits_plateau(self):
  for h in (.5,.25,.125,.0625):self.assertAlmostEqual(self.simulate(h)[-1].state.cumul_exits,60)
 def test_conservation_under_refinement(self):
  for h in (1,.5,.25,.125,.0625):
   for z in self.simulate(h):self.assertAlmostEqual(z.end_conservation_error,0,places=8)
if __name__=='__main__':unittest.main()
