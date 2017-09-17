import copy
import coord as c

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
	UNKNOWN_FIELD = "?"

	PLAYER_POSITION_UP_STR = "A"
	PLAYER_POSITION_RIGHT_STR = ">"
	PLAYER_POSITION_DOWN_STR = "V"
	PLAYER_POSITION_LEFT_STR = "<"

	EMPTY_FIELD_VALUE = 0
	COLLISION_FIELD_VALUE = 1
	PLAYER_POSITION_VALUE = 2
	UNKNOWN_FIELD_VALUE = None

	PLAYER_POSITION_UP_VALUE = 20
	PLAYER_POSITION_RIGHT_VALUE = 21
	PLAYER_POSITION_DOWN_VALUE = 22
	PLAYER_POSITION_LEFT_VALUE = 23

	def __init__(self):
		self.mArr = []
		
	def getMapArray(self):
		return copy.copy(self.mArr)

	def toText(self, pad=False):
		return self.arrayToText(self.mArr, pad)
	
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
					self.mArr[i] = self.mArr[i] + (value * h)
				else:
					self.mArr[i] = (value * h) + self.mArr[i]
			else:
				value = [None]
				if h > 0:
					value = value * (initialWidth + h)
				else:
					value = value * initialWidth
				if appendY:
					self.mArr.append(value)
				else:
 					self.mArr = ([value]) + self.mArr
			
	def withinMap(self, x, y):
		if (y > 0 and self.getHeight() >= y) and (x > 0 and len(self.mArr[0]) >= x):
			return True
		return False
		
	
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
				if c == GameMap.UNKNOWN_FIELD_VALUE:
					strOut += GameMap.UNKNOWN_FIELD

				if c == GameMap.PLAYER_POSITION_UP_VALUE:
					strOut += GameMap.PLAYER_POSITION_UP_STR
				if c == GameMap.PLAYER_POSITION_RIGHT_VALUE:
					strOut += GameMap.PLAYER_POSITION_RIGHT_STR
				if c == GameMap.PLAYER_POSITION_DOWN_VALUE:
					strOut += GameMap.PLAYER_POSITION_DOWN_STR
				if c == GameMap.PLAYER_POSITION_LEFT_VALUE:
					strOut += GameMap.PLAYER_POSITION_LEFT_STR

			strOut += "\n"

			# code for padding

			if not pad:
				continue

			lineLength = len(line)
			if lineLongest < lineLength:
				lineLongest = lineLength

		if pad:
			strOutUnpadded = strOut.rstrip("\n") # remove last \n (so our split() will no give us one element too much
			strOut = ""
			lines = strOutUnpadded.split("\n")
			for line in lines:
				strOut += line.ljust(lineLongest)
				strOut += "\n"

		return strOut

	def getNonCollisionFields(self):
		fields = []
		for y in range(1, len(self.mArr) + 1):
			for x in range(1, len(self.mArr[y - 1]) + 1):
				if self.getLocation(x, y) == self.COLLISION_FIELD_VALUE:
					continue
				fields.append(c.Coordinate(x, y))
		return fields
		
	def draw(self):
		return self.arrayToText(self.mArr)
	
	def writeMapFile(self, filepath):
		mapString = self.draw()
		open(filepath, "w").write(mapString)
		