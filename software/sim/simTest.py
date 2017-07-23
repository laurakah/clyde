import unittest
import sim
import gameMap

class SimTestCase(unittest.TestCase):
	
	def setUp(self):
		self.gameMapFile = "maps/test-room1-box.txt"
		self.s = sim.Sim(self.gameMapFile)
		
	def tearDown(self):
		return
		
	def testInit_runningState_isFalseOnInit(self):
		self.assertEqual(False, self.s.getRunningState())
		
	def testStart_setsRunningStateToTrue(self):
		self.s.start()
		self.assertEqual(True, self.s.getRunningState())
		
	def testInit_hasMap(self):
		self.assertIsInstance(self.s.getMap(), gameMap.GameMap)
	
	
if __name__ == "__main__":
	unittest.main()	