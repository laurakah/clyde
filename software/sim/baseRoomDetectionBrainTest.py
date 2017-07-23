import unittest
import baseRoomDetectionBrain

class BaseRoomDetectionBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.inputs = [0]
		self.outputs = [1]
		self.b = baseRoomDetectionBrain.BaseRoomDetectionBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
	
	def testGetBrainMap_returnsArray(self):
		self.assertIsInstance(self.b.getBrainMap(), list)
		
	def testIsFinished_returnsBoolean(self):
		self.assertIsInstance(self.b.isFinished(), bool)
		
	def testClass_hasStepMethod(self):
		self.assertEqual(True, "step" in dir(self.b))
		
	def testInit_raisesInputsEmptyException(self):
		e = baseRoomDetectionBrain.InputsEmptyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, [], self.outputs)
		
	def testInit_raisesOutputsEmptyException(self):
		e = baseRoomDetectionBrain.OutputsEmptyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, [])
	
if __name__ == "__main__":
	unittest.main()