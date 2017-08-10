import unittest
import baseRoomDetectionBrain

def fakeCallback():
	return


class BaseRoomDetectionBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.cls = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
		self.b = baseRoomDetectionBrain.BaseRoomDetectionBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
		
	def assertRaisesExceptionWithMessage(self, e, cls, args, msg):
		with self.assertRaises(e) as ex:
			b = cls(args[0], args[1])
		self.assertEqual(msg, ex.exception.message)
		
	def testInit_raisesExceptionWhenInputsIsNotADict(self):
		e = baseRoomDetectionBrain.NotADictException
		args = [[0], self.outputs]
		msg = "inputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsIsNotADict(self):
		e = baseRoomDetectionBrain.NotADictException
		args = [self.inputs, [0]]
		msg = "outputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenInputsIsEmpty(self):
		e = baseRoomDetectionBrain.IsEmptyException
		args = [{}, self.inputs]
		msg = "inputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsIsEmpty(self):
		e = baseRoomDetectionBrain.IsEmptyException
		args = [self.outputs, {}]
		msg = "outputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenInputsHasNoIsSomethingCollisionKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		args = [{"foo": None}, self.outputs]
		msg = "inputs: isCollision"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNoExceptionWhenInputsHasIsSomethingCollisionKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		c = baseRoomDetectionBrain.BaseRoomDetectionBrain
		inputs = {"isSomethingCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
# 		self.assertRaises(e, c, inputs, self.outputs)
		#try:
		baseRoomDetectionBrain.BaseRoomDetectionBrain(inputs, self.outputs)
		#except:
		#	self.assertTrue(False)
		#	print "X!" * 70
		self.assertTrue(True)
		
	def testInit_raisesExceptionWhenInputsHasNoGetOrientationKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		args = [{"isCollision": None}, self.outputs]
		msg = "inputs: getOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenInputsHasNoGetMovementDirectionKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		args = [{"isCollision": None, "getOrientation": None}, self.outputs]
		msg = "inputs: getMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsHasNoSetOrientationKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		args = [self.inputs, {"bar": None}]
		msg = "outputs: setOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsHasNoSetMovementDirectionKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		args = [self.inputs, {"setOrientation": None}]
		msg = "outputs: setMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsHasNoMoveKey(self):
		e = baseRoomDetectionBrain.IsNotAKeyException
		args = [self.inputs, {"setOrientation": None, "setMovementDirection": None}]
		msg = "outputs: move"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenIsSomethingCollisionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		args = [{"isCollision": None, "getOrientation": None, "getMovementDirection": None}, self. outputs]
		msg = "inputs: isCollision"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
		#TODO: fix me!
		
	def testInit_raisesNotAFunctionExceptionWhenGetOrientationIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		args = [{"isCollision": fakeCallback, "getOrientation": None, "getMovementDirection": None}, self. outputs]
		msg = "inputs: getOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenGetMovementDirectionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		args = [{"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": None}, self. outputs]
		msg = "inputs: getMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenSetOrientationIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		args = [self.inputs, {"setOrientation": None, "setMovementDirection": None, "move": None}]
		msg = "outputs: setOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
			
	def testInit_raisesNotAFunctionExceptionWhenSetMovementDirectionIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		args = [self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": None, "move": None}]
		msg = "outputs: setMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenMoveIsNotAFunction(self):
		e = baseRoomDetectionBrain.NotAFunctionException
		args = [self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": None}]
		msg = "outputs: move"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
	
	def testGetBrainMap_returnsArray(self):
		self.assertIsInstance(self.b.getBrainMap(), list)
		
	def testIsFinished_returnsBoolean(self):
		self.assertIsInstance(self.b.isFinished(), bool)
		
	def testClass_hasStepMethod(self):
		self.assertEqual(True, "step" in dir(self.b))
	
if __name__ == "__main__":
	unittest.main()