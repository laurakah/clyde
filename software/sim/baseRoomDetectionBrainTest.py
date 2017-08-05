import unittest
import baseRoomDetectionBrain

def fakeCallback():
	return


class BaseRoomDetectionBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
		self.b = baseRoomDetectionBrain.BaseRoomDetectionBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
		
	def testInit_raisesExceptionWhenInputsIsNotADict(self):
		e = baseRoomDetectionBrain.InputsNotADictException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, [0], self.outputs)
		
	def testInit_raisesExceptionWhenOutputsIsNotADict(self):
		e = baseRoomDetectionBrain.OutputsNotADictException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, [0])
		
	def testInit_raisesInputsEmptyException(self):
		e = baseRoomDetectionBrain.InputsEmptyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {}, self.outputs)
		
	def testInit_raisesOutputsEmptyException(self):
		e = baseRoomDetectionBrain.OutputsEmptyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {})
		
	def testInit_raisesInputsHasNoIsSomethingCollisionKeyException(self):
		e = baseRoomDetectionBrain.InputsHasNoIsSomethingCollisionKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {"foo": None}, self.outputs)
		
	def testInit_raisesNoExceptionWhenInputsHasIsSomethingCollisionKey(self):
		e = baseRoomDetectionBrain.InputsHasNoIsSomethingCollisionKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		inputs = {"isSomethingCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
# 		self.assertRaises(e, c, inputs, self.outputs)
		#try:
		baseRoomDetectionBrain.BaseRoomDetectionBrain(inputs, self.outputs)
		#except:
		#	self.assertTrue(False)
		#	print "X!" * 70
		self.assertTrue(True)
		
	def testInit_raisesInputsHasNoGetOrientationKeyException(self):
		e = baseRoomDetectionBrain.InputsHasNoGetOrientationKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {"isCollision": None}, self.outputs)
		
	def testInit_raisesInputsHasNoGetMovementDirectionKeyException(self):
		e = baseRoomDetectionBrain.InputsHasNoGetMovementDirectionKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {"isCollision": None, "getOrientation": None}, self.outputs)
		
	def testInit_raisesOutputsHasNoSetOrientationKeyException(self):
		e = baseRoomDetectionBrain.OutputsHasNoSetOrientationKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {"bar": None})
		
	def testInit_raisesOutputsHasNoSetMovementDirectionKeyException(self):
		e = baseRoomDetectionBrain.OutputsHasNoSetMovementDirectionKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {"setOrientation": None})
		
	def testInit_raisesOutputsHasNoMoveKeyException(self):
		e = baseRoomDetectionBrain.OutputsHasNoMoveKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {"setOrientation": None, "setMovementDirection": None})
		
	def testInit_raisesNotAFunctionExceptionWhenIsSomethingCollisionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {"isCollision": None, "getOrientation": None, "getMovementDirection": None}, self. outputs)
		
		#TODO: fix me!
		
	def testInit_raisesNotAFunctionExceptionWhenGetOrientationIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {"isCollision": fakeCallback, "getOrientation": None, "getMovementDirection": None}, self. outputs)
		
	def testInit_raisesNotAFunctionExceptionWhenGetMovementDirectionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": None}, self. outputs)
		
	def testInit_raisesNotAFunctionExceptionWhenSetOrientationIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {"setOrientation": None, "setMovementDirection": None, "move": None})
			
	def testInit_raisesNotAFunctionExceptionWhenSetMovementDirectionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": None, "move": None})
		
	def testInit_raisesNotAFunctionExceptionWhenMoveIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.assertRaises(e, c, self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": None})
	
	def testGetBrainMap_returnsArray(self):
		self.assertIsInstance(self.b.getBrainMap(), list)
		
	def testIsFinished_returnsBoolean(self):
		self.assertIsInstance(self.b.isFinished(), bool)
		
	def testClass_hasStepMethod(self):
		self.assertEqual(True, "step" in dir(self.b))
	
if __name__ == "__main__":
	unittest.main()