import unittest
import simLauncher
import baseRoomDetectionBrain

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
"""
	# TODO check None is returned for invalid module
	def testLoadClass_returnsNoneOnInvalidModule(self):
		return
	# TODO check None is returned for invalid class
	def testLoadClass_returnsNoneOnInvalidClass(self):
		return
"""

if __name__ == '__main__':
	unittest.main()
