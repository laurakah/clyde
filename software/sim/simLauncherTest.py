import unittest
import simLauncher
import baseBrain
import os

class SimulatorLauncherTestCase(unittest.TestCase):

	def setup(self):
		return

	def teardown(self):
		return

	def testLoadClass_loadsClassByClassPath(self):
		classPath = "baseBrain.BaseBrain"
		classObjExpected = baseBrain.BaseBrain
		classObj = simLauncher.SimulatorLauncher.loadClass(classPath)
		self.assertEqual(classObjExpected, classObj)

#	# TODO check None is returned for invalid module
#	def testLoadClass_returnsNoneOnInvalidModule(self):
#		return
#	# TODO check None is returned for invalid class
#	def testLoadClass_returnsNoneOnInvalidClass(self):
#		return

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

if __name__ == '__main__':
	unittest.main()
