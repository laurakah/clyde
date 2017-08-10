import copy

class EmptyGameMapException(BaseException):
	pass
class OpenGameMapException(BaseException):
	pass

class GameMap():
	
	EMPTY_FIELD = " "
	COLLISION_FIELD = "#"
	PLAYER_POSITION = "*"

	EMPTY_FIELD_VALUE = 0
	COLLISION_FIELD_VALUE = 1
	PLAYER_POSITION_VALUE = 2

	def __init__(self, gameMapFile):
		self.loadMapFile(gameMapFile)
		
	def getMapArray(self):
		return self.m
	
	def getLocation(self, x, y):
		return self.getLocationFromArray(self.m, x, y)
		
	def setLocation(self, x, y, location):
		self.setLocationInArray(self.m, x, y, location)
	
	@staticmethod
	def getLocationFromArray(arr, x, y):
		index = GameMap.posToIndex(x, y)
		if not index:
			return None
		return arr[index[0]][index[1]]
		
	@staticmethod
	def setLocationInArray(arr, x, y, location):
		index = GameMap.posToIndex(x, y)
		if not index:
			return
		arr[index[0]][index[1]] = location
		
	@staticmethod
	def posToIndex(x, y):
		if x == 0:
			return None
		if y == 0:
			return None
		return [y - 1, x - 1]
	
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
					fields.append(GameMap.COLLISION_FIELD_VALUE)
				if c == GameMap.EMPTY_FIELD:
					fields.append(GameMap.EMPTY_FIELD_VALUE)
			m.append(fields)
		m.reverse()
		return m
		
	def loadMapFile(self, mapFile):
		m = GameMap.readMapFile(mapFile)
		if m == []:
			raise EmptyGameMapException()
		self.m = m
		
	@staticmethod
	def arrayToText(arrayIn):
		arrayIn = copy.copy(arrayIn)
		arrayIn.reverse()
		strOut = ""
		for line in arrayIn:
			for c in line:
				if c == GameMap.COLLISION_FIELD_VALUE:
					strOut += GameMap.COLLISION_FIELD
				if c == GameMap.EMPTY_FIELD_VALUE:
					strOut += GameMap.EMPTY_FIELD
				if c == GameMap.PLAYER_POSITION_VALUE:
					strOut += GameMap.PLAYER_POSITION
			strOut += "\n"
		return strOut

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
