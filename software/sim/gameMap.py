import copy

class EmptyGameMapException(BaseException):
	pass
class OpenGameMapException(BaseException):
	pass
	
class InvalidTypeException(BaseException):
	pass
class InvalidCoordinateException(BaseException):
	pass



class GameMap():
	
	EMPTY_FIELD = " "
	COLLISION_FIELD = "#"
	PLAYER_POSITION = "*"

	PLAYER_POSITION_UP = "A"
	PLAYER_POSITION_RIGHT = ">"
	PLAYER_POSITION_DOWN = "V"
	PLAYER_POSITION_LEFT = "<"

	EMPTY_FIELD_VALUE = 0
	COLLISION_FIELD_VALUE = 1
	PLAYER_POSITION_VALUE = 2

	PLAYER_POSITION_UP_VALUE = 20
	PLAYER_POSITION_RIGHT_VALUE = 21
	PLAYER_POSITION_DOWN_VALUE = 22
	PLAYER_POSITION_LEFT_VALUE = 23

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
		if not type(arr) is list:
			raise InvalidTypeException("arr is not of type list!")
		if y > len(arr):
			raise InvalidCoordinateException("y not within arr!")
		if x > len(arr[y - 1]):
			raise InvalidCoordinateException("x not within arr!")
		index = GameMap.posToIndex(x, y)
		if not index:
			return None
		return arr[index[0]][index[1]]
		
	@staticmethod
	def setLocationInArray(arr, x, y, location):
		if not type(arr) is list:
			raise InvalidTypeException("arr is not of type list!")
		if y > len(arr):
			raise InvalidCoordinateException("y not within arr!")
		if x > len(arr[y - 1]):
			raise InvalidCoordinateException("x not within arr!")
		index = GameMap.posToIndex(x, y)
		if not index:
			return
		arr[index[0]][index[1]] = location
		
	@staticmethod
	def posToIndex(x, y):
		if x == 0:
			raise InvalidCoordinateException("x can't be zero!")
		if y == 0:
			raise InvalidCoordinateException("y can't be zero!")
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
		
	def getHeight(self):
		return len(self.m)
		
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

				if c == GameMap.PLAYER_POSITION_UP_VALUE:
					strOut += GameMap.PLAYER_POSITION_UP
				if c == GameMap.PLAYER_POSITION_RIGHT_VALUE:
					strOut += GameMap.PLAYER_POSITION_RIGHT
				if c == GameMap.PLAYER_POSITION_DOWN_VALUE:
					strOut += GameMap.PLAYER_POSITION_DOWN
				if c == GameMap.PLAYER_POSITION_LEFT_VALUE:
					strOut += GameMap.PLAYER_POSITION_LEFT

			strOut += "\n"
		return strOut

	# FIXME In a non-square map, non-collision locations outside of the room
	# wil also be returned. Make this function so that it will not return
	# these locations.
	def getNonCollisionFields(self):
		fields = []
		for y in range(1, len(self.m) + 1):
			for x in range(1, len(self.m[y - 1]) + 1):
				if self.getLocation(x, y) == 1:
					continue
				fields.append({'x': x, 'y': y})
		return fields
