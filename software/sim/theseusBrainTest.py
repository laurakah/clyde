import unittest
import theseusBrain
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

def setupFakes(self, **kwargs):
	if "ori" in kwargs:
		global getOrientationValue
		getOrientationValue = kwargs["ori"]
		self.inputs["getOrientation"] = fakeGetOrientation
	if "collision" in kwargs:
		global isCollisionValue
		isCollisionValue = kwargs["collision"]
		self.inputs["isCollision"] = fakeIsCollision
	if "direction" in kwargs:
		global getMovementDirectionValue
		getMovementDirectionValue = kwargs["direction"]
		self.inputs["getMovementDirection"] = fakeGetMovementDirection


class TheseusBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
		self.b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
		
	def testTheseusBrain_extendsBaseBrain(self):
		self.assertEqual(True, issubclass(theseusBrain.TheseusBrain, baseBrain.BaseBrain))
		
	def testIsFinished_returnsBoolean(self):
		self.assertEqual(True, type(self.b.isFinished()) is bool)
		
	# tests for step calling inputs and outputs
		
	def testStep_callsIsCollision(self):
		global isCollisionCalled
		isCollisionCalled = False
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, isCollisionCalled)
		
	def testStep_callsGetOrientation_whenIsCollisionIsTrue(self):
		global getOrientationCalled
		getOrientationCalled = False
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = True, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, getOrientationCalled)
		
	def testStep_callsSetOrientation_whenIsCollisionIsTrue(self):
		global setOrientationCalled
		setOrientationCalled = False
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = True, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, setOrientationCalled)
		
	def testStep_doesNotCallSetOrientation_whenIsCollisionIsFalse(self):
		global setOrientationCalled
		setOrientationCalled = False
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(False, setOrientationCalled)
		
	# tests for movement behaviour
		
	def testStep_setOrientation_changesOrientationClockwise(self):
		global setOrientationValue
		setOrientationValue = None
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = True, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(self.b.ORIENTATION_RIGHT, setOrientationValue)
		
	def testStep_setOrientation_setsZeroWhenOrientationWasThree(self):
		global setOrientationValue
		setOrientationValue = None
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_LEFT, collision = True, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(self.b.ORIENTATION_UP, setOrientationValue)
		
	def testStep_callsMoveWhenIsCollisionIsFalse(self):
		global moveCalled
		moveCalled = False
		self.outputs["move"] = fakeMove
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, moveCalled)
		
	def testStep_doesNotCallMoveWhenIsCollisionIsTrue(self):
		global moveCalled
		moveCalled = False
		self.outputs["move"] = fakeMove
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = True, direction = self.b.DIRECTION_FOREWARD)
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(False, moveCalled)
		
	# tests for brain map manipulation
		
	def testStep_appendsMapWithFrontFacingLocationVertically(self):
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(2, self.b.getBrainMap().getHeight())
		
	def testStep_appendsMapWithFrontFacingLocationHorizontally(self):
		setupFakes(self, ori = self.b.ORIENTATION_RIGHT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(2, len(self.b.getBrainMap().getMapArray()[0]))
		
	def testStep_appendsMapWithFrontFacingLocationOnCollisionVertically(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = True, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionVertically(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionVerticallyByFour(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.b.step()
		self.b.step()
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 5))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionHorizontallyByFour(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_RIGHT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.b.step()
		self.b.step()
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(5, 1))
		
	def testStep_appendsMapWithFrontFacingLocationOnCollisionHorizontally(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_RIGHT, collision = True, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionHorizontally(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_RIGHT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_prependsMapWithFrontFacingLocationOnCollisionHorizontallyWithOrientationLeft(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_LEFT, collision = True, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(0, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_prependsMapWithFrontFacingLocationOnNonCollisionHorizontallyWithOrientationLeft(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_LEFT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(0, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_prependsMapWithFrontFacingLocationOnCollisionVerticallyWithOrientationDown(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_DOWN, collision = True, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(1, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_prependsMapWithFrontFacingLocationOnNonCollisionVerticallyWithOrientationDown(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_DOWN, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 1))
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 2))
		
	# tests for brain internal attributes
		
	def testStep_storesLastOrientationOnCollision(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_DOWN, collision = True, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(getOrientationValue, self.b.getLastOrientation())
		
	def testStep_storesLastOrientationOnNoneCollision(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_DOWN, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(None, self.b.getLastOrientation())
	
	def testGetLastOrientation_isNoneOnInit(self):
		lastOri = self.b.getLastOrientation()
		self.assertEqual(None, lastOri)
		
	def testGetLastOrientationChange_isNoneOnInit(self):
		lastOriChange = self.b.getLastOrientationChange()
		self.assertEqual(None, lastOriChange)
		
	def testGetLastOrientationChange_isZeroWhenLastTurnWasLeft_closingDirectionCircle(self):
		setupFakes(self, ori = self.b.ORIENTATION_LEFT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.lastOri = self.b.ORIENTATION_UP
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.COUNTER_CLOCKWISE, ch)
		
	def testGetLastOrientationChange_isZeroWhenLastTurnWasLeft(self):
		setupFakes(self, ori = self.b.ORIENTATION_RIGHT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.lastOri = self.b.ORIENTATION_DOWN
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.COUNTER_CLOCKWISE, ch)
		
	def testGetLastOrientationChange_isOneWhenLastTurnWasRight(self):
		setupFakes(self, ori = self.b.ORIENTATION_RIGHT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.lastOri = self.b.ORIENTATION_UP
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.CLOCKWISE, ch)
		
	def testGetLastOrientationChange_isZeroWhenLastTurnWasRight_closingDirectionCircle(self):
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.lastOri = self.b.ORIENTATION_LEFT
		ch = self.b.getLastOrientationChange()
		self.assertEqual(self.b.CLOCKWISE, ch)
		
	def testGetNextOrientation_returnsOneWhenOrientationWasZeroAndCwArgIsTrue(self):
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		nextOri = self.b.getNextOrientation(True)
		self.assertEqual(self.b.ORIENTATION_RIGHT, nextOri)
		
	def testGetNextOrientation_returnsOneWhenOrientationWasTwoAndCwArgIsFalse(self):
		setupFakes(self, ori = self.b.ORIENTATION_DOWN, collision = False, direction = self.b.DIRECTION_FOREWARD)
		nextOri = self.b.getNextOrientation(False)
		self.assertEqual(self.b.ORIENTATION_RIGHT, nextOri)
		
	def testGetNextOrientation_returnsZeroWhenOrientationWasThreeAndCwArgIsTrue(self):
		setupFakes(self, ori = self.b.ORIENTATION_LEFT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		nextOri = self.b.getNextOrientation(True)
		self.assertEqual(self.b.ORIENTATION_UP, nextOri)
		
	def testGetNextOrientation_returnsThreeWhenOrientationWasZeroAndCwArgIsFalse(self):
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		nextOri = self.b.getNextOrientation(False)
		self.assertEqual(self.b.ORIENTATION_LEFT, nextOri)
		
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
		getNextPositionCalled = False
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.getNextPosition = fakeGetNextPosition
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = True, direction = self.b.DIRECTION_FOREWARD)
		beforePos = self.b._getPosition()
		self.b.step()
		afterPos = self.b._getPosition()
		self.assertEqual(False, getNextPositionCalled)
		self.assertEqual(beforePos, afterPos)
		
	def testStep_doesNotChangePositionBecausePrependingMapVertically(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_DOWN, collision = False, direction = self.b.DIRECTION_FOREWARD)
		beforePos = self.b._getPosition()
		self.b.step()
		afterPos = self.b._getPosition()
		self.assertEqual(beforePos, afterPos)
		
	def testStep_doesNotChangePositionBecausePrependingMapHorizontally(self):
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_LEFT, collision = False, direction = self.b.DIRECTION_FOREWARD)
		beforePos = self.b._getPosition()
		self.b.step()
		afterPos = self.b._getPosition()
		self.assertEqual(beforePos, afterPos)
		
	def testStep_callsWithinMap(self):
		global withinMapCalled
		withinMapCalled = False
		self.b.mObj.withinMap = fakeWithinMap
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(True, withinMapCalled)
		
	def testStep_callsExpandMapWhenCoordinatesAreNotWithinMapArray(self):
		global expandMapCalled
		global withinMapValue
		expandMapCalled = False
		withinMapValue = False
		self.b.mObj.withinMap = fakeWithinMap
		self.b.mObj.expandMap = fakeExpandMap
		self.b.mObj.setLocation = fakeSetLocation
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(True, expandMapCalled)
		
	def testStep_doesNotCallExpandMapWhenCoordinatesAreWithinMapArray(self):
		global expandMapCalled
		global withinMapValue
		expandMapCalled = False
		withinMapValue = True
		self.b.mObj.withinMap = fakeWithinMap
		self.b.mObj.expandMap = fakeExpandMap
		self.b.mObj.setLocation = fakeSetLocation
		self.outputs["setOrientation"] = fakeSetOrientation
		setupFakes(self, ori = self.b.ORIENTATION_UP, collision = False, direction = self.b.DIRECTION_FOREWARD)
		self.b.step()
		self.assertEqual(False, expandMapCalled)
	

if __name__ == "__main__":
	unittest.main()