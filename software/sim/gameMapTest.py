import unittest
import gameMap
import sys
import copy

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
		self.assertNotEqual([], self.m.getMapArray())
		
	def testGameMap_ConvertsTextToArray_BoxMap(self):
		a = [[1] * 16]
		for i in range(0, 5):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1] * 16)
		m = gameMap.GameMap("maps/test-room1-box.txt")
		self.assertEqual(a, m.getMapArray())
		
	def testGameMap_ConvertsTextToArray_LMap(self):
		a = [[1] * 16]
		for i in range(0, 2):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
		for i in range(0, 2):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1] * 28)
		m = gameMap.GameMap("maps/test-room2-l-shape.txt")
		self.assertEqual(a, m.getMapArray())
		
	def testGameMap_ConvertsArrayToText(self):
		s = "#####\n"
		s += "#   #\n"
		s += "#####\n"
		a = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
		t = gameMap.GameMap.arrayToText(a)
		self.assertEqual(s, t)
		
	def testGameMap_ConvertsArrayToText(self):
		s = "#########\n"
		s += "#       #\n"
		s += "#   #####\n"
		s += "#####\n"
		a = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]
		t = gameMap.GameMap.arrayToText(a)
		self.assertEqual(s, t)
		
	def testGameMap_ConvertsArrayToTextWithPlayerPosition(self):
		s = "#####\n"
		s += "# * #\n"
		s += "#####\n"
		a = [[1, 1, 1, 1, 1], [1, 0, 2, 0, 1], [1, 1, 1, 1, 1]]
		t = gameMap.GameMap.arrayToText(a)
		self.assertEqual(s, t)
		
	def testIsValidLine_isFalseWhenLineIsNotTerminatedWithHash(self):
		line = "#             # "
		self.assertEqual(False, gameMap.GameMap.isValidLine(line))


	def testIsValidLine_isFalseIfHashCountIsSmallerTwo(self):
		line = "               #"
		self.assertEqual(False, gameMap.GameMap.isValidLine(line))

	def testGetNonCollisionFields_forBoxMap(self):
		m = gameMap.GameMap("maps/test-room1-box.txt")
		# construct the array of non-collision fields (that matches test-room1-box.txt)
		# calculate all coordinates while skipping all collision fields (result is all non-collision fields)
		# - skip line with y=0 completely
		# - skip line with y=6 (7th line) comletely
		# - subtract first and last x coordinate in every line in between line y=0 and y=6
		fields = []
		mapArray = m.getMapArray()
		maxY = len(mapArray) - 1
		for y in range(0, maxY + 1):
			if y == 0 or y == maxY:
				continue
			maxX = len(mapArray[y]) - 1
			for x in range(0, maxX + 1):
				if x == 0 or x == maxX:
					continue
				# verify that the map location is really a non-collision field
				if mapArray[y][x] == 1:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, m.getNonCollisionFields())

	def testGetNonCollisionFields_forLShapeMap(self):
		self.maxDiff = None
		m = gameMap.GameMap("maps/test-room2-l-shape.txt")
		fields = []
		mapArray = m.getMapArray()
		maxY = len(mapArray) - 1
		for y in range(0, maxY + 1):
			if y == 0 or y == maxY:
				continue
			maxX = len(mapArray[y]) - 1
			for x in range(0, maxX + 1):
				if x == 0 or x == maxX:
					continue
				# verify that the map location is really a non-collision field
				if mapArray[y][x] == 1:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, m.getNonCollisionFields())
		
	def testGetLocation_returnsNoneWhenXIsZero(self):
		self.assertEqual(None, self.m.getLocation(0, 4))
	
	def testGetLocation_returnsNoneWhenYIsZero(self):
		self.assertEqual(None, self.m.getLocation(4, 0))
		
	def testGetLocation_returnsValueFromGameMapArray(self):
		location = 333
		self.m.m[0][0] = location
		self.assertEqual(location, self.m.getLocation(1, 1))
		
	def testSetLocation_setsLocation(self):
		location = 666
		expected = copy.deepcopy(self.m.m)
		expected[2][2] = location
		self.m.setLocation(3, 3, location)
		self.assertEqual(expected, self.m.getMapArray())
		
	def testSetLocation_changesNothingWhenXIsZero(self):
		before = copy.deepcopy(self.m.m)
		location = 444
		self.m.setLocation(0, 4, location)
		self.assertEqual(before, self.m.getMapArray())
	
	def testSetLocation_changesNothingWhenYIsZero(self):
		before = copy.deepcopy(self.m.m)
		location = 555
		self.m.setLocation(4, 0, location)
		self.assertEqual(before, self.m.getMapArray())


if __name__ == "__main__":
	unittest.main()	