import unittest
import simLauncher
import dullBrain
import os

launchSimCalled = False
launchSimCalledNtimes = 0

def fakeLaunchSim():
	global launchSimCalled
	global launchSimCalledNtimes
	launchSimCalled = True
	launchSimCalledNtimes += 1

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

	def testLaunchSimForAllMaps_callsLaunchSimNtimes(self):
		global launchSimCalledNtimes
		fakeMapDir = "fakeMaps"
		fakeMapFiles = [
			os.path.join(fakeMapDir, "foo.txt"),
			os.path.join(fakeMapDir, "bar.txt"),
			os.path.join(fakeMapDir, "bla.txt"),
			os.path.join(fakeMapDir, "fnord.txt"),
			os.path.join(fakeMapDir, "baz.txt")
		]

		# create fake map directory with fake maps

		os.mkdir(fakeMapDir)
		for f in fakeMapFiles:
			open(f, "w+").write("")

		launchSimCalledNtimes = 0
		self.sl.launchSim = fakeLaunchSim
		self.sl.launchSimForAllMaps(fakeMapDir)
		try:
			self.assertEqual(5, launchSimCalledNtimes)
		finally:
			# clean up fake files and map directory

			for f in fakeMapFiles:
				os.unlink(f)
			os.rmdir(fakeMapDir)

if __name__ == '__main__':
	unittest.main()
