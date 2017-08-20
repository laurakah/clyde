import unittest
import simLauncher
import dullBrain
import os

launchSimCalled = False
launchSimCalledNtimes = 0
launchSimArg = {'gameMapFile': None, 'brainClassPath': None, 'timeOut': None, 'delay': None, 'follow': None, 'verbose': None}

def fakeLaunchSim(gameMapFile, brainClassPath, timeOut, delay, follow, verbose):
	global launchSimCalled
	global launchSimCalledNtimes
	global lanuchSimArg

	launchSimCalled = True
	launchSimCalledNtimes += 1

	launchSimArg['gameMapFile'] = gameMapFile
	launchSimArg['brainClassPath'] = brainClassPath
	launchSimArg['timeOut'] = timeOut
	launchSimArg['delay'] = delay
	launchSimArg['follow'] = follow
	launchSimArg['verbose'] = verbose

class SimulatorLauncherTestCase(unittest.TestCase):

	def setUp(self):
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
			self.assertEqual(expected, simLauncher.SimulatorLauncher.findBrainClasses(brainDir))
		finally:
			os.unlink(brainFile1)
			os.unlink(brainFile2)
			os.rmdir(brainDir)

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
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_callsLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-foo.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-bar.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-bla.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-fnord.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-baz.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 5
		delay = 100
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimCalledNtimes = 0
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(5, launchSimCalledNtimes)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_onlyCallsLaunchSimForMapFilesMatchingStartsWithPattern(self):
		global launchSimCalledNtimes
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_onlyCallsLaunchSimForMapFilesMatchingStartsWithPattern"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-foo.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-tbar.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "bla.txt"),
			os.path.join(fakeMapDir, "%s-fnord.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "baz.txt")
		]
		excludeMaps = []
		timeOut = 5
		delay = 100
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimCalledNtimes = 0
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(3, launchSimCalledNtimes)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_skipsMapsExcluded(self):
		global launchSimCalledNtimes
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_skipsMapsExcluded"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-x1.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-x2.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-x3.txt" % mapFileNameStartsWith),
			os.path.join(fakeMapDir, "%s-x4.txt" % mapFileNameStartsWith)
		]
		excludeMaps = [
			"%s-x1.txt" % mapFileNameStartsWith,
			"%s-x2.txt" % mapFileNameStartsWith
		]
		timeOut = 5
		delay = 100
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimCalledNtimes = 0
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(2, launchSimCalledNtimes)
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesGameMapFileToLaunchSim(self):
		global launchSimArg
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_passesGameMapFileToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-super.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 5
		delay = 100
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['gameMapFile'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(fakeMapFiles[0], launchSimArg['gameMapFile'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesBrainClassPathToLaunchSim(self):
		global launchSimArg
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_passesBrainClassPathToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 5
		delay = 100
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['brainClassPath'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(brainClassPath, launchSimArg['brainClassPath'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesTimeOutToLaunchSim(self):
		global launchSimArg
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_passesTimeOutToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 10
		delay = 100
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['timeOut'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(timeOut, launchSimArg['timeOut'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesDelayToLaunchSim(self):
		global launchSimArg
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_passesDelayToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 10
		delay = 500
		follow = False
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['delay'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(delay, launchSimArg['delay'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesFollowToLaunchSim(self):
		global launchSimArg
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_passesFollowToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 10
		delay = 500
		follow = True
		verbose = False
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['follow'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(follow, launchSimArg['follow'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

	def testLaunchSimForAllMaps_passesVerboseToLaunchSim(self):
		global launchSimArg
		brainClassPath = "dullBrain.DullBrain"
		mapFileNameStartsWith = "test-room"
		fakeMapDir = "testLaunchSimForAllMaps_passesVerboseToLaunchSim"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "%s-ooops.txt" % mapFileNameStartsWith)
		]
		excludeMaps = []
		timeOut = 10
		delay = 500
		follow = False
		verbose = True
		self._createDirAndFiles(fakeMapDir, fakeMapFiles)
		launchSimArg['verbose'] = None
		self.sl.launchSim = fakeLaunchSim
		try:
			self.sl.launchSimForAllMaps(brainClassPath, fakeMapDir, mapFileNameStartsWith, excludeMaps,
							timeOut, delay, follow, verbose)
			self.assertEqual(verbose, launchSimArg['verbose'])
		finally:
			self._removeFilesAndDir(fakeMapDir, fakeMapFiles)

if __name__ == '__main__':
	unittest.main()
