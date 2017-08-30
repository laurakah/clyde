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
	

	def isValid(self):
		if self.x > 0 and self.y > 0:
			return True
		return False
