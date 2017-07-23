import unittest
import sim
import gameMap
import baseRoomDetectionBrain
import player

		
startCalled = False
playerStepCalled = False
playerIsFinishedCalled = False
playerIsFinishedValue = False

def fakeStart():
	global startCalled
	startCalled = True
	
def fakePlayerStep():
	global playerStepCalled
	playerStepCalled = True
	
def fakePlayerIsFinished():
	global playerIsFinishedCalled
	global playerIsFinishedValue
	playerIsFinishedCalled = True
	return playerIsFinishedValue



class SimTestCase(unittest.TestCase):
	
	def setUp(self):
		self.gameMapFile = "maps/test-room1-box.txt"
		self.brainClass = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.s = sim.Sim(self.gameMapFile, self.brainClass, sim.Sim.DEFAULT_TIMEOUT)
		
	def tearDown(self):
		return
		
	def testInit_runningState_isFalse(self):
		self.assertEqual(False, self.s.getRunningState())
		
# 	def testInit_gameOverState_isFalse(self):
# 		self.assertEqual(False, self.s.getGameOverState())
		
	def testInit_stepCount_isZero(self):
		self.assertEqual(0, self.s.getStepCount())
		
	def testInit_hasMap(self):
		self.assertIsInstance(self.s.getMap(), gameMap.GameMap)
		
	def testInit_timeOut_isDefault(self):
		self.assertEqual(sim.Sim.DEFAULT_TIMEOUT, self.s.getTimeOut())
		
	def testInit_timeOut_isUserSpecified(self):
		timeOut = 8888
		s = sim.Sim(self.gameMapFile, self.brainClass, timeOut)
		self.assertEqual(timeOut, s.getTimeOut())
		
	def testSetTimeOut(self):
		timeOut = 66666
		self.s.setTimeOut(timeOut)
		self.assertEqual(timeOut, self.s.getTimeOut())
		
	def testStart_setsRunningStateToTrue(self):
		self.s.start()
		self.assertEqual(True, self.s.getRunningState())
	
	def testRun_callsStart(self):
		global startCalled
		startCalled = False
		self.s.start = fakeStart
		self.s.run()
		self.assertEqual(True, startCalled)
		
	def testRun_runningState_isFalseOnReturn(self):
		self.s.run()
		self.assertEqual(False, self.s.getRunningState())
		
	def testStep_incrementsStepCount(self):
		stepCount = self.s.getStepCount()
		self.s.start()
		self.s.step()
		self.assertEqual(stepCount + 1, self.s.getStepCount())
		
	def testStep_stepCount_doesNotIncrementWhenRunningStateIsFalse(self):
		stepCount = self.s.getStepCount()
		self.s.step()
		self.assertEqual(stepCount, self.s.getStepCount())
		
	def testStep_callsPlayerStep(self):
		global playerStepCalled
		playerStepCalled = False
		self.s.player.step = fakePlayerStep
		self.s.start()
		self.s.step()
		self.assertEqual(True, playerStepCalled)
		
# 	def testStep_setsIsFinishedToTrue_onTimeOut(self):
# 		self.s.setTimeOut(100)
# 		self.s.start()
# 		for i in range(0, 101):
# 			self.s.step()
# 		self.assertEqual(True, self.s.isFinished())
		
	def testStep_setsRunningStateToFalse_onTimeOut(self):
		self.s.setTimeOut(100)
		self.s.start()
		for i in range(0, 101):
			self.s.step()
		self.assertEqual(False, self.s.getRunningState())
		
	def testIsFinished_callsPlayerIsFinished(self):
		global playerIsFinishedCalled
		playerIsFinishedCalled = False
		self.s.player.isFinished = fakePlayerIsFinished
		self.s.isFinished()
		self.assertEqual(True, playerIsFinishedCalled)
		
	def testIsFinished_returnsPlayerIsFinishedValue(self):
		global playerIsFinishedValue
		playerIsFinishedValue = True
		self.s.player.isFinished = fakePlayerIsFinished
		self.assertEqual(playerIsFinishedValue, self.s.isFinished())
		
	def testGetReport_returnsDictWithStepCount(self):
		self.s.run()
		stepCount = self.s.getStepCount()
		rep = self.s.getReport()
		self.assertEqual(stepCount, rep["stepCount"])
		
	def testGetReport_returnsDictWithGameMapFile(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.s.gameMapFile, rep["gameMapFile"])
		
	def testGetReport_returnsDictWithTimeOut(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.s.getTimeOut(), rep["timeOut"])
	
	
if __name__ == "__main__":
	unittest.main()	