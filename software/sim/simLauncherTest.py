import unittest
import simLauncher
import baseRoomDetectionBrain
import os

class SimulatorLauncherTestCase(unittest.TestCase):

	def setup(self):
		return

	def teardown(self):
		return

	def testLoadClass_loadsClassByClassPath(self):
		classPath = "baseRoomDetectionBrain.BaseRoomDetectionBrain"
		classObjExpected = baseRoomDetectionBrain.BaseRoomDetectionBrain
		classObj = simLauncher.SimulatorLauncher.loadClass(classPath)
		self.assertEqual(classObjExpected, classObj)

#	# TODO check None is returned for invalid module
#	def testLoadClass_returnsNoneOnInvalidModule(self):
#		return
#	# TODO check None is returned for invalid class
#	def testLoadClass_returnsNoneOnInvalidClass(self):
#		return

	def testFindBrainModules(self):
		brainDir = "tmp-test-brains"
		brainFile1 = os.path.join(brainDir, "barBrain.py")
		brainFile2 = os.path.join(brainDir, "fooBrain.py")

		os.mkdir(brainDir)
		open(brainFile1, "w+").write("\n")
		open(brainFile2, "w+").write("\n")

		expected = [brainFile1, brainFile2]

		try:
			self.assertEqual(expected, simLauncher.SimulatorLauncher.findBrainModules(brainDir))
		finally:
			os.unlink(brainFile1)
			os.unlink(brainFile2)
			os.rmdir(brainDir)

if __name__ == '__main__':
	unittest.main()
