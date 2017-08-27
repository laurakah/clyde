class Coordinate():

	def __init__(self, x = None, y = None):
		self.x = x
		self.y = y

	def isValid(self):
		if self.x > 0 and self.y > 0:
			return True
		return False
