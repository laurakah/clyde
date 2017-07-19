import unittest
import gameMap

class GameMapTestCase(unittest.TestCase):
	
	def setUp(self):
		self.m = gameMap.GameMap()
		
	def tearDown(self):
		return
		
	def testGameMap_IsEmptyAtInit(self):
		self.assertEqual([], self.m.getMap())
		
	def testGameMap_ConvertsTextToArray_BoxMap(self):
		a = [[1] * 16]
		for i in range(0, 5):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1] * 16)
		m = gameMap.GameMap("maps/test-room1-box.txt")
		self.assertEqual(a, m.getMap())
		
	def testGameMap_ConvertsTextToArray_LMap(self):
		a = [[1] * 28]
		for i in range(0, 2):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
		for i in range(0, 2):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1] * 16)
		m = gameMap.GameMap("maps/test-room2-l-shape.txt")
		self.assertEqual(a, m.getMap())
		
if __name__ == "__main__":
	unittest.main()	