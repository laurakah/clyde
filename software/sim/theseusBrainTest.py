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
		getOrientationValue = 0
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
		getOrientationValue = 0
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
		getOrientationValue = 0
		setOrientationValue = None
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(1, setOrientationValue)
		
	def testStep_setOrientation_setsZeroWhenOrientationWasThree(self):
		global getOrientationValue
		global setOrientationValue
		global isCollisionValue
		isCollisionValue = True
		getOrientationValue = 3
		setOrientationValue = None
		self.inputs["isCollision"] = fakeIsCollision
		self.inputs["getOrientation"] = fakeGetOrientation
		self.outputs["setOrientation"] = fakeSetOrientation
		b = theseusBrain.TheseusBrain(self.inputs, self.outputs)
		b.step()
		self.assertEqual(0, setOrientationValue)
		
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
		getOrientationValue = 0			#orientation up
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.step()
		self.assertEqual(2, self.b.getBrainMap().getHeight())
		
	def testStep_appendsMapWithFrontFacingLocationHorizontally(self):
		global getOrientationValue
		getOrientationValue = 1			#orientation right
		self.inputs["getOrientation"] = fakeGetOrientation
		self.b.step()
		self.assertEqual(2, len(self.b.getBrainMap().getMapArray()[0]))
	

if __name__ == "__main__":
	unittest.main()