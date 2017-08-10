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
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls([0], self.outputs)
		self.assertEqual("inputs", ex.exception.message)
		
	def testInit_raisesExceptionWhenOutputsIsNotADict(self):
		e = baseRoomDetectionBrain.OutputsNotADictException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, [0])
		self.assertEqual("outputs", ex.exception.message)
		
	def testInit_raisesInputsEmptyException(self):
		e = baseRoomDetectionBrain.InputsEmptyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({}, self.inputs)
		self.assertEqual("inputs", ex.exception.message)
		
	def testInit_raisesOutputsEmptyException(self):
		e = baseRoomDetectionBrain.OutputsEmptyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.outputs, {})
		self.assertEqual("outputs", ex.exception.message)
		
	def testInit_raisesInputsHasNoIsSomethingCollisionKeyException(self):
		e = baseRoomDetectionBrain.InputsHasNoIsSomethingCollisionKeyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({"foo": None}, self.outputs)
		self.assertEqual("inputs", ex.exception.message)
		
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
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({"isCollision": None}, self.outputs)
		self.assertEqual("inputs: getOrientation", ex.exception.message)
		
	def testInit_raisesInputsHasNoGetMovementDirectionKeyException(self):
		e = baseRoomDetectionBrain.InputsHasNoGetMovementDirectionKeyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({"isCollision": None, "getOrientation": None}, self.outputs)
		self.assertEqual("inputs: getMovementDirection", ex.exception.message)
		
	def testInit_raisesOutputsHasNoSetOrientationKeyException(self):
		e = baseRoomDetectionBrain.OutputsHasNoSetOrientationKeyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, {"bar": None})
		self.assertEqual("outputs: setOrientation", ex.exception.message)
		
	def testInit_raisesOutputsHasNoSetMovementDirectionKeyException(self):
		e = baseRoomDetectionBrain.OutputsHasNoSetMovementDirectionKeyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, {"setOrientation": None})
		self.assertEqual("outputs: setMovementDirection", ex.exception.message)
		
	def testInit_raisesOutputsHasNoMoveKeyException(self):
		e = baseRoomDetectionBrain.OutputsHasNoMoveKeyException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, {"setOrientation": None, "setMovementDirection": None})
		self.assertEqual("outputs: move", ex.exception.message)
		
	def testInit_raisesNotAFunctionExceptionWhenIsSomethingCollisionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({"isCollision": None, "getOrientation": None, "getMovementDirection": None}, self. outputs)
		self.assertEqual("inputs: isCollision", ex.exception.message)
		
		#TODO: fix me!
		
	def testInit_raisesNotAFunctionExceptionWhenGetOrientationIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({"isCollision": fakeCallback, "getOrientation": None, "getMovementDirection": None}, self. outputs)
		self.assertEqual("inputs: getOrientation", ex.exception.message)
		
	def testInit_raisesNotAFunctionExceptionWhenGetMovementDirectionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls({"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": None}, self. outputs)
		self.assertEqual("inputs: getMovementDirection", ex.exception.message)
		
	def testInit_raisesNotAFunctionExceptionWhenSetOrientationIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, {"setOrientation": None, "setMovementDirection": None, "move": None})
		self.assertEqual("outputs: setOrientation", ex.exception.message)
			
	def testInit_raisesNotAFunctionExceptionWhenSetMovementDirectionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": None, "move": None})
		self.assertEqual("outputs: setMovementDirection", ex.exception.message)
		
	def testInit_raisesNotAFunctionExceptionWhenMoveIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		with self.assertRaises(e) as ex:
			b = cls(self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": None})
		self.assertEqual("outputs: move", ex.exception.message)
	
	def testGetBrainMap_returnsArray(self):
		self.assertIsInstance(self.b.getBrainMap(), list)
		
	def testIsFinished_returnsBoolean(self):
		self.assertIsInstance(self.b.isFinished(), bool)
		
	def testClass_hasStepMethod(self):
		self.assertEqual(True, "step" in dir(self.b))
	
if __name__ == "__main__":
	unittest.main()