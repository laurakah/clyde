import unittest
import player

class PlayerTestCase(unittest.TestCase):
	
	def setUp(self):
		self.m = PlayerTestCase.createBlankMap(10, 10)
		self.p = player.Player(self.m)
		
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
		
	def testPlayerPosition_isUserSpecified(self):
		pos = {"x": 2, "y": 3}
		p2 = player.Player(self.m, pos)
		self.assertEqual(pos, p2.getPosition())
		
	def testIsGameOver_isNotTrueOnInit(self):
		self.assertEqual(False, self.p.isGameOver())
		
	def testStep_changesPositionWhenNoCollision(self):
		pos = self.p.getPosition()
		self.p.step()
		self.assertNotEqual(pos, self.p.getPosition())
		
	def testStep_doesNotChangePositionOnCollision(self):
		self.m[9][9] = 1
		p3 = player.Player(self.m, {"x": 9, "y": 9})
		pos = p3.getPosition()
		p3.step()
		self.assertEqual(pos, p3.getPosition())
		
# 	def testStep_movesExactlyOneStep(self):
# 		pos = self.p.getPosition()
# 		pos["y"] += 1
# 		self.p.step()
# 		self.assertEqual(pos, self.p.getPosition())
		
	def testIsCollision_isFalseOnInit(self):
		self.assertEqual(False, self.p.isCollision())
		
	def testIsCollision_isTrueOnCollision(self):
		self.m[9][9] = 1
		p3 = player.Player(self.m, {"x": 9, "y": 9})
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
	
	
if __name__ == "__main__":
	unittest.main()	