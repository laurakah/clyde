import unittest
import sim

class SimTestCase(unittest.TestCase):
	
	def setUp(self):
# 		self.gameMapFile = "maps/test-room1-box.txt"
		self.s = sim.Sim()
		
	def tearDown(self):
		return
		
	def testInit_runningState_isFalseOnInit(self):
		self.assertEqual(False, self.s.getRunningState())
		
	def testStart_setsRunningStateToTrue(self):
		self.s.start()
		self.assertEqual(True, self.s.getRunningState())
		
	
	
if __name__ == "__main__":
	unittest.main()	