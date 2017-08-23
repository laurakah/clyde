import unittest
import theseusBrain
import baseBrain

isCollisionCalled = False
isCollisionValue = False
getOrientationCalled = False
getOrientationValue = None
setOrientationCalled = False
setOrientationValue = None
moveCalled = False

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
		
	def testStep_callsIsCollision(self):
		global isCollisionCalled
		global isCollisionValue
		isCollisionCalled = False
		isCollisionValue = False
		self.inputs["isCollision"] = fakeIsCollision
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
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
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
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
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(True, setOrientationCalled)
		
	def testStep_doesNotCallSetOrientation_whenIsCollisionIsFalse(self):
		global isCollisionValue
		global setOrientationCalled
		isCollisionValue = False
		setOrientationCalled = False
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(False, setOrientationCalled)
		
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
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
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
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(self.b.ORIENTATION_UP, setOrientationValue)
		
	def testStep_callsMoveWhenIsCollisionIsFalse(self):
		global moveCalled
		global isCollisionValue
		moveCalled = False
		isCollisionValue = False
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["move"] = fakeMove
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
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
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(False, moveCalled)
		
	def testStep_appendsMapWithFrontFacingLocationVertically(self):
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_UP			#orientation up
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.step()
		self.assertEqual(self.b.ORIENTATION_DOWN, self.b.getBrainMap().getHeight())
		
	def testStep_appendsMapWithFrontFacingLocationHorizontally(self):
		global getOrientationValue
		getOrientationValue = self.b.ORIENTATION_RIGHT			#orientation right
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.step()
		self.assertEqual(self.b.ORIENTATION_DOWN, len(self.b.getBrainMap().getMapArray()[0]))
		
	def testStep_appendsMapWithFrontFacingLocationOnCollisionVertically(self):
		global getOrientationValue
		global isCollisionValue
		getOrientationValue = self.b.ORIENTATION_UP
		isCollisionValue = True
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(self.b.ORIENTATION_RIGHT, self.b.getBrainMap().getLocation(1, 2))
		
	def testStep_appendsMapWithFrontFacingLocationOnNonCollisionVertically(self):
		global getOrientationValue
		global isCollisionValue
		getOrientationValue = self.b.ORIENTATION_UP
		isCollisionValue = False
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(1, 2))
		
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
		getOrientationValue = self.b.ORIENTATION_RIGHT
		isCollisionValue = False
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(0, self.b.getBrainMap().getLocation(2, 1))
		
	def testStep_storesLastOrientation(self):
		global isCollisionValue
		global getOrientationValue
		isCollisionValue = True
		getOrientationValue = self.b.ORIENTATION_DOWN
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
		self.outputs["setOrientation"] = fakeSetOrientation
		self.b.step()
		self.assertEqual(getOrientationValue, self.b.getLastOrientation())
		
	def testStep_storesLastOrientation(self):
		global isCollisionValue
		global getOrientationValue
		isCollisionValue = False
		getOrientationValue = self.b.ORIENTATION_DOWN
		self.inputs["getOrientation"] = fakeGetOrientation
		self.inputs["isCollision"] = fakeIsCollision
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
	

if __name__ == "__main__":
	unittest.main()