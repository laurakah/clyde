import unittest
import gameMap
import sys
import copy

class GameMapTestCase(unittest.TestCase):
	
	def setUp(self):
		self.gameMapFile = "maps/test-room1-box.txt"
		self.mObj = gameMap.GameMap()
		self.mObj.loadMapFile(self.gameMapFile)
		
	def tearDown(self):
		return
		
# 	def testInit_onEmptyMapFile_throwsException(self):
# 		self.assertRaises(gameMap.EmptyGameMapException, gameMap.GameMap, "maps/test-room0-empty.txt")

#	def testInit_onUnclosedMapFile_throwsException(self):
#		self.assertRaises(gameMap.OpenGameMapException, gameMap.GameMap, "maps/test-room0.1-open.txt")
		
	def testLoadMapFile_updatesMapArray(self):
		mapFile = "maps/test-room2-l-shape.txt"
		expectedArray = gameMap.GameMap.readMapFile(mapFile)
		self.mObj.loadMapFile(mapFile)
		self.assertEqual(expectedArray, self.mObj.getMapArray())
		
	def testGameMap_ConvertsTextToArray_BoxMap(self):
		a = [[1] * 16]
		for i in range(0, 5):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1] * 16)
		mObj = gameMap.GameMap()
		mObj.loadMapFile("maps/test-room1-box.txt")
		self.assertEqual(a, mObj.getMapArray())
		
	def testGameMap_ConvertsTextToArray_LMap(self):
		a = [[1] * 16]
		for i in range(0, 2):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
		for i in range(0, 2):
			a.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
		a.append([1] * 28)
		mObj = gameMap.GameMap()
		mObj.loadMapFile("maps/test-room2-l-shape.txt")
		self.assertEqual(a, mObj.getMapArray())
		
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
		

	# test to draw map with player position and orientation


	def testGameMap_ConvertsArrayToTextWithPlayerPositionAndOrientation_Up(self):
		player_up = "A"
		player_up_value = 20
		expectTxt = "#####\n"
		expectTxt += "# %c #\n" % player_up
		expectTxt += "#####\n"
		mapArrIn = [[1, 1, 1, 1, 1], [1, 0, player_up_value, 0, 1], [1, 1, 1, 1, 1]]
		txt = gameMap.GameMap.arrayToText(mapArrIn)
		self.assertEqual(expectTxt, txt)

	def testGameMap_ConvertsArrayToTextWithPlayerPositionAndOrientation_Right(self):
		player_right = ">"
		player_right_value = 21
		expectTxt = "#####\n"
		expectTxt += "# %c #\n" % player_right
		expectTxt += "#####\n"
		mapArrIn = [[1, 1, 1, 1, 1], [1, 0, player_right_value, 0, 1], [1, 1, 1, 1, 1]]
		txt = gameMap.GameMap.arrayToText(mapArrIn)
		self.assertEqual(expectTxt, txt)

	def testGameMap_ConvertsArrayToTextWithPlayerPositionAndOrientation_Down(self):
		player_down = "V"
		player_down_value = 22
		expectTxt = "#####\n"
		expectTxt += "# %c #\n" % player_down
		expectTxt += "#####\n"
		mapArrIn = [[1, 1, 1, 1, 1], [1, 0, player_down_value, 0, 1], [1, 1, 1, 1, 1]]
		txt = gameMap.GameMap.arrayToText(mapArrIn)
		self.assertEqual(expectTxt, txt)

	def testGameMap_ConvertsArrayToTextWithPlayerPositionAndOrientation_Left(self):
		player_left = "<"
		player_left_value = 23
		expectTxt = "#####\n"
		expectTxt += "# %c #\n" % player_left
		expectTxt += "#####\n"
		mapArrIn = [[1, 1, 1, 1, 1], [1, 0, player_left_value, 0, 1], [1, 1, 1, 1, 1]]
		txt = gameMap.GameMap.arrayToText(mapArrIn)
		self.assertEqual(expectTxt, txt)

	def testIsValidLine_isFalseWhenLineIsNotTerminatedWithHash(self):
		line = "#             # "
		self.assertEqual(False, gameMap.GameMap.isValidLine(line))


	def testIsValidLine_isFalseIfHashCountIsSmallerTwo(self):
		line = "               #"
		self.assertEqual(False, gameMap.GameMap.isValidLine(line))

	def testGetNonCollisionFields_forBoxMap(self):
		mObj = gameMap.GameMap()
		mObj.loadMapFile("maps/test-room1-box.txt")
		# construct the array of non-collision fields (that matches test-room1-box.txt)
		# calculate all coordinates while skipping all collision fields (result is all non-collision fields)
		# - skip line with y=1 completely
		# - skip line with y=7 comletely
		# - subtract first and last x coordinate in every line in between line y=1 and y=7
		fields = []
		mapArray = mObj.getMapArray()
		maxY = mObj.getHeight()
		for y in range(1, maxY + 1):
			if y == 1 or y == maxY:
				continue
			maxX = len(mapArray[y - 1])
			for x in range(1, maxX + 1):
				if x == 1 or x == maxX:
					continue
				# verify that the map location is really a non-collision field
				if mObj.getLocation(x, y) == 1:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, mObj.getNonCollisionFields())

	def testGetNonCollisionFields_forLShapeMap(self):
		self.maxDiff = None
		mObj = gameMap.GameMap()
		mObj.loadMapFile("maps/test-room2-l-shape.txt")
		fields = []
		mapArray = mObj.getMapArray()
		maxY = mObj.getHeight()
		for y in range(1, maxY + 1):
			if y == 1 or y == maxY:
				continue
			maxX = len(mapArray[y - 1])
			for x in range(1, maxX + 1):
				if x == 1 or x == maxX:
					continue
				# verify that the map location is really a non-collision field
				if mObj.getLocation(x, y) == 1:
					continue
				fields.append({'x': x, 'y': y})
		self.assertEqual(fields, mObj.getNonCollisionFields())
		
	def testGetHeight_returnsMaxHeightOfMapArray(self):
		mObj = gameMap.GameMap()
		mObj.loadMapFile("maps/test-room2-l-shape.txt")
		self.assertEqual(len(self.mObj.mArr), mObj.getHeight())
		
	def testGetLocation_raisesInvalidCoordinateExceptionForXIsZero(self):
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			self.mObj.getLocation(0, 2)
		self.assertEqual("x can't be zero!", ex.exception.message)
	
	def testGetLocation_raisesInvalidCoordinateExceptionForYIsZero(self):
		e = gameMap.InvalidCoordinateException
		with self.assertRaises(e) as ex:
			self.mObj.getLocation(2, 0)
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
		self.mObj.mArr[0][0] = location
		self.assertEqual(location, self.mObj.getLocation(1, 1))
		
	def testSetLocation_setsLocation(self):
		location = 666
		expected = copy.deepcopy(self.mObj.mArr)
		expected[2][2] = location
		self.mObj.setLocation(3, 3, location)
		self.assertEqual(expected, self.mObj.getMapArray())
		
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