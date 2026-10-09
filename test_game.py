import unittest
from bloonvanta import Defense,PATH
class Tests(unittest.TestCase):
 def test_build(self):
  g=Defense();self.assertTrue(g.build((5,5),1));self.assertEqual(g.money,65)
 def test_path(self):self.assertFalse(Defense().build(PATH[0],1))
 def test_no_credit(self):
  g=Defense();g.money=0;self.assertFalse(g.build((5,5),1))
 def test_upgrade(self):
  g=Defense();g.build((5,5),1);self.assertTrue(g.upgrade((5,5)));self.assertEqual(g.towers[5,5]['level'],2)
 def test_start(self):
  g=Defense();self.assertTrue(g.start());self.assertFalse(g.start())
 def test_leak(self):
  g=Defense();g.start();g.remaining=0;g.balloons=[{'pos':len(PATH),'hp':1}];g.step(.1);self.assertEqual(g.lives,19)
 def test_hit(self):
  g=Defense();g.build((5,5),1);g.start();g.remaining=0;g.balloons=[{'pos':3.,'hp':1}];g.step(.1);self.assertFalse(g.balloons)
 def test_ten_waves(self):
  g=Defense();g.money=100000
  for p in ((5,5),(12,5),(15,8),(8,8),(5,12),(10,14),(19,13)):
   g.build(p,1);g.upgrade(p);g.upgrade(p)
  for _ in range(10):
   g.start()
   for tick in range(10000):
    g.step(.1)
    if not g.active:break
  self.assertTrue(g.won);self.assertGreater(g.lives,0)
if __name__=='__main__':unittest.main()
