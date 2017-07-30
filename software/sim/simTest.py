import unittest
import sim
import gameMap
import baseRoomDetectionBrain
import player

		
startCalled = False
playerStepCalled = False
playerGetPositionCalled = False
playerGetPositionValue = {}
playerIsFinishedCalled = False
playerIsFinishedValue = False
playerGetMapValue = []

def fakeStart():
	global startCalled
	startCalled = True
	
def fakePlayerStep():
	global playerStepCalled
	playerStepCalled = True
	
def fakePlayerGetPosition():
	global playerGetPositionCalled
	global playerGetPositionValue
	playerGetPositionCalled = True
	return playerGetPositionValue
	
def fakePlayerIsFinished():
	global playerIsFinishedCalled
	global playerIsFinishedValue
	playerIsFinishedCalled = True
	return playerIsFinishedValue

def fakePlayerGetMap():
	global playerGetMapValue
	return playerGetMapValue


class SimTestCase(unittest.TestCase):
	
	def setUp(self):
		self.gameMapFile = "maps/test-room1-box.txt"
		self.brainClass = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.s = sim.Sim(self.gameMapFile, self.brainClass, sim.Sim.DEFAULT_TIMEOUT)
		
	def tearDown(self):
		return
		
	def testInit_runningState_isFalse(self):
		self.assertEqual(False, self.s.getRunningState())
		
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
		
	def testInit_exitCode_isNoneOnInit(self):
		self.assertEqual(None, self.s.getExitCode())
		
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
		
	def testStep_callsPlayerIsFinished(self):
		global playerIsFinishedCalled
		playerIsFinishedCalled = False
		self.s.player.isFinished = fakePlayerIsFinished
		self.s.start()
		self.s.step()
		self.assertEqual(True, playerIsFinishedCalled)
		
	def testStep_setsRunningStateToFalse_onTimeOut(self):
		self.s.setTimeOut(100)
		self.s.start()
		for i in range(0, 101):
			self.s.step()
		self.assertEqual(False, self.s.getRunningState())
		
	def testStep_setsExitCode_onTimeOut(self):
		self.s.run()
		self.assertEqual(sim.Sim.EXITCODE_TIMEOUT, self.s.getExitCode())
		
	def testStep_setsExitCode_onMapMissMatch(self):
		global playerIsFinishedValue
		playerIsFinishedValue = True
		self.s.player.isFinished = fakePlayerIsFinished
		self.s.run()
		self.assertEqual(sim.Sim.EXITCODE_MAPMISSMATCH, self.s.getExitCode())
		
	def testStep_setsExitCode_onMapMatch(self):
		global playerGetMapValue
		global playerIsFinishedValue
		playerIsFinishedValue = True
		playerGetMapValue = gameMap.GameMap.readMapFile(self.gameMapFile)
		self.s.player.isFinished = fakePlayerIsFinished
		self.s.player.getMap = fakePlayerGetMap
		self.s.run()
		self.assertEqual(sim.Sim.EXITCODE_MAPMATCH, self.s.getExitCode())
		
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
		
	def testGetPosition_isPlayerPosition(self):
		expectedPos = {"x": 0, "y": 0}
		self.assertEqual(expectedPos, self.s.getPosition())
		
	def testGetPosition_callsPlayerGetPosition(self):
		global playerGetPositionCalled
		playerGetPositionCalled = False
		self.s.player.getPosition = fakePlayerGetPosition
		self.s.getPosition()
		self.assertEqual(True, playerGetPositionCalled)
		
	def testGetPosition_returnsValueFromPlayerGetPosition(self):
		global playerGetPositionValue
		playerGetPositionValue = "12345"
		self.s.player.getPosition = fakePlayerGetPosition
		self.assertEqual(playerGetPositionValue, self.s.getPosition())
		
# 	def testDraw_drawsGameMapWithPlayerPosition(self):
# 		global playerGetMapValue
# 		pos = self.s.getPosition()
# 		expectedMap = self.s.getMap().getMap()
# 		expectedMap[pos["x"]][pos["y"]] = 2					# 2 == player
# 		playerGetMapValue = expectedMap
# 		expectedMap = gameMap.GameMap.arrayToText(expectedMap)
# 		self.s.player.getMap = fakePlayerGetMap
# 		self.assertEqual(expectedMap, self.s.draw())
		
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

	def testGetReport_returnsDictWithBrainClassName(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.brainClass, rep["brainClass"])

	def testGetReport_returnsDictWithExitCode(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.s.getExitCode(), rep["exitCode"])
	
	
if __name__ == "__main__":
	unittest.main()	