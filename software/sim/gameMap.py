class EmptyGameMapException(BaseException):
	pass
class OpenGameMapException(BaseException):
	pass

class GameMap():
	
	EMPTY_FIELD = " "
	COLLISION_FIELD = "#"
	PLAYER_POSITION = "*"
	
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
		
	@staticmethod
	def arrayToText(arrayIn):
		strOut = ""
		for line in arrayIn:
			for c in line:
				if c == 1:
					strOut += GameMap.COLLISION_FIELD
				if c == 0:
					strOut += GameMap.EMPTY_FIELD
				if c == 2:
					strOut += GameMap.PLAYER_POSITION
			strOut += "\n"
		return strOut
	
	def getMap(self):
		return self.m

	# FIXME In a non-square map, non-collision locations outside of the room
	# wil also be returned. Make this function so that it will not return
	# these locations.
	def getNonCollisionFields(self):
		fields = []
		for y in range(0, len(self.m)):
			for x in range(0, len(self.m[y])):
				if self.m[y][x] == 1:
					continue
				fields.append({'x': x, 'y': y})
		return fields
