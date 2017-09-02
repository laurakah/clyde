import unittest
import simpleBrain
import baseBrain
import coord as c

isCollisionCalled = False
isCollisionValue = False
getOrientationCalled = False
getOrientationValue = None
setOrientationCalled = False
setOrientationValue = None
moveCalled = False
getNextPositionCalled = False
getNextPositionValue = None
getMovementDirectionValue = None
withinMapCalled = False
withinMapValue = None
expandMapCalled = False

def fakeCallback():
	return
	
def fakeIsCollision():
	global isCollisionCalled
	global isCollisionValue
	isCollisionCalled = True
	return isCollisionValue
	
def fakeGetOrientation():
	global getOrientationCalled
	global getOrientationValue
	getOrientationCalled = True
	return getOrientationValue
	
def fakeSetOrientation(ori):
	global setOrientationCalled
	global setOrientationValue
	setOrientationCalled = True
	setOrientationValue = ori
	
def fakeMove():
	global moveCalled
	moveCalled = True
	
def fakeGetNextPosition(pos, ori, direction):
	global getNextPositionCalled
	global getNextPositionValue
	getNextPositionCalled = True
	return getNextPositionValue
	
def fakeGetMovementDirection():
	global getMovementDirectionValue
	return getMovementDirectionValue
	
def fakeWithinMap(x, y):
	global withinMapCalled
	global withinMapValue
	withinMapCalled = True
	return withinMapValue
	
def fakeExpandMap(h, v, appV, appH):
	global expandMapCalled
	expandMapCalled = True
	
def fakeSetLocation(x, y, loc):
	return



class SimpleBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
		self.b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
		
	def testSimpleBrain_extendsBaseBrain(self):
		self.assertEqual(True, issubclass(simpleBrain.SimpleBrain, baseBrain.BaseBrain))
		
	def testIsFinished_returnsBoolean(self):
		self.assertEqual(True, type(self.b.isFinished()) is bool)
		
	# tests for step calling inputs and outputs
		
	def testStep_callsIsCollision(self):
		global isCollisionCalled
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		isCollisionCalled = False
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_UP
		getMovementDirectionValue = 1
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, isCollisionCalled)
		
	def testStep_callsGetOrientation_whenIsCollisionIsTrue(self):
		global isCollisionValue
		global getOrientationCalled
		global getOrientationValue
		isCollisionValue = True
		getOrientationCalled = False
		getOrientationValue = self.b.ORIENTATION_UP
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, getOrientationCalled)
		
	def testStep_callsSetOrientation_whenIsCollisionIsTrue(self):
		global isCollisionValue
		global setOrientationCalled
		global getOrientationValue
		isCollisionValue = True
		setOrientationCalled = False
		getOrientationValue = self.b.ORIENTATION_UP
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, setOrientationCalled)
		
	def testStep_doesNotCallSetOrientation_whenIsCollisionIsFalse(self):
		global isCollisionValue
		global setOrientationCalled
		global getMovementDirectionValue
		isCollisionValue = False
		setOrientationCalled = False
		getMovementDirectionValue = 1
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(False, setOrientationCalled)
		
	# tests for movement behaviour
		
	def testStep_setOrientation_changesOrientationClockwise(self):
		global getOrientationValue
		global setOrientationValue
		global isCollisionValue
		isCollisionValue = True
		getOrientationValue = self.b.ORIENTATION_UP
		setOrientationValue = None
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(self.b.ORIENTATION_RIGHT, setOrientationValue)
		
	def testStep_setOrientation_setsZeroWhenOrientationWasThree(self):
		global getOrientationValue
		global setOrientationValue
		global isCollisionValue
		isCollisionValue = True
		getOrientationValue = self.b.ORIENTATION_LEFT
		setOrientationValue = None
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(self.b.ORIENTATION_UP, setOrientationValue)
		
	def testStep_callsMoveWhenIsCollisionIsFalse(self):
		global moveCalled
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		moveCalled = False
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_UP
		getMovementDirectionValue = 1
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["move"] = fakeMove
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, moveCalled)
		
	def testStep_doesNotCallMoveWhenIsCollisionIsTrue(self):
		global moveCalled
		global isCollisionValue
		global getOrientationValue
		moveCalled = False
		isCollisionValue = True
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["move"] = fakeMove
		self.outputs["setOrientation"] = fakeSetOrientation
		b = simpleBrain.SimpleBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(False, moveCalled)
		
	# tests for brain map manipulation
		
	def testStep_appendsMapWithFrontFacingLocationVertically(self):
		global getOrientationValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_UP			#orientation up
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.b.step()
		self.assertEqual(2, self.b.getBrainMap().getHeight())
		
	def testStep_appendsMapWithFrontFacingLocationHorizontally(self):
		global getOrientationValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_RIGHT			#orientation right
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.b.step()
		self.assertEqual(2, len(self.b.getBrainMap().getMapArray()[0]))
		
	def testStep_appendsMapWithFrontFacingLocationOnCollisionVertically(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_UP
		isCollisionValue = True
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionVertically(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_UP
		isCollisionValue = False
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionVerticallyByFour(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_UP
		isCollisionValue = False
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.b.step()
		self.b.step()
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 5))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionHorizontallyByFour(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_RIGHT
		isCollisionValue = False
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.b.step()
		self.b.step()
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(5, 1))
		
	def testStep_appendsMapWithFrontFacingLocationOnCollisionHorizontally(self):
		global getOrientationValue
		global isCollisionValue
		getOrientationValue = self.b.ORIENTATION_RIGHT
		isCollisionValue = True
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionHorizontally(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_RIGHT
		isCollisionValue = False
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_prependsMapWithFrontFacingLocationOnCollisionHorizontallyWithOrientationLeft(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_LEFT
		isCollisionValue = True
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(3, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_prependsMapWithFrontFacingLocationOnNonCollisionHorizontallyWithOrientationLeft(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_LEFT
		isCollisionValue = False
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(3, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_prependsMapWithFrontFacingLocationOnCollisionVerticallyWithOrientationDown(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_DOWN
		isCollisionValue = True
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(3, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_prependsMapWithFrontFacingLocationOnNonCollisionVerticallyWithOrientationDown(self):
		global getOrientationValue
		global isCollisionValue
		global getMovementDirectionValue
		getOrientationValue = self.b.ORIENTATION_DOWN
		isCollisionValue = False
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(3, self.b.getBrainMap().getLocation(1, 2))
		
	# tests for brain internal attributes
		
	def testStep_storesLastOrientationOnCollision(self):
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		isCollisionValue = True
		getOrientationValue = self.b.ORIENTATION_DOWN
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(getOrientationValue, self.b.getLastOrientation())
		
	def testStep_storesLastOrientationOnNoneCollision(self):
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_DOWN
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(None, self.b.getLastOrientation())
	
	def testGetLastOrientation_isNoneOnInit(self):
		lastOri = self.b.getLastOrientation()
		self.assertEqual(None, lastOri)
		
	def testGetLastOrientationChange_isNoneOnInit(self):
		lastOriChange = self.b.getLastOrientationChange()
		self.assertEqual(None, lastOriChange)
		
	def testGetLastOrientationChange_isZeroWhenLastTurnWasLeft_closingDirectionCircle(self):		#counter clockwise
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_LEFT
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.lastOri = self.b.ORIENTATION_UP			#up
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.COUNTER_CLOCKWISE, ch)		#0 = symbol for counter clockwise orientation change
		
	def testGetLastOrientationChange_isZeroWhenLastTurnWasLeft(self):		#counter clockwise
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_RIGHT
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.lastOri = self.b.ORIENTATION_DOWN
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.COUNTER_CLOCKWISE, ch)		#0 = symbol for counter clockwise orientation change
		
	def testGetLastOrientationChange_isOneWhenLastTurnWasRight(self):		#clockwise
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_RIGHT
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.lastOri = self.b.ORIENTATION_UP			#up
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.CLOCKWISE, ch)		#1 = symbol for counter clockwise orientation change
		
	def testGetLastOrientationChange_isZeroWhenLastTurnWasRight_closingDirectionCircle(self):		#clockwise
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_UP
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.lastOri = self.b.ORIENTATION_LEFT
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.CLOCKWISE, ch)		#1 = symbol for counter clockwise orientation change
		
	def testGetNextOrientation_returnsOneWhenOrientationWasZeroAndCwArgIsTrue(self):
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_UP
		self.inputs["getOrientation"] = fakeGetOrientation
		nextOri = self.b.getNextOrientation(True)				#True == clockwise
		self.assertEqual(self.b.ORIENTATION_RIGHT, nextOri)
		
	def testGetNextOrientation_returnsOneWhenOrientationWasTwoAndCwArgIsFalse(self):
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_DOWN
		self.inputs["getOrientation"] = fakeGetOrientation
		nextOri = self.b.getNextOrientation(False)				#False == counter clockwise
		self.assertEqual(self.b.ORIENTATION_RIGHT, nextOri)
		
	def testGetNextOrientation_returnsZeroWhenOrientationWasThreeAndCwArgIsTrue(self):
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_LEFT
		self.inputs["getOrientation"] = fakeGetOrientation
		nextOri = self.b.getNextOrientation(True)				#True == clockwise
		self.assertEqual(self.b.ORIENTATION_UP, nextOri)
		
	def testGetNextOrientation_returnsThreeWhenOrientationWasZeroAndCwArgIsFalse(self):
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_UP
		self.inputs["getOrientation"] = fakeGetOrientation
		nextOri = self.b.getNextOrientation(False)				#False == counter clockwise
		self.assertEqual(self.b.ORIENTATION_LEFT, nextOri)
		
	def testStep_alternatelyChangesOrientationOnCollisions(self):
		global getOrientationValue
		global isCollisionValue
		global setOrientationValue
		getOrientationValue = self.b.ORIENTATION_UP
		setOrientationValue = None
		isCollisionValue = True
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(self.b.ORIENTATION_RIGHT, setOrientationValue)
		getOrientationValue = setOrientationValue
		self.b.step()
		self.assertEqual(self.b.ORIENTATION_UP, setOrientationValue)
		
	def testStep_callsGetNextPosition(self):
		global getNextPositionCalled
		getNextPositionCalled = False
		self.b.getNextPosition = fakeGetNextPosition
		self.b.step()
		self.assertEqual(True, getNextPositionCalled)
		
	def testStep_setsPosToNextPositionValue(self):
		global getNextPositionValue
		getNextPositionValue = c.Coordinate(66, 88)
		self.b.getNextPosition = fakeGetNextPosition
		self.b.step()
		self.assertEqual(getNextPositionValue, self.b._getPosition())
		
	def testStep_callsGetNextPositionOnlyWhenNoCollision(self):
		global getNextPositionCalled
		global isCollisionValue
		global getOrientationValue
		getNextPositionCalled = False
		isCollisionValue = True
		getOrientationValue = self.b.ORIENTATION_UP
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.b.getNextPosition = fakeGetNextPosition
		beforePos = self.b._getPosition()
		self.b.step()
		afterPos = self.b._getPosition()
		self.assertEqual(False, getNextPositionCalled)
		self.assertEqual(beforePos, afterPos)
		
	def testStep_doesNotChangePositionBecausePrependingMapVertically(self):
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_DOWN
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		beforePos = self.b._getPosition()
		self.b.step()
		afterPos = self.b._getPosition()
		self.assertEqual(beforePos, afterPos)
		
	def testStep_doesNotChangePositionBecausePrependingMapHorizontally(self):
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_LEFT
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		beforePos = self.b._getPosition()
		self.b.step()
		afterPos = self.b._getPosition()
		self.assertEqual(beforePos, afterPos)
		
	def testStep_callsWithinMap(self):
		global withinMapCalled
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		withinMapCalled = False
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_UP
		getMovementDirectionValue = 1
		self.b.mObj.withinMap = fakeWithinMap
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(True, withinMapCalled)
		
	def testStep_callsExpandMapWhenCoordinatesAreNotWithinMapArray(self):
		global expandMapCalled
		global withinMapValue
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		expandMapCalled = False
		withinMapValue = False
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_UP
		getMovementDirectionValue = 1
		self.b.mObj.withinMap = fakeWithinMap
		self.b.mObj.expandMap = fakeExpandMap
		self.b.mObj.setLocation = fakeSetLocation
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(True, expandMapCalled)
		
	def testStep_doesNotCallExpandMapWhenCoordinatesAreWithinMapArray(self):
		global expandMapCalled
		global withinMapValue
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		expandMapCalled = False
		withinMapValue = True
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_UP
		getMovementDirectionValue = 1
		self.b.mObj.withinMap = fakeWithinMap
		self.b.mObj.expandMap = fakeExpandMap
		self.b.mObj.setLocation = fakeSetLocation
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(False, expandMapCalled)
		
	def testGetLastPosition_returnsPreviousPositionAfterMoving(self):
		global isCollisionValue
		global getOrientationValue
		global getMovementDirectionValue
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_UP
		getMovementDirectionValue = 1
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getMovementDirection"] = fakeGetMovementDirection
		self.b.step()
 		self.assertEqual(c.Coordinate(1, 1), self.b._getLastPosition())


if __name__ == "__main__":
	unittest.main()