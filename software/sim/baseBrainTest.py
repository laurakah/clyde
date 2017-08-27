import unittest
import baseBrain
import gameMap

def fakeCallback():
	return


class BaseBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.cls = baseBrain.BaseBrain
		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
		self.b = baseBrain.BaseBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
		
	def assertRaisesExceptionWithMessage(self, e, cls, args, msg):
		with self.assertRaises(e) as ex:
			b = cls(args[0], args[1])
		self.assertEqual(msg, ex.exception.message)
		
	def testInit_raisesExceptionWhenInputsIsNotADict(self):
		e = baseBrain.NotADictException
		args = [[0], self.outputs]
		msg = "inputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsIsNotADict(self):
		e = baseBrain.NotADictException
		args = [self.inputs, [0]]
		msg = "outputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenInputsIsEmpty(self):
		e = baseBrain.IsEmptyException
		args = [{}, self.inputs]
		msg = "inputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsIsEmpty(self):
		e = baseBrain.IsEmptyException
		args = [self.outputs, {}]
		msg = "outputs"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenInputsHasNoIsSomethingCollisionKey(self):
		e = baseBrain.IsNotAKeyException
		args = [{"foo": None}, self.outputs]
		msg = "inputs: isCollision"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNoExceptionWhenInputsHasIsSomethingCollisionKey(self):
		e = baseBrain.IsNotAKeyException
		c = baseBrain.BaseBrain
		inputs = {"isSomethingCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
# 		self.assertRaises(e, c, inputs, self.outputs)
		#try:
		baseBrain.BaseBrain(inputs, self.outputs)
		#except:
		#	self.assertTrue(False)
		#	print "X!" * 70
		self.assertTrue(True)
		
	def testInit_raisesExceptionWhenInputsHasNoGetOrientationKey(self):
		e = baseBrain.IsNotAKeyException
		args = [{"isCollision": None}, self.outputs]
		msg = "inputs: getOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenInputsHasNoGetMovementDirectionKey(self):
		e = baseBrain.IsNotAKeyException
		args = [{"isCollision": None, "getOrientation": None}, self.outputs]
		msg = "inputs: getMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsHasNoSetOrientationKey(self):
		e = baseBrain.IsNotAKeyException
		args = [self.inputs, {"bar": None}]
		msg = "outputs: setOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsHasNoSetMovementDirectionKey(self):
		e = baseBrain.IsNotAKeyException
		args = [self.inputs, {"setOrientation": None}]
		msg = "outputs: setMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesExceptionWhenOutputsHasNoMoveKey(self):
		e = baseBrain.IsNotAKeyException
		args = [self.inputs, {"setOrientation": None, "setMovementDirection": None}]
		msg = "outputs: move"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenIsSomethingCollisionIsNotAFunction(self):
		e = baseBrain.NotAFunctionException
		args = [{"isCollision": None, "getOrientation": None, "getMovementDirection": None}, self. outputs]
		msg = "inputs: isCollision"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
		#TODO: fix me!
		
	def testInit_raisesNotAFunctionExceptionWhenGetOrientationIsNotAFunction(self):
		e = baseBrain.NotAFunctionException
		args = [{"isCollision": fakeCallback, "getOrientation": None, "getMovementDirection": None}, self. outputs]
		msg = "inputs: getOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenGetMovementDirectionIsNotAFunction(self):
		e = baseBrain.NotAFunctionException
		args = [{"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": None}, self. outputs]
		msg = "inputs: getMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenSetOrientationIsNotAFunction(self):
		e = baseBrain.NotAFunctionException
		args = [self.inputs, {"setOrientation": None, "setMovementDirection": None, "move": None}]
		msg = "outputs: setOrientation"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
			
	def testInit_raisesNotAFunctionExceptionWhenSetMovementDirectionIsNotAFunction(self):
		e = baseBrain.NotAFunctionException
		args = [self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": None, "move": None}]
		msg = "outputs: setMovementDirection"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
		
	def testInit_raisesNotAFunctionExceptionWhenMoveIsNotAFunction(self):
		e = baseBrain.NotAFunctionException
		args = [self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": None}]
		msg = "outputs: move"
		self.assertRaisesExceptionWithMessage(e, self.cls, args, msg)
	
	def testInit_storesInputs(self):
		self.assertEqual(self.inputs, self.b.inputs)
		
	def testInit_storesOutputs(self):
		self.assertEqual(self.outputs, self.b.outputs)
		
	def testInit_hasStartLocation(self):
		self.assertEqual(3, self.b.getBrainMap().getLocation(1, 1))
		
	def testInit_hasBrainStartPositionOneOne(self):
		self.assertEqual({"x": 1, "y": 1}, self.b._getPosition())
		
	def testGetPosition_returnsCopy(self):
		pos = self.b._getPosition()
		pos["x"] = 686
		self.assertNotEqual(pos, self.b._getPosition())
		
	def testGetNextPosition_raisesExceptionWhenCalledWithNoneValueAsPosition(self):
		e = baseBrain.ArgumentIsNoneException
		msg = "Position can't be None!"
		with self.assertRaises(e) as ex:
			self.b.getNextPosition(None, 3, 1)
		self.assertEqual(msg, ex.exception.message)
		
	def testGetNextPosition_raisesExceptionWhenCalledWithNoneValueAsOrientation(self):
		e = baseBrain.ArgumentIsNoneException
		msg = "Orientation can't be None!"
		with self.assertRaises(e) as ex:
			self.b.getNextPosition({"x": 1, "y": 1}, None, 1)
		self.assertEqual(msg, ex.exception.message)
		
	def testGetNextPosition_raisesExceptionWhenCalledWithNoneValueAsDirection(self):
		e = baseBrain.ArgumentIsNoneException
		msg = "Direction can't be None!"
		with self.assertRaises(e) as ex:
			self.b.getNextPosition({"x": 1, "y": 1}, 3, None)
		self.assertEqual(msg, ex.exception.message)
	
	def testGetBrainMap_returnsGameMapObject(self):
		self.assertIsInstance(self.b.getBrainMap(), gameMap.GameMap)
		
	def testIsFinished_raisesNotImplementedException(self):
		e = NotImplementedError
		with self.assertRaises(e) as ex:
			self.b.isFinished()
		
	def testClass_hasStepMethod(self):
		self.assertEqual(True, "step" in dir(self.b))
		
	def testStep_raisesNotImplementedException(self):
		e = NotImplementedError
		with self.assertRaises(e) as ex:
			self.b.step()
	
if __name__ == "__main__":
	unittest.main()