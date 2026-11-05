import unittest
from src.micro_network import Link,Network,Demand
class DirectedTopologyTest(unittest.TestCase):
 def test_connected_route(self):
  net=Network([Link('a',15),Link('b',15)],connections={'a':('b',)})
  self.assertIn('x',net.run([Demand('x',0,('a','b'))],60).completed_s)
 def test_invalid_connection(self):
  net=Network([Link('a',15),Link('b',15)],connections={'a':()})
  with self.assertRaises(ValueError):net.run([Demand('x',0,('a','b'))],60)
if __name__=='__main__':unittest.main()
