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
		
	def testLoadMapFile_updatesMapArray(self):
		mapFile = "maps/test-room2-l-shape.txt"
		expectedArray = gameMap.GameMap.readMapFile(mapFile)
		self.m.loadMapFile(mapFile)
		self.assertEqual(expectedArray, self.m.getMapArray())
		
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
		# - skip line with y=1 completely
		# - skip line with y=7 comletely
		# - subtract first and last x coordinate in every line in between line y=1 and y=7
		fields = []
		mapArray = m.getMapArray()
		maxY = m.getHeight()
		for y in range(1, maxY + 1):
			if y == 1 or y == maxY:
				continue
			maxX = len(mapArray[y - 1])
			for x in range(1, maxX + 1):
				if x == 1 or x == maxX:
					continue
				# verify that the map location is really a non-collision field
				if m.getLocation(x, y) == 1:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, m.getNonCollisionFields())

	def testGetNonCollisionFields_forLShapeMap(self):
		self.maxDiff = None
		m = gameMap.GameMap("maps/test-room2-l-shape.txt")
		fields = []
		mapArray = m.getMapArray()
		maxY = m.getHeight()
		for y in range(1, maxY + 1):
			if y == 1 or y == maxY:
				continue
			maxX = len(mapArray[y - 1])
			for x in range(1, maxX + 1):
				if x == 1 or x == maxX:
					continue
				# verify that the map location is really a non-collision field
				if m.getLocation(x, y) == 1:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, m.getNonCollisionFields())
		
	def testGetHeight_returnsMaxHeightOfMapArray(self):
		m = gameMap.GameMap("maps/test-room2-l-shape.txt")
		self.assertEqual(len(self.m.m), m.getHeight())
		
	def testGetLocation_raisesInvalidCoordinateExceptionForXIsZero(self):
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			self.m.getLocation(0, 2)
		self.assertEqual("x can't be zero!", ex.exception.message)
	
	def testGetLocation_raisesInvalidCoordinateExceptionForYIsZero(self):
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			self.m.getLocation(2, 0)
		self.assertEqual("y can't be zero!", ex.exception.message)
		
	def testGetLocationInArray_raisesInvalidCoordinateExceptionForY(self):
		arr = [[0, 0, 0]] * 3
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			gameMap.GameMap.getLocationFromArray(arr, 2, 5)
		self.assertEqual("y not within arr!", ex.exception.message)
		
	def testGetLocationInArray_raisesInvalidCoordinateExceptionForX(self):
		arr = [[0, 0, 0]] * 3
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			gameMap.GameMap.getLocationFromArray(arr, 5, 2)
		self.assertEqual("x not within arr!", ex.exception.message)
		
	def testGetLocationFromArray_raisesInvalidTypeException(self):
		e = gameMap.InvalidTypeException
		with self.assertRaises(e) as ex:
			gameMap.GameMap.getLocationFromArray({}, 5, 2)
		self.assertEqual("arr is not of type list!", ex.exception.message)
		
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
		
	def testSetLocationInArray_raisesInvalidCoordinateExceptionForY(self):
		arr = [[0, 0, 0]] * 3
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			gameMap.GameMap.setLocationInArray(arr, 2, 5, 0)
		self.assertEqual("y not within arr!", ex.exception.message)
		
	def testSetLocationInArray_raisesInvalidCoordinateExceptionForX(self):
		arr = [[0, 0, 0]] * 3
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			gameMap.GameMap.setLocationInArray(arr, 5, 2, 0)
		self.assertEqual("x not within arr!", ex.exception.message)
		
	def testSetLocationInArray_raisesInvalidTypeException(self):
		e = gameMap.InvalidTypeException
		with self.assertRaises(e) as ex:
			gameMap.GameMap.setLocationInArray({}, 5, 2, 0)
		self.assertEqual("arr is not of type list!", ex.exception.message)


if __name__ == "__main__":
	unittest.main()	