import unittest
import coord

class CoordinateTestCase(unittest.TestCase):

	def setUp(self):
		self.c = coord.Coordinate()

	def tearDown(self):
		return


# tests constructor defaults

	def testInit_xIsNone(self):
		self.assertEqual(None, self.c.x)

	def testInit_yIsNone(self):
		self.assertEqual(None, self.c.y)


# tests constructor arguments

	def testInit_xIsUserSpecified(self):
		c = coord.Coordinate(9, None)
		self.assertEqual(9, c.x)

	def testInit_yIsUserSpecified(self):
		c = coord.Coordinate(None, 32)
		self.assertEqual(32, c.y)


# tests for isValid

	def testIsValid_returnsFalse_whenXIsNone(self):
		self.c.x = None
		self.c.y = 12
		self.assertEqual(False, self.c.isValid())

	def testIsValid_returnsFalse_whenYIsNone(self):
		self.c.x = 92
		self.c.y = None
		self.assertEqual(False, self.c.isValid())

	def testIsValid_returnsFalse_whenXIsZero(self):
		self.c.x = 0
		self.c.y = 29
		self.assertEqual(False, self.c.isValid())

	def testIsValid_returnsFalse_whenYIsZero(self):
		self.c.x = 21
		self.c.y = 0
		self.assertEqual(False, self.c.isValid())

	def testIsValid_returnsFalse_whenXIsNegative(self):
		self.c.x = -3
		self.c.y = 28
		self.assertEqual(False, self.c.isValid())

	def testIsValid_returnFalse_whenYIsNegative(self):
		self.c.x = 18
		self.c.y = -11
		self.assertEqual(False, self.c.isValid())

	def testIsValid_returnsTrue_whenXYArePositiveInts(self):
		self.c.x = 13
		self.c.y = 23
		self.assertEqual(True, self.c.isValid())

		
# tests for comparison
	
	def testCompare_returnsTrueWhenDataIsEqual(self):
		self.c.x = 111
		self.c.y = 222
		c2 = coord.Coordinate(111, 222)
		self.assertEqual(c2, self.c)
		
	def testCompare_returnsFalseWhenOtherIsNotCoordinate(self):
		self.c.x = 111
		self.c.y = 222
		self.assertEqual(False, self.c.__eq__(None))


# tests for "to string" functions

	def testStr(self):
		self.c.x = 100
		self.c.y = 200
		self.assertEqual("<100, 200>", str(self.c))
		

# tests for string parsing

	def testFromStr_parsesStringAndSetsXY(self):
		self.c.fromStr("<23, 42>")
		self.assertEqual(coord.Coordinate(23, 42), self.c)


# tests for translation
	
	def testTranslate_translatesXAccordingToFirstArgument(self):
		self.c.x = 2
		self.c.y = 5
		self.c.translate(1, 0)
		self.assertEqual(coord.Coordinate(3, 5), self.c)
		
	def testTranslate_translatesYAccordingToSecondArgument(self):
		self.c.x = 2
		self.c.y = 5
		self.c.translate(0, 1)
		self.assertEqual(coord.Coordinate(2, 6), self.c)
		
	def testTranslate_translatesXAccordingToFirstArgumentSubtraction(self):
		self.c.x = 4
		self.c.y = 5
		self.c.translate(-2, 0)
		self.assertEqual(coord.Coordinate(2, 5), self.c)
	

if __name__ == '__main__':
	unittest.main()
