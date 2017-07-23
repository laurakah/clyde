class EmptyGameMapException(BaseException):
	pass
class OpenGameMapException(BaseException):
	pass

class GameMap():
	
	EMPTY_FIELD = " "
	COLLISION_FIELD = "#"
	
	def __init__(self, gameMapFile):
		m = GameMap.readMapFile(gameMapFile)
		if m == []:
			raise EmptyGameMapException()
		self.m = m

	@staticmethod
	def isValidLine(line):
		c = GameMap.COLLISION_FIELD
		if line[-1] != c:
			return False
		if line.count(c) < 2:
			return False
		return True

	@staticmethod
	def readMapFile(gameMapFile):
		lineInvalid = False
		m = []
		txt = []
		f = open(gameMapFile)
		for line in f.readlines():
			txt.append(line)
		f.close()
		for line in txt:
			fields = []
			for c in line:
				if c == GameMap.COLLISION_FIELD:
					fields.append(1)
				if c == GameMap.EMPTY_FIELD:
					fields.append(0)
			m.append(fields)
		return m
	
	def getMap(self):
		return self.m