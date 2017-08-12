import unittest
import player
import baseRoomDetectionBrain

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
		self.brainClass = baseRoomDetectionBrain.BaseRoomDetectionBrain
		self.m = PlayerTestCase.createBlankMap(10, 10)
		self.p = player.Player(self.brainClass, self.m)
		
	def tearDown(self):
		return
	
	@staticmethod
	def createBlankMap(width, height):
		m = []
		for i in range(0, width):
			m.append([0] * height)
		return m

	def testInit_raisesException_whenGameMapNotOfTypeList(self):
		e = player.InvalidTypeException
		c = player.Player
		with self.assertRaises(e) as ex:
			p = c(self.brainClass, {})
		self.assertEqual("gameMap not of type list", ex.exception.message)

	def testPlayerGetPosition_isXTwoYTwoOnInit(self):
		self.assertEqual({"x": 2, "y": 2}, self.p.getPosition())
		
	def testInit_playerPosition_isUserSpecified(self):
		pos = {"x": 2, "y": 3}
		p2 = player.Player(self.brainClass, self.m, pos)
		self.assertEqual(pos, p2.getPosition())
		
	def testSetPosition_changesPosition(self):
		pos = {"x": 99, "y": 55}
		self.p.setPosition(pos)
		self.assertEqual(pos, self.p.getPosition())
		
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
		
		
# tests for FRONT collision detection
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0) and position (0, 0)
		self.m[0][1] = 1
		self.p.pos = {"x": 0, "y": 0}
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0) and position (0, 0)
		self.p.pos = {"x": 0, "y": 0}
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationRight(self):
		#expecting default position (0, 0)
		self.m[1][0] = 1
		self.p.pos = {"x": 0, "y": 0}
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationRight(self):
		#expecting default position (0, 0)
		self.p.pos = {"x": 0, "y": 0}
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationDown(self):
		self.m[1][0] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationLeft(self):
		self.m[0][1] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
# tests for RIGHT collision detection
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0) and position (0, 0)
		self.m[1][0] = 1
		self.p.pos = {"x": 0, "y": 0}
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0) and position (0, 0)
		self.p.pos = {"x": 0, "y": 0}
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationRight(self):
		self.m[1][0] = 1
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationDown(self):
		self.m[0][1] = 1
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationLeft(self):
		self.m[1][2] = 1
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
# tests for BACK collision detection
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.m[1][0] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationRight(self):
		self.m[0][1] = 1
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationDown(self):
		self.m[1][2] = 1
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationLeft(self):
		self.m[2][1] = 1
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
# tests for LEFT collision detection
	
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.m[0][1] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.m[1][2] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.m[2][1] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.m[1][0] = 1
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.pos = {"x": 1, "y": 1}
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		

		
	#movement is relative to the player
	def testGetMovementDirection_isForewardOnInit(self):
		self.assertEqual(player.Player.DIRECTION_FOREWARD, self.p.getMovementDirection())
		
	def testSetMovementDirection_isUserSpecified(self):
		direction = player.Player.DIRECTION_BACKWARD
		self.p.setMovementDirection(direction)
		self.assertEqual(direction, self.p.getMovementDirection())
		
	#orientation is absolute to the coordinate system
	def testPlayerOrientation_isUpOnInit(self):
		self.assertEqual(player.Player.ORIENTATION_UP, self.p.getOrientation())
		
	def testSetOrientation(self):
		ori = player.Player.ORIENTATION_RIGHT
		self.p.setOrientation(ori)
		self.assertEqual(ori, self.p.getOrientation())
		
	def testInit_playerOrientation_isUserSpecified(self):
		ori = player.Player.ORIENTATION_LEFT
		p4 = player.Player(self.brainClass, self.m, None, ori)
		self.assertEqual(ori, p4.getOrientation())
		
			
	# move tests for ORIENTATION_UP
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_withDefaultValues(self):
		# expecting default orientation, direction and position
		self.p.pos = {"x": 0, "y": 0}
		ori = self.p.getOrientation()				# UP
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()					# 0, 0
		expectedPos = {"x": 0, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Up_Backward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# UP
		direction = self.p.getMovementDirection()
		pos = self.p.getPosition()
		expectedPos = {"x": 1, "y": 0}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
		
	# move tests for ORIENTATION_RIGHT
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Right_Foreward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setOrientation(player.Player.ORIENTATION_RIGHT)
		ori = self.p.getOrientation()				# RIGHT
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 2, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Right_Backward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setOrientation(player.Player.ORIENTATION_RIGHT)
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# RIGHT
		direction = self.p.getMovementDirection()	# BACKWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 0, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
		
	# move tests for ORIENTATION_DOWN
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Down_Foreward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setOrientation(player.Player.ORIENTATION_DOWN)
		ori = self.p.getOrientation()				# DOWN
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 1, "y": 0}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Down_Backward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setOrientation(player.Player.ORIENTATION_DOWN)
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# DOWN
		direction = self.p.getMovementDirection()	# BACKWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 1, "y": 2}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
		
	# move tests for ORIENTATION_LEFT
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Left_Foreward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setOrientation(player.Player.ORIENTATION_LEFT)
		ori = self.p.getOrientation()				# LEFT
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 0, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Left_Backward(self):
		self.p.pos = {"x": 1, "y": 1}
		self.p.setOrientation(player.Player.ORIENTATION_LEFT)
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# LEFT
		direction = self.p.getMovementDirection()	# BACKWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 2, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	
	
if __name__ == "__main__":
	unittest.main()	