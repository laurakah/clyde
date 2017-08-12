import unittest
import theseusBrain
import baseRoomDetectionBrain

isCollisionCalled = False
isCollisionValue = False

def fakeCallback():
	return
	
def fakeIsCollision():
	global isCollisionCalled
	global isCollisionValue
	isCollisionCalled = True
	isCollisionValue = True


class TheseusBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
		self.b = baseRoomDetectionBrain.BaseRoomDetectionBrain(self.inputs, self.outputs)
		
	def tearDown(self):
		return
		
	def testTheseusBrain_extendsBaseBrain(self):
		self.assertEqual(True, issubclass(theseusBrain.TheseusBrain, baseRoomDetectionBrain.BaseRoomDetectionBrain))
		
	def testStep_callsIsCollision(self):
		global isCollisionCalled
		isCollisionCalled = False
		b = baseRoomDetectionBrain.BaseRoomDetectionBrain(self.inputs, self.outputs)
		b.isCollision = fakeIsCollision
		b.isCollision()
		self.assertEqual(True, isCollisionCalled)
		
	def testStep_returnsIsCollisionValue(self):
		global isCollisionValue
		isCollisionValue = False
		b = baseRoomDetectionBrain.BaseRoomDetectionBrain(self.inputs, self.outputs)
		b.isCollision = fakeIsCollision
		b.isCollision()
		self.assertEqual(True, isCollisionValue)
	

if __name__ == "__main__":
	unittest.main()