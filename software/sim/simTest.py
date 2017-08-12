import unittest
import sim
import gameMap
import baseBrain
import player
import time

		
startCalled = False
playerStepCalled = False
playerGetPositionCalled = False
playerGetPositionValue = {}
playerIsFinishedCalled = False
playerIsFinishedValue = False
playerGetMapValue = []
playerGetPlayerMapCalled = False
playerGetPlayerMapValue = []
drawCalled = False
drawValue = None
drawSimMapCalled = False
drawPlayerMapCalled = False
drawPlayerMapValue = ""
printCalled = False
printValue = None

def fakeStart():
	global startCalled
	startCalled = True

def fakeDrawSimMap():
	global drawSimMapCalled
	drawSimMapCalled = True
	# NOTE Make sure this map is the same as used in setup
	# of this test case
	m = gameMap.GameMap.readMapFile("maps/test-room1-box.txt")
	txt = gameMap.GameMap.arrayToText(m)
	return txt

def fakeDrawPlayerMap():
	global drawPlayerMapCalled
	global drawPlayerMapValue
	drawPlayerMapCalled = True
	return drawPlayerMapValue
	
def fakeDraw():
	global drawCalled
	global drawValue
	drawCalled = True
	return drawValue

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
	
def fakePlayerGetPlayerMap():
	global playerGetPlayerMapCalled
	global playerGetPlayerMapValue
	playerGetPlayerMapCalled = True
	return playerGetPlayerMapValue

def fakePrint(s):
	global printCalled
	global printValue
	printCalled = True
	printValue = s

class SimTestCase(unittest.TestCase):
	
	def setUp(self):
		self.gameMapFile = "maps/test-room1-box.txt"
		self.brainClass = baseBrain.BaseBrain
		self.s = sim.Sim(self.gameMapFile, self.brainClass, sim.Sim.DEFAULT_TIMEOUT)
		
	def tearDown(self):
		return
		
	def testInit_runningState_isFalse(self):
		self.assertEqual(False, self.s.getRunningState())
		
	def testInit_stepCount_isZero(self):
		self.assertEqual(0, self.s.getStepCount())
		
	def testInit_stepDelay_isZero(self):
		self.assertEqual(0, self.s.getStepDelay())

	def testInit_stepDelay_isUserSpecified(self):
		delay = 500
		s = sim.Sim(self.gameMapFile, self.brainClass, sim.Sim.DEFAULT_TIMEOUT, delay)
		self.assertEqual(delay, s.getStepDelay())

	def testInit_hasInstanceOfGameMap(self):
		self.assertIsInstance(self.s.getSimMap(), gameMap.GameMap)
		
	def testInit_startPosition_isNonCollisionField(self):
		startPos = self.s.getStartPosition()
		nonCollisionFields = self.s.getSimMap().getNonCollisionFields()
		self.assertEqual(True, startPos in nonCollisionFields)

	def testInit_startPosition_isSameWithinSimulatorInstance(self):
		startPos1 = self.s.getStartPosition()
		startPos2 = self.s.getStartPosition()
		self.assertEqual(startPos1, startPos2)

	def testInit_startPosition_isRandom(self):
		startPos1 = None
		startPos2 = None
		s1 = sim.Sim(self.gameMapFile, self.brainClass, sim.Sim.DEFAULT_TIMEOUT)
		startPos1 = s1.getStartPosition()
		s2 = sim.Sim(self.gameMapFile, self.brainClass, sim.Sim.DEFAULT_TIMEOUT)
		startPos2 = s2.getStartPosition()
		self.assertNotEqual(startPos1, startPos2)
		
	def testInit_setsStartOrientationRandomlyWithinSimInstance(self):
		orientation1 = self.s.getStartOrientation()
		orientation2 = self.s.getStartOrientation()
		self.assertEqual(orientation1, orientation2)
		
	def testInit_setsStartOrientationRandomly(self):
		try1 = []
		try2 = []
		for i in range(0, 5):
			s1 = sim.Sim(self.gameMapFile, self.brainClass)
			try1.append(s1.getStartOrientation())
		for i in range(0, 5):	
			s2 = sim.Sim(self.gameMapFile, self.brainClass)
			try2.append(s2.getStartOrientation())
		self.assertNotEqual(try1, try2)

# 	def testInit_playerPosition_isStartPosition(self):
# 		self.assertEqual(self.s.startPosition, self.s.getPosition())

	def testInit_timeOut_isDefault(self):
		self.assertEqual(sim.Sim.DEFAULT_TIMEOUT, self.s.getTimeOut())
		
	def testInit_timeOut_isUserSpecified(self):
		timeOut = 8888
		s = sim.Sim(self.gameMapFile, self.brainClass, timeOut)
		self.assertEqual(timeOut, s.getTimeOut())
		
	def testInit_exitCode_isNoneOnInit(self):
		self.assertEqual(None, self.s.getExitCode())
		
	def testInit_followIsFalseByDefault(self):
		self.assertEqual(False, self.s.followIsSet())
		
	def testInit_followIsUserSpecified(self):
		s = sim.Sim(self.gameMapFile, self.brainClass, 20, 20, True)
		self.assertEqual(True, s.followIsSet())
		
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
		
	def testRun_delaysStepsByStepDelay(self):
		delayMs = 50
		timeOut = 3
		deviationMs = 20
		expectedDelta = (timeOut) * delayMs
		s = sim.Sim(self.gameMapFile, self.brainClass, timeOut, delayMs)
		t1 = time.time()
		s.run()
		t2 = time.time()
		deltaMs = int((t2 - t1) * 1000)
		self.assertAlmostEqual(expectedDelta, deltaMs, None, None, deviationMs)
		
	def testRun_callsDrawWhenFollowIsTrue(self):
		global drawCalled
		s = sim.Sim(self.gameMapFile, self.brainClass, 2, 0, True)
		s.draw = fakeDraw
		# override only so that the real print is not called
		# in order not to polute our test output
		s._print = fakePrint
		drawCalled = False
		s.run()
		self.assertEqual(True, drawCalled)
		
	def testRun_doesNotCallDrawWhenFollowIsFalse(self):
		global drawCalled
		s = sim.Sim(self.gameMapFile, self.brainClass, 2, 0, False)
		s.draw = fakeDraw
		drawCalled = False
		s.run()
		self.assertEqual(False, drawCalled)
		
	def testRun_callsPrintWhenFollowIsTrue(self):
		global printCalled
		printCalled = False
		s = sim.Sim(self.gameMapFile, self.brainClass, 2, 0, True)
		s._print = fakePrint
		s.run()
		self.assertEqual(True, printCalled)

	def testRun_callsPrintWithReturnFromDrawWhenFollowIsTrue(self):
		global drawValue
		global printValue
		drawValue = "xxx"
		printValue = None
		s = sim.Sim(self.gameMapFile, self.brainClass, 2, 0, True)
		s.draw = fakeDraw
		s._print = fakePrint
		s.run()
		self.assertEqual("xxx", printValue)

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
		self.s.player.getPlayerMap = fakePlayerGetMap
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
		
	def testGetPlayerMap_callsPlayerGetPlayerMap(self):
		global playerGetPlayerMapCalled
		playerGetPlayerMapCalled = False
		self.s.player.getPlayerMap = fakePlayerGetPlayerMap
		self.s.getPlayerMap()
		self.assertEqual(True, playerGetPlayerMapCalled)
		
	def testGetPlayerMap_returnsPlayerGetPlayerMapValue(self):
		global playerGetPlayerMapValue
		playerGetPlayerMapValue = []
		self.s.player.getPlayerMap = fakePlayerGetPlayerMap
		self.assertEqual(playerGetPlayerMapValue, self.s.getPlayerMap())

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
		
	def testDrawPlayerMap_drawsGameMapWithPlayerPosition(self):
		global playerGetMapValue
		setLoc = gameMap.GameMap.setLocationInArray
		playerSymbol = gameMap.GameMap.PLAYER_POSITION_VALUE
		pos = {"x": 2, "y": 2}
		simMapObj = self.s.getSimMap()
		simMapArray = simMapObj.getMapArray()
		setLoc(simMapArray, pos["y"], pos["x"], playerSymbol)
		playerGetMapValue = simMapArray
		txtMap = gameMap.GameMap.arrayToText(simMapArray)
		self.s.player.getPlayerMap = fakePlayerGetMap
		self.assertEqual(txtMap, self.s.drawPlayerMap())
		
	def testDrawSimMap_drawsGameMapWithPlayerPosition(self):
		setLoc = gameMap.GameMap.setLocationInArray
		playerSymbol = gameMap.GameMap.PLAYER_POSITION_VALUE
		pos = self.s.getPosition()
		simMapArray = self.s.getSimMap().getMapArray()
		setLoc(simMapArray, pos['x'], pos['y'], playerSymbol)
		txtMap = gameMap.GameMap.arrayToText(simMapArray)
		self.assertEqual(txtMap, self.s.drawSimMap())

	def testDraw_callsDrawSimMap(self):
		global drawSimMapCalled
		drawSimMapCalled = False
		self.s.drawSimMap = fakeDrawSimMap
		self.s.draw()
		self.assertEqual(True, drawSimMapCalled)

	def testDraw_callsDrawPlayerMap(self):
		global drawPlayerMapCalled
		drawPlayerMapCalled = False
		self.s.drawPlayerMap = fakeDrawPlayerMap
		self.s.draw()
		self.assertEqual(True, drawPlayerMapCalled)

	def testDraw_returnsSimAndPlayerMapSideBySide(self):
		global drawPlayerMapValue

		txtExpect = ""
		txtPlayerMap = "###\n#*#\n###\n"

		# install fake

		drawPlayerMapValue = txtPlayerMap
		self.s.drawPlayerMap = fakeDrawPlayerMap

		# get text maps

		txtSimMapArr = self.s.drawSimMap().rstrip().split('\n')
		txtPlayerMapArr = self.s.drawPlayerMap().rstrip().split('\n')

		# get map dimensions

		simMapHeight = self.s.getSimMap().getHeight()
		playerMapHeight = len(txtPlayerMapArr)
		playerMapOffset = simMapHeight - playerMapHeight

		# combine both maps

		player_i = 0
		for sim_i in range(0, simMapHeight):
			txtExpect += txtSimMapArr[sim_i]
			if sim_i >= playerMapOffset:
				txtExpect += " "
				txtExpect += txtPlayerMapArr[player_i]
				player_i += 1
			txtExpect += "\n"

		self.assertEqual(txtExpect, self.s.draw())

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

	def testGetReport_returnsDictWithStartPosition(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.s.getStartPosition(), rep["startPosition"])
		
	def testGetReport_returnsDictWithSimMap(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.s.getSimMap(), rep["simMap"])
		
	def testGetReport_returnsDictWithPlayerMap(self):
		self.s.run()
		rep = self.s.getReport()
		self.assertEqual(self.s.getPlayerMap(), rep["playerMap"])
	
	
if __name__ == "__main__":
	unittest.main()	