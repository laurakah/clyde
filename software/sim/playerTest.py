import unittest
import player
import baseRoomDetectionBrain

brainStepCalled = False
brainIsFinishedCalled = False
brainIsFinishedValue = False

def fakeBrainStep():
	global brainStepCalled
	brainStepCalled = True
	
def fakeBrainIsFinished():
	global brainIsFinishedCalled
	global brainIsFinishedValue
	brainIsFinishedCalled = True
	return brainIsFinishedValue


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
	
	def testPlayerPosition_isZeroOnInit(self):
		self.assertEqual({"x": 0, "y": 0}, self.p.getPosition())
		
	def testInit_playerPosition_isUserSpecified(self):
		pos = {"x": 2, "y": 3}
		p2 = player.Player(self.brainClass, self.m, pos)
		self.assertEqual(pos, p2.getPosition())
		
# 	def testIsGameOver_isNotTrueOnInit(self):
# 		self.assertEqual(False, self.p.isGameOver())
		
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
		
# 	def testStep_changesPositionWhenNoCollision(self):
# 		pos = self.p.getPosition()
# 		self.p.step()
# 		self.assertNotEqual(pos, self.p.getPosition())
# 		
# 	def testStep_doesNotChangePositionOnCollision(self):
# 		self.m[9][9] = 1
# 		p3 = player.Player(self.brainClass, self.m, {"x": 9, "y": 9})
# 		pos = p3.getPosition()
# 		p3.step()
# 		self.assertEqual(pos, p3.getPosition())
# 		
# 	def testStep_movesExactlyOneStep(self):
# 		pos = self.p.getPosition()
# 		pos["y"] += 1
# 		self.p.step()
# 		self.assertEqual(pos, self.p.getPosition())
		
	def testIsCollision_isFalseOnInit(self):
		self.assertEqual(False, self.p.isCollision())
		
	def testIsCollision_isTrueOnCollision(self):
		self.m[9][9] = 1
		p3 = player.Player(self.brainClass, self.m, {"x": 9, "y": 9})
		p3.step()
		self.assertEqual(True, p3.isCollision())
		
	#movement is relative to the player
	def testMovementDirection_isForewardOnInit(self):
		self.assertEqual(player.Player.DIRECTION_FOREWARD, self.p.getMovementDirection())
		
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
	
	
if __name__ == "__main__":
	unittest.main()	