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
	

if __name__ == '__main__':
	unittest.main()
