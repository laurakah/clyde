import unittest
import simLauncher
import sim
import dullBrain
import os

launchSimCalled = False
launchSimCalledNtimes = 0
launchSimArg = {'gameMapFile': None, 'brainClassPath': None, 'timeOut': None, 'delay': None, 'follow': None, 'verbose': None, 'position': None}
launchSimValue = None
launchSimMapsExecuted = []

def fakeLaunchSim(gameMapFile, brainClassPath, timeOut, delay, follow, verbose, position, orientation):
	global launchSimCalled
	global launchSimCalledNtimes
	global lanuchSimArg
	global launchSimValue
	global launchSimMapsExecuted

	launchSimCalled = True
	launchSimCalledNtimes += 1

	launchSimArg['gameMapFile'] = gameMapFile
	launchSimArg['brainClassPath'] = brainClassPath
	launchSimArg['timeOut'] = timeOut
	launchSimArg['delay'] = delay
	launchSimArg['follow'] = follow
	launchSimArg['verbose'] = verbose
	launchSimArg['position'] = position
	launchSimArg['orientation'] = orientation

	launchSimMapsExecuted.append(gameMapFile)

	return launchSimValue

class SimulatorLauncherTestCase(unittest.TestCase):

	def setUp(self):

		self.brainClassPath = "dullBrain.DullBrain"
		self.mapFileNameStartsWith = "test-room"
		self.excludeMaps = []
		self.timeOut = 5
		self.delay = 100
		self.follow = False
		self.verbose = False
		self.position = "random"
		self.orientation = "random"

		self.sl = simLauncher.SimulatorLauncher()

	def teardown(self):
		return

	def testLoadClass_loadsClassByClassPath(self):
		classPath = "dullBrain.DullBrain"
		classObjExpected = dullBrain.DullBrain
		classObj = simLauncher.SimulatorLauncher.loadClass(classPath)
		self.assertEqual(classObjExpected, classObj)

	# TODO change to raise simLauncherException
	# TODO check for specific error message (that is more specific compared to the python exception)
	def testLoadClass_raisesExceptionOnInvalidModule(self):
		e = ImportError
		classPath = "badModuleName.DullBrain"
		with self.assertRaises(e) as ex:
			simLauncher.SimulatorLauncher.loadClass(classPath)

	# TODO change to raise simLauncherException
	# TODO check for specific error message (that is more specific compared to the python exception)
	def testLoadClass_raisesExceptionOnInvalidClass(self):
		e = AttributeError
		classPath = "dullBrain.badClassName"
		with self.assertRaises(e) as ex:
			simLauncher.SimulatorLauncher.loadClass(classPath)

	def testFindBrainClasses(self):
		brainDir = "tmp-test-brains"
		brainModule1 = "barBrain"
		brainClass1 = "BarBrain"
		brainModule2 = "fooBrain"
		brainClass2 = "FooBrain"
		brainFile1 = os.path.join(brainDir, "%s.py" % brainModule1)
		brainFile2 = os.path.join(brainDir, "%s.py" % brainModule2)

		os.mkdir(brainDir)
		open(brainFile1, "w+").write("\n")
		open(brainFile2, "w+").write("\n")

		expected = [brainModule1 + "." + brainClass1, brainModule2 + "." + brainClass2]

		try:
			self.assertEqual(sorted(expected), sorted(simLauncher.SimulatorLauncher.findBrainClasses(brainDir)))
		finally:
			os.unlink(brainFile1)
			os.unlink(brainFile2)
			os.rmdir(brainDir)

	def testIsValidStartPosition_returnsFalseByDefault(self):
		sl = simLauncher.SimulatorLauncher
		self.assertEqual(False, sl.isValidStartPosition("foo"))

	def testIsValidStartPosition_returnsTrueWhenArgIsStrRandom(self):
		sl = simLauncher.SimulatorLauncher
		self.assertEqual(True, sl.isValidStartPosition("random"))

	def testIsvalidStartPosition_returnsTrueWhenArgIsStrRand(self):
		sl = simLauncher.SimulatorLauncher
		self.assertEqual(True, sl.isValidStartPosition("rand"))

	def testIsValidStartPosition_returnsTrueWhenArgIsValidCoordinateStr(self):
		sl = simLauncher.SimulatorLauncher
		self.assertEqual(True, sl.isValidStartPosition("3,9"))

	def testisValidStartPosition_returnsFalseWhenArgIsInvalidCoordinate(self):
		sl = simLauncher.SimulatorLauncher
		self.assertEqual(False, sl.isValidStartPosition("0,0"))

	def testLaunchSim_returnsReport(self):
		rep = self.sl.launchSim()
		self.assertEqual(True, type(rep) is dict)

	def _createDirAndFiles(self, dirName, files):
		os.mkdir(dirName)
		for f in files:
			open(f, "w+").write("")

	def _removeFilesAndDir(self, dirName, files):
		for f in files:
			os.unlink(f)
		os.rmdir(dirName)

	def testLaunchSimForAllMaps_callsLaunchSimNtimes(self):
		global launchSimCalledNtimes
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_callsLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-foo.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-bar.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-bla.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-fnord.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-baz.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimCalledNtimes = 0
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(5, launchSimCalledNtimes)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_onlyCallsLaunchSimForMapFilesMatchingStartsWithPattern(self):
		global launchSimCalledNtimes
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_onlyCallsLaunchSimForMapFilesMatchingStartsWithPattern"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-foo.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-tbar.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "bla.txt"),
			os.path.join(fakeMapDir, "%s-fnord.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "baz.txt")
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimCalledNtimes = 0
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(3, launchSimCalledNtimes)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_skipsMapsExcluded(self):
		global launchSimCalledNtimes
		fakeMapDir = "testLaunchSimForAllMaps_skipsMapsExcluded"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-x1.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-x2.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-x3.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-x4.txt" % self.mapFileNameStartsWith)
		]
		excludeMaps = [
			"%s-x1.txt" % self.mapFileNameStartsWith,
			"%s-x2.txt" % self.mapFileNameStartsWith
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimCalledNtimes = 0
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(2, launchSimCalledNtimes)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_executesMapsInOrder(self):
		global launchSimMapsExecuted
		fakeMapDir = "testLaunchSimForAllMaps_executesMapsInOrder"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-6.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-9.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-a.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-1.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-7.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-4.txt" % self.mapFileNameStartsWith),
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimMapsExecuted = []
		expectedMapExecutionOrder = fakeMapFiles
		expectedMapExecutionOrder.sort()
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(expectedMapExecutionOrder, launchSimMapsExecuted)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesGameMapFileToLaunchSim(self):
		global launchSimArg
		fakeMapDir = "testLaunchSimForAllMaps_passesGameMapFileToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-super.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['gameMapFile'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(fakeMapFiles[0], launchSimArg['gameMapFile'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesBrainClassPathToLaunchSim(self):
		global launchSimArg
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_passesBrainClassPathToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['brainClassPath'] = None
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(self.brainClassPath, launchSimArg['brainClassPath'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesStartPositionStringToLaunchSim(self):
		global launchSimArg
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_passesStartPositionStringToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-1.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-2.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-3.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['position'] = None
		# do we need to set the launchSimValue exit code?
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual("random", launchSimArg["position"])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesStartOrientationStringToLaunchSim(self):
		global launchSimArg
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_passesStartOrientationStrintToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-one.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-two.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-three.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['orientation'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual("random", launchSimArg["orientation"])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesTimeOutToLaunchSim(self):
		global launchSimArg
		fakeMapDir = "testLaunchSimForAllMaps_passesTimeOutToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % self.mapFileNameStartsWith)
		]
		timeOut = 10
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['timeOut'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(timeOut, launchSimArg['timeOut'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesDelayToLaunchSim(self):
		global launchSimArg
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_passesDelayToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % self.mapFileNameStartsWith)
		]
		delay = 500
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['delay'] = None
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, delay, self.follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(delay, launchSimArg['delay'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesFollowToLaunchSim(self):
		global launchSimArg
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_passesFollowToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % self.mapFileNameStartsWith)
		]
		follow = True
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['follow'] = None
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, follow, self.verbose,
							self.position, self.orientation)
			self.assertEqual(follow, launchSimArg['follow'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesVerboseToLaunchSim(self):
		global launchSimArg
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_passesVerboseToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % self.mapFileNameStartsWith)
		]
		verbose = True
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['verbose'] = None
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, verbose,
							self.position, self.orientation)
			self.assertEqual(verbose, launchSimArg['verbose'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_returnsZeroWhenAllSimReportsContainExitCodeMapMatch(self):
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_returnsZeroWhenAllSimReportsContainExitCodeMapMatch"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-a.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-b.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-c.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_MAPMATCH}
		self.sl.launchSim = fakeLaunchSim
		try:
			rv = self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
								self.timeOut, self.delay, self.follow, self.verbose,
								self.position, self.orientation)
			self.assertEqual(0, rv)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_returnsOneWhenAtLeastOneSimReportContainExitNotEqualCodeMapMatch(self):
		global launchSimValue
		fakeMapDir = "testLaunchSimForAllMaps_returnsZeroWhenAllSimReportsContainExitCodeMapMatch"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-a.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-b.txt" % self.mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-c.txt" % self.mapFileNameStartsWith)
		]
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimValue = {'exitCode': sim.Sim.EXITCODE_TIMEOUT}
		self.sl.launchSim = fakeLaunchSim
		rv = self.sl.launchSimForAllMaps(self.brainClassPath, fakeMapDir, self.mapFileNameStartsWith, self.excludeMaps,
							self.timeOut, self.delay, self.follow, self.verbose,
							self.position, self.orientation)
		try:
			self.assertEqual(1, rv)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)


if __name__ == '__main__':
	unittest.main()
