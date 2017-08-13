import unittest
import player
import dullBrain
import gameMap

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
# 		self.m = PlayerTestCase.createBlankMap(10, 10)
		self.mapFile = "maps/test-room1-box.txt"
		self.m = gameMap.GameMap()
		self.m.loadMapFile(self.mapFile)
		self.pos = {"x": 3, "y": 3}
		self.p = player.Player(self.brainClass, self.m, self.pos)
		
	def tearDown(self):
		return
	
	@staticmethod
	def createBlankMap(width, height):
		m = []
		for i in range(0, width):
			m.append([0] * height)
		return m

	def testInit_raisesException_whenGameMapNotOfTypeGameMap(self):
		e = player.InvalidTypeException
		cls = player.Player
		m = []
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, m, self.pos)
		self.assertEqual("gameMap not of type gameMap.GameMap!", ex.exception.message)
		
	def testInit_playerPosition_isUserSpecified(self):
		pos = {"x": 5, "y": 4}
		p2 = player.Player(self.brainClass, self.m, pos)
		self.assertEqual(pos, p2.getPosition())
		
	def testSetPosition_changesPosition(self):
		pos = {"x": 7, "y": 6}
		self.p.setPosition(pos)
		self.assertEqual(pos, self.p.getPosition())
		
	def testSetPosition_raisesInvalidTypeException_whenPosIsNone(self):
		e = player.InvalidTypeException
		cls = player.Player
		pos = None
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.m, pos)
		self.assertEqual("pos can't be None!", ex.exception.message)
		
	def testSetPosition_raisesInvalidTypeException_whenPosIsNotADict(self):
		e = player.InvalidTypeException
		cls = player.Player
		pos = 45
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.m, pos)
		self.assertEqual("pos must be a dict!", ex.exception.message)
		
	def testSetPosition_raisesExceptionInvalidCoordinateForY(self):
		e = player.InvalidCoordinateException
		cls = player.Player
		pos = {"x": 3, "y": 0}
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.m, pos)
		self.assertEqual("y can't be zero!", ex.exception.message)
		
	def testSetPosition_raisesExceptionInvalidCoordinateForX(self):
		e = player.InvalidCoordinateException
		cls = player.Player
		pos = {"x": 0, "y": 3}
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.m, pos)
		self.assertEqual("x can't be zero!", ex.exception.message)
		
	def testSetPosition_raisesExceptionInvalidCoordinateForMaxYPlusOne(self):
		e = player.InvalidCoordinateException
		cls = player.Player
		pos = {"x": 3, "y": 8}
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.m, pos)
		self.assertEqual("y (%d) can't be outside of map!" % pos["y"], ex.exception.message)
		
	def testSetPosition_raisesExceptionInvalidCoordinateForMaxXPlusOne(self):
		e = player.InvalidCoordinateException
		cls = player.Player
		pos = {"x": 17, "y": 3}
		with self.assertRaises(e) as ex:
			p = cls(self.brainClass, self.m, pos)
		self.assertEqual("x (%d) can't be outside of map!" % pos["x"], ex.exception.message)
		
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
		#expecting default orientation (0)
		self.p.setPosition({"x": 3, "y": 6})
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 3, "y": 5})
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationRight(self):
		#expecting default position (0, 0)
		self.p.setPosition({"x": 15, "y": 5})
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.setPosition({"x": 14, "y": 5})
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationDown(self):
		self.p.setPosition({"x": 14, "y": 2})
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 14, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
	def testIsFrontCollision_isTrueWhenFrontIsTouchingCollisionField_onOrientationLeft(self):
		self.p.setPosition({"x": 2, "y": 3})
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.step()
		self.assertEqual(True, self.p.isFrontCollision())
		
	def testIsFrontCollision_isFalseWhenFrontIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 3, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isFrontCollision())
		
		
# tests for RIGHT collision detection
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 15, "y": 3})
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 14, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.setPosition({"x": 14, "y": 2})
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.setPosition({"x": 14, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 2, "y": 3})
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 3, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
	def testIsRightCollision_isTrueWhenRightIsTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 3, "y": 6})
		self.p.step()
		self.assertEqual(True, self.p.isRightCollision())
		
	def testIsRightCollision_isFalseWhenRightIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 3, "y": 5})
		self.p.step()
		self.assertEqual(False, self.p.isRightCollision())
		
		
# tests for BACK collision detection
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 3, "y": 2})
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 3, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.setPosition({"x": 2, "y": 3})
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.setPosition({"x": 3, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 3, "y": 6})
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 3, "y": 5})
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
	def testIsBackCollision_isTrueWhenBackIsTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 15, "y": 3})
		self.p.step()
		self.assertEqual(True, self.p.isBackCollision())
		
	def testIsBackCollision_isFalseWhenBackIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 14, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isBackCollision())
		
		
# tests for LEFT collision detection
	
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 2, "y": 3})
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationUp(self):
		#expecting default orientation (0)
		self.p.setPosition({"x": 3, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.setPosition({"x": 14, "y": 6})
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationRight(self):
		self.p.ori = player.Player.ORIENTATION_RIGHT
		self.p.setPosition({"x": 14, "y": 5})
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 15, "y": 3})
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationDown(self):
		self.p.ori = player.Player.ORIENTATION_DOWN
		self.p.setPosition({"x": 14, "y": 3})
		self.p.step()
		self.assertEqual(False, self.p.isLeftCollision())
		
		
	def testIsLeftCollision_isTrueWhenLeftIsTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 3, "y": 2})
		self.p.step()
		self.assertEqual(True, self.p.isLeftCollision())
		
	def testIsLeftCollision_isFalseWhenLeftIsNotTouchingCollisionField_onOrientationLeft(self):
		self.p.ori = player.Player.ORIENTATION_LEFT
		self.p.setPosition({"x": 3, "y": 3})
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
		p4 = player.Player(self.brainClass, self.m, self.pos, ori)
		self.assertEqual(ori, p4.getOrientation())
		
			
	# move tests for ORIENTATION_UP
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_withDefaultValues(self):
		# expecting default orientation, direction
		self.p.setPosition({"x": 1, "y": 1})
		ori = self.p.getOrientation()				# UP
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()					# 0, 0
		expectedPos = {"x": 1, "y": 2}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Up_Backward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# UP
		direction = self.p.getMovementDirection()
		pos = self.p.getPosition()
		expectedPos = {"x": 2, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
		
	# move tests for ORIENTATION_RIGHT
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Right_Foreward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setOrientation(player.Player.ORIENTATION_RIGHT)
		ori = self.p.getOrientation()				# RIGHT
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 3, "y": 2}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Right_Backward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setOrientation(player.Player.ORIENTATION_RIGHT)
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# RIGHT
		direction = self.p.getMovementDirection()	# BACKWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 1, "y": 2}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
		
	# move tests for ORIENTATION_DOWN
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Down_Foreward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setOrientation(player.Player.ORIENTATION_DOWN)
		ori = self.p.getOrientation()				# DOWN
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 2, "y": 1}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Down_Backward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setOrientation(player.Player.ORIENTATION_DOWN)
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# DOWN
		direction = self.p.getMovementDirection()	# BACKWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 2, "y": 3}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
		
	# move tests for ORIENTATION_LEFT
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Left_Foreward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setOrientation(player.Player.ORIENTATION_LEFT)
		ori = self.p.getOrientation()				# LEFT
		direction = self.p.getMovementDirection()	# FOREWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 1, "y": 2}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	def testMove_changesPositionAccordingToDirectionAndOrientation_Left_Backward(self):
		self.p.setPosition({"x": 2, "y": 2})
		self.p.setOrientation(player.Player.ORIENTATION_LEFT)
		self.p.setMovementDirection(player.Player.DIRECTION_BACKWARD)
		ori = self.p.getOrientation()				# LEFT
		direction = self.p.getMovementDirection()	# BACKWARD
		pos = self.p.getPosition()
		expectedPos = {"x": 3, "y": 2}
		self.p.move()
		self.assertEqual(expectedPos, self.p.getPosition())
		
	
	
if __name__ == "__main__":
	unittest.main()	