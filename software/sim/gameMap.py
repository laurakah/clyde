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

	def __init__(self):
		self.mArr = []
		
	def getMapArray(self):
		return self.mArr
	
	def getLocation(self, x, y):
		return self.getLocationFromArray(self.mArr, x, y)
		
	def setLocation(self, x, y, location):
		self.setLocationInArray(self.mArr, x, y, location)
		
	def expandMap(self, h, v, appendY, appendX):
		initialHeight = self.getHeight()
		if len(self.mArr) > 0:
			initialWidth = len(self.mArr[0])
		else:
			initialWidth = 0
		for i in range(0, (initialHeight + v)):
			if i < initialHeight:
				value = [None]
				if appendX:
					self.mArr[i] = self.mArr[i] + ([value] * h)
				else:
					self.mArr[i] = (value * h) + self.mArr[i]
			else:
				value = [None]
				if h > 1:
					value = value * (initialWidth + h)
				if appendY:
					self.mArr.append(value)
				else:
 					self.mArr = [value] + self.mArr
			
	
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
		mArr = []
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
			mArr.append(fields)
		mArr.reverse()
		return mArr
		
	def loadMapFile(self, mapFile):
		mArr = GameMap.readMapFile(mapFile)
		if mArr == []:
			raise EmptyGameMapException()
		self.mArr = mArr
		
	def getHeight(self):
		return len(self.mArr)
		
	@staticmethod
	def arrayToText(arrayIn, pad=False):
		arrayIn = copy.copy(arrayIn)
		arrayIn.reverse()
		lineLongest = 0
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

			# code for padding

			if not pad:
				continue

			lineLength = len(line)
			if lineLongest < lineLength:
				lineLongest = lineLength

		if pad:
			strOutUnpadded = strOut.rstrip() # remove last \n (so our split() will no give us one element to much
			strOut = ""
			for line in strOutUnpadded.split("\n"):
				lineLength = len(line)
				if lineLongest > lineLength:
					padSpaces = lineLongest - lineLength
					line += " " * padSpaces
				strOut += line
				strOut += "\n"

		return strOut

	# FIXME In a non-square map, non-collision locations outside of the room
	# wil also be returned. Make this function so that it will not return
	# these locations.
	def getNonCollisionFields(self):
		fields = []
		for y in range(1, len(self.mArr) + 1):
			for x in range(1, len(self.mArr[y - 1]) + 1):
				if self.getLocation(x, y) == 1:
					continue
				fields.append({'x': x, 'y': y})
		return fields
		
	def draw(self):
		return self.arrayToText(self.mArr)
	

	def writeMapFile(self, filepath):
		mapString = self.draw()
		open(filepath, "w").write(mapString)
		