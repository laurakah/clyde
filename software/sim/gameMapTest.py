import unittest
import gameMap

class GameMapTestCase(unittest.TestCase):
	
	def setUp(self):
		self.gameMapFile = "maps/test-room1-box.txt"
		self.m = gameMap.GameMap(self.gameMapFile)
		
	def tearDown(self):
		return
		
	def testInit_onEmptyMapFile_throwsException(self):
		self.assertRaises(gameMap.EmptyGameMapException, gameMap.GameMap, "maps/test-room0-empty.txt")
		
		
	def testInit_GameMap_IsNotEmptyAtInit(self):
		self.assertNotEqual([], self.m.getMap())
		
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