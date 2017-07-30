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

#	def testInit_onUnclosedMapFile_throwsException(self):
#		self.assertRaises(gameMap.OpenGameMapException, gameMap.GameMap, "maps/test-room0.1-open.txt")
		
		
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
		
	def testGameMap_ConvertsArrayToText(self):
		s = "#####\n"
		s += "#   #\n"
		s += "#####\n"
		a = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
		t = gameMap.GameMap.arrayToText(a)
		self.assertEqual(s, t)
		
	def testIsValidLine_isFalseWhenLineIsNotTerminatedWithHash(self):
		line = "#             # "
		self.assertEqual(False, gameMap.GameMap.isValidLine(line))


	def testIsValidLine_isFalseIfHashCountIsSmallerTwo(self):
		line = "               #"
		self.assertEqual(False, gameMap.GameMap.isValidLine(line))

	def testGetNonCollisionFields(self):
		# construct the array of non-collision fields (that matches test-room1-box.txt)
		# calculate all coordinates while skipping all collision fields (result is all non-collision fields)
		# - skip line with y=0 completely
		# - skip line with y=6 (7th line) comletely
		# - subtract first and last x coordinate in every line in between line y=0 and y=6
		fields = []
		for y in range(0, 7):
			if y == 0 or y == 6:
				continue
			for x in range(0, 16):
				if x == 0 or x == 15:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, self.m.getNonCollisionFields())

if __name__ == "__main__":
	unittest.main()	