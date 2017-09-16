import re

class Coordinate():

	def __init__(self, x = None, y = None):
		self.x = x
		self.y = y
		
	def __eq__(self, other):
		if other == None:
			return False
		if self.x == other.x and self.y == other.y:
			return True
		return False
	
	def __repr__(self):
		return "<%d, %d>" % (self.x, self.y)
	
	def fromStr(self, coordStr):
		exp = "(?P<x>\d+),[ ]+(?P<y>\d+)"
		m = re.search(exp, coordStr)
		if m:
			self.x = int(m.group('x'))
			self.y = int(m.group('y'))

	def isValid(self):
		if self.x > 0 and self.y > 0:
			return True
		return False

	def translate(self, x, y):
		self.x += x
		self.y += y