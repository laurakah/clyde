import unittest
import baseBrain
import gameMap
import coord as c

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
		
	
# helper
		
	def assertRaisesExceptionWithMessage(self, e, args, msg):
		cls = self.cls
		with self.assertRaises(e) as ex:
			b = cls(args[0], args[1])
		self.assertEqual(msg, ex.exception.message)
		
	
# tests for init
		
	def testInit_raisesExceptionWhenInputsIsNotADict(self):
		e = baseBrain.NotADictException
		args = [[0], self.outputs]
		msg = "inputs"
		self.assertRaisesExceptionWithMessage(e, args, msg)
		
	def testInit_raisesExceptionWhenOutputsIsNotADict(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotADictException, [self.inputs, [0]], "outputs")
		
	def testInit_raisesExceptionWhenInputsIsEmpty(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsEmptyException, [{}, self.inputs], "inputs")
		
	def testInit_raisesExceptionWhenOutputsIsEmpty(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsEmptyException, [self.outputs, {}], "outputs")
		
	def testInit_raisesExceptionWhenInputsHasNoIsSomethingCollisionKey(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsNotAKeyException, [{"foo": None}, self.outputs], "inputs: isCollision")
		
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
		self.assertRaisesExceptionWithMessage(baseBrain.IsNotAKeyException, [{"isCollision": None}, self.outputs], "inputs: getOrientation")
		
	def testInit_raisesExceptionWhenInputsHasNoGetMovementDirectionKey(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsNotAKeyException, [{"isCollision": None, "getOrientation": None}, self.outputs], "inputs: getMovementDirection")
		
	def testInit_raisesExceptionWhenOutputsHasNoSetOrientationKey(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsNotAKeyException, [self.inputs, {"bar": None}], "outputs: setOrientation")
		
	def testInit_raisesExceptionWhenOutputsHasNoSetMovementDirectionKey(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsNotAKeyException, [self.inputs, {"setOrientation": None}], "outputs: setMovementDirection")
		
	def testInit_raisesExceptionWhenOutputsHasNoMoveKey(self):
		self.assertRaisesExceptionWithMessage(baseBrain.IsNotAKeyException, [self.inputs, {"setOrientation": None, "setMovementDirection": None}], "outputs: move")
		
	def testInit_raisesNotAFunctionExceptionWhenIsSomethingCollisionIsNotAFunction(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotAFunctionException, [{"isCollision": None, "getOrientation": None, "getMovementDirection": None}, self. outputs], "inputs: isCollision")
		
	#TODO: fix me!	
	def testInit_raisesNotAFunctionExceptionWhenGetOrientationIsNotAFunction(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotAFunctionException, [{"isCollision": fakeCallback, "getOrientation": None, "getMovementDirection": None}, self. outputs], "inputs: getOrientation")
		
	def testInit_raisesNotAFunctionExceptionWhenGetMovementDirectionIsNotAFunction(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotAFunctionException, [{"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": None}, self. outputs], "inputs: getMovementDirection")
		
	def testInit_raisesNotAFunctionExceptionWhenSetOrientationIsNotAFunction(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotAFunctionException, [self.inputs, {"setOrientation": None, "setMovementDirection": None, "move": None}], "outputs: setOrientation")
			
	def testInit_raisesNotAFunctionExceptionWhenSetMovementDirectionIsNotAFunction(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotAFunctionException, [self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": None, "move": None}], "outputs: setMovementDirection")
		
	def testInit_raisesNotAFunctionExceptionWhenMoveIsNotAFunction(self):
		self.assertRaisesExceptionWithMessage(baseBrain.NotAFunctionException, [self.inputs, {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": None}], "outputs: move")
		
	def testInit_finishedIsFalse(self):
		self.assertEqual(False, self.b.finished)
	
	def testInit_storesInputs(self):
		self.assertEqual(self.inputs, self.b.inputs)
		
	def testInit_storesOutputs(self):
		self.assertEqual(self.outputs, self.b.outputs)
		
	def testInit_hasStartLocation(self):
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 1))
		
	def testInit_hasBrainStartPositionOneOne(self):
		self.assertEqual(c.Coordinate(1, 1), self.b._getPosition())
		
	def testInit_stepLogIsEmpty(self):
		self.assertEqual(0, len(self.b._getStepLog()))
		
	def testInit_hasStartPositionOneOne(self):
		self.assertEqual(c.Coordinate(1, 1), self.b._getStartPosition())
		
	def testInit_hasFirstCollisionPos(self):
		self.assertEqual(None, self.b._getFirstCollisionPos())
		
	def testGetStartPosition_returnsCopy(self):
		pos = self.b._getStartPosition()
		pos.x = 686
		self.assertNotEqual(pos, self.b._getStartPosition())
		
	def testGetStepLog_returnsCopy(self):
		log = self.b._getStepLog()
		log.append("76")
		self.assertNotEqual(log, self.b._getStepLog())
		
	def testGetPosition_returnsCopy(self):
		pos = self.b._getPosition()
		pos.x = 686
		self.assertNotEqual(pos, self.b._getPosition())
		
	def testGetLastPosition_isNoneOnInit(self):
		self.assertEqual(None, self.b._getLastPosition())
		
	def testGetLastPosition_returnsCopy(self):
		self.b.lastPos = c.Coordinate(5, 5)
		pos = self.b._getLastPosition()
		pos.x = 686
		self.assertNotEqual(pos, self.b._getLastPosition())
		
	def testGetNextPosition_doesNotChangePosArg(self):
		pos = c.Coordinate(7, 7)
		self.b.getNextPosition(pos, 1, 1)
		self.assertEqual(c.Coordinate(7, 7), pos)
		
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
			self.b.getNextPosition(c.Coordinate(1, 1), None, 1)
		self.assertEqual(msg, ex.exception.message)
		
	def testGetNextPosition_raisesExceptionWhenCalledWithNoneValueAsDirection(self):
		e = baseBrain.ArgumentIsNoneException
		msg = "Direction can't be None!"
		with self.assertRaises(e) as ex:
			self.b.getNextPosition(c.Coordinate(1, 1), 3, None)
		self.assertEqual(msg, ex.exception.message)
	
	def testGetBrainMap_returnsGameMapObject(self):
		self.assertIsInstance(self.b.getBrainMap(), gameMap.GameMap)
		
	def testGetBrainMap_returnsCopy(self):
		mObj = self.b.getBrainMap()
		mObj.mArr.append("76")
		self.assertNotEqual(mObj, self.b.getBrainMap())
		
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