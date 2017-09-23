import unittest
import player
import dullBrain
import gameMap
import baseBrain as bb
import coord as c

brainStepCalled = False
brainIsFinishedCalled = False
brainIsFinishedValue = False
brainGetMapCalled = False
brainGetMapValue = None

def fakeBrainStep():
	global brainStepCalled
	brainStepCalled = True
	
def fakeBrainIsFinished():
	global brainIsFinishedCalled
	global brainIsFinishedValue
	brainIsFinishedCalled = True
	return brainIsFinishedValue
	
def fakeBrainGetMap():
	global brainGetMapCalled
	global brainGetMapValue
	brainGetMapCalled = True
	return brainGetMapValue



class PlayerTestCase(unittest.TestCase):
	
	def setUp(self):
		self.brainClass = dullBrain.DullBrain
		self.mapFile = "maps/test-room1-box.txt"
		self.mObj = gameMap.GameMap()
		self.mObj.loadMapFile(self.mapFile)
		self.pos = c.Coordinate(3, 3)
		self.p = player.Player(self.brainClass, self.mObj, self.pos)
		
	def tearDown(self):
		return

	def testInit_raisesException_whenGameMapNotOfTypeGameMap(self):
		e = player.InvalidTypeException
		cls = player.Player
		mArr = []
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, mArr, self.pos)
		self.assertEqual("gameMap not of type gameMap.GameMap!", ex.exception.message)
		
	def testInit_playerPosition_isUserSpecified(self):
		pos = c.Coordinate(5, 4)
		p2 = player.Player(self.brainClass, self.mObj, pos)
		self.assertEqual(pos, p2.getPosition())
		
		
# helper
	
	def assertRaisesExceptionWithMessage(self, position, exc, msg):
		e = exc
		cls = player.Player
		pos = position
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.mObj, pos)
		self.assertEqual(msg, ex.exception.message)
		
	def testSetPosition_changesPosition(self):
		pos = c.Coordinate(7, 6)
		self.p.setPosition(pos)
		self.assertEqual(pos, self.p.getPosition())
		
	def testSetPosition_raisesInvalidTypeException_whenPosIsNone(self):
		self.assertRaisesExceptionWithMessage(None, player.InvalidTypeException, "pos can't be None!")
		
	def testSetPosition_raisesInvalidTypeException_whenPosIsNotOfTypeCoordinate(self):
		self.assertRaisesExceptionWithMessage(45, player.InvalidTypeException, "pos must be of type Coordinate!")
			
	def testSetPosition_raisesExceptionInvalidCoordinateForY(self):
		self.assertRaisesExceptionWithMessage(c.Coordinate(3, 0), player.InvalidCoordinateException, "y can't be zero!")
		
	def testSetPosition_raisesExceptionInvalidCoordinateForX(self):
		self.assertRaisesExceptionWithMessage(c.Coordinate(0, 3), player.InvalidCoordinateException, "x can't be zero!")
		
	def testSetPosition_raisesExceptionInvalidCoordinateForMaxYPlusOne(self):
		self.assertRaisesExceptionWithMessage(c.Coordinate(3, 8), player.InvalidCoordinateException, "y (%d) can't be outside of map!" % 8)
		
	def testSetPosition_raisesExceptionInvalidCoordinateForMaxXPlusOne(self):
		self.assertRaisesExceptionWithMessage(c.Coordinate(17, 3), player.InvalidCoordinateException, "x (%d) can't be outside of map!" % 17)
		
	def testGetPosition_returnsCopy(self):
		p1 = self.p.getPosition()
		p1.x = 100
		p2 = self.p.getPosition()
		self.assertNotEqual(p1, p2)

	def testStep_callsBrainStep(self):
		global brainStepCalled
		brainStepCalled = False
		self.p.brain.step = fakeBrainStep
		self.p.step()
		self.assertEqual(True, brainStepCalled)
		
	def testIsFinished_callsBrainIsFinished(self):
		global brainIsFinishedCalled
		brainIsFinishedCalled = False
		self.p.brain.isFinished = fakeBrainIsFinished
		self.p.isFinished()
		self.assertEqual(True, brainIsFinishedCalled)
		
	def testIsFinished_returnsValueFromBrainIsFinished(self):
		global brainIsFinishedValue
		brainIsFinishedValue = True
		self.p.brain.isFinished = fakeBrainIsFinished
		self.assertEqual(True, self.p.isFinished())
		
	def testGetMap_callsBrainGetMap(self):
		global brainGetMapCalled
		brainGetMapCalled = False
		self.p.brain.getBrainMap = fakeBrainGetMap
		self.p.getPlayerMap()
		self.assertEqual(True, brainGetMapCalled)
		
	def testGetMap_returnsValueFromBrainGetMap(self):
		global brainGetMapValue
		brainGetMapValue = 12345
		self.p.brain.getBrainMap = fakeBrainGetMap
		self.assertEqual(12345, self.p.getPlayerMap())
		
# helper

	def assertCollision(self, x, y, collisionFunc, collisionValue, ori = None):
		self.p.setPosition(c.Coordinate(x, y))
		if ori:
			self.p.ori = ori
		self.p.step()
		self.assertEqual(collisionValue, collisionFunc())
		
# tests for FRONT collision detection
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(3, 6, self.p.isFrontCollision, True)
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(3, 5, self.p.isFrontCollision, False)
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(15, 5, self.p.isFrontCollision, True, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(14, 5, self.p.isFrontCollision, False, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(14, 2, self.p.isFrontCollision, True, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(14, 3, self.p.isFrontCollision, False, bb.BaseBrain.ORIENTATION_DOWN)		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(2, 3, self.p.isFrontCollision, True, bb.BaseBrain.ORIENTATION_LEFT)
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(3, 3, self.p.isFrontCollision, False, bb.BaseBrain.ORIENTATION_LEFT)
		
		
# tests for RIGHT collision detection
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(15, 3, self.p.isRightCollision, True)
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(14, 3, self.p.isRightCollision, False)
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(14, 2, self.p.isRightCollision, True, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(14, 3, self.p.isRightCollision, False, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(2, 3, self.p.isRightCollision, True, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(3, 3, self.p.isRightCollision, False, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(3, 6, self.p.isRightCollision, True, bb.BaseBrain.ORIENTATION_LEFT)
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(3, 5, self.p.isRightCollision, False, bb.BaseBrain.ORIENTATION_LEFT)
		
		
# tests for BACK collision detection
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(3, 2, self.p.isBackCollision, True)
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(3, 3, self.p.isBackCollision, False)
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(2, 3, self.p.isBackCollision, True, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(3, 3, self.p.isBackCollision, False, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(3, 6, self.p.isBackCollision, True, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(3, 5, self.p.isBackCollision, False, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(15, 3, self.p.isBackCollision, True, bb.BaseBrain.ORIENTATION_LEFT)
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(14, 3, self.p.isBackCollision, False, bb.BaseBrain.ORIENTATION_LEFT)
		
		
# tests for LEFT collision detection
	
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(2, 3, self.p.isLeftCollision, True)
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationUp(self):
		self.assertCollision(3, 3, self.p.isLeftCollision, False)
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(14, 6, self.p.isLeftCollision, True, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationRight(self):
		self.assertCollision(14, 5, self.p.isLeftCollision, False, bb.BaseBrain.ORIENTATION_RIGHT)
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(15, 3, self.p.isLeftCollision, True, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationDown(self):
		self.assertCollision(14, 3, self.p.isLeftCollision, False, bb.BaseBrain.ORIENTATION_DOWN)
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(3, 2, self.p.isLeftCollision, True, bb.BaseBrain.ORIENTATION_LEFT)
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationLeft(self):
		self.assertCollision(3, 3, self.p.isLeftCollision, False, bb.BaseBrain.ORIENTATION_LEFT)

		
#movement is relative to the player

	def testGetMovementDirection_isForewardOnInit(self):
		self.assertEqual(bb.BaseBrain.DIRECTION_FOREWARD, self.p.getMovementDirection())
		
	def testSetMovementDirection_isUserSpecified(self):
		direction = bb.BaseBrain.DIRECTION_BACKWARD
		self.p.setMovementDirection(direction)
		self.assertEqual(direction, self.p.getMovementDirection())
		
		
#orientation is absolute to the coordinate system

	def testPlayerOrientation_isUpOnInit(self):
		self.assertEqual(bb.BaseBrain.ORIENTATION_UP, self.p.getOrientation())
		
	def testSetOrientation(self):
		ori = bb.BaseBrain.ORIENTATION_RIGHT
		self.p.setOrientation(ori)
		self.assertEqual(ori, self.p.getOrientation())
		
	def testInit_playerOrientation_isUserSpecified(self):
		ori = bb.BaseBrain.ORIENTATION_LEFT
		p4 = player.Player(self.brainClass, self.mObj, self.pos, ori)
		self.assertEqual(ori, p4.getOrientation())
		
		
# helper
		
	def assertMove(self, x, y, orientation, direction, expX, expY):
		self.p.setPosition(c.Coordinate(x, y))
		self.p.setMovementDirection(direction)
		self.p.setOrientation(orientation)
		expectedPos = c.Coordinate(expX, expY)
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
			
# move tests for ORIENTATION_UP
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_withDefaultValues(self):
		self.assertMove(1, 1, bb.BaseBrain.ORIENTATION_UP, bb.BaseBrain.DIRECTION_FOREWARD, 1, 2)
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Up_Backward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_UP, bb.BaseBrain.DIRECTION_BACKWARD, 2, 1)
		
		
# move tests for ORIENTATION_RIGHT
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Right_Foreward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_RIGHT, bb.BaseBrain.DIRECTION_FOREWARD, 3, 2)
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Right_Backward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_RIGHT, bb.BaseBrain.DIRECTION_BACKWARD, 1, 2)
		
		
# move tests for ORIENTATION_DOWN
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Down_Foreward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_DOWN, bb.BaseBrain.DIRECTION_FOREWARD, 2, 1)
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Down_Backward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_DOWN, bb.BaseBrain.DIRECTION_BACKWARD, 2, 3)
		
		
# move tests for ORIENTATION_LEFT
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Left_Foreward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_LEFT, bb.BaseBrain.DIRECTION_FOREWARD, 1, 2)
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Left_Backward(self):
		self.assertMove(2, 2, bb.BaseBrain.ORIENTATION_LEFT, bb.BaseBrain.DIRECTION_BACKWARD, 3, 2)
		
	
	
if __name__ == "__main__":
	unittest.main()	