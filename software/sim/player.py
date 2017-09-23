import copy
import gameMap
import baseBrain as bb
import coord as c

class InvalidTypeException(BaseException):
	pass
class InvalidCoordinateException(BaseException):
	pass


class Player():

	FRONT_COLLISION = 0
	RIGHT_COLLISION = 1
	BACK_COLLISION = 2
	LEFT_COLLISION = 3
	collisionType = [
		FRONT_COLLISION,
		RIGHT_COLLISION,
		BACK_COLLISION,
		LEFT_COLLISION
	]
	collisionTestOperation = [
		# FRONT
		[
			{'y': 1,	'x': 0},	# UP
			{'x': 1,	'y': 0},	# RIGHT
			{'y': -1,	'x': 0},	# DOWN
			{'x': -1,	'y': 0}		# LEFT
		],
		# RIGHT
		[
			{'x': 1,	'y': 0},	# UP
			{'y': -1,	'x': 0},	# RIGHT
			{'x': -1,	'y': 0},	# DOWN
			{'y': 1,	'x': 0}		# LEFT
		],
		# BACK
		[
			{'y': -1,	'x': 0},	# UP
			{'x': -1,	'y': 0},	# RIGHT
			{'y': 1,	'x': 0},	# DOWN
			{'x': 1,	'y': 0}		# LEFT
		],
		# LEFT
		[
			{'x': -1,	'y': 0},	# UP
			{'y': 1,	'x': 0},	# RIGHT
			{'x': 1,	'y': 0},	# DOWN
			{'y': -1,	'x': 0}		# LEFT
		]
	]

	def __init__(self, brainClass, gameMapObj, pos, ori = bb.BaseBrain.ORIENTATION_UP):
		if not isinstance(gameMapObj, gameMap.GameMap):
			raise InvalidTypeException("gameMap not of type gameMap.GameMap!")

		self.inputs = {}
		self.inputs.update({"isCollision": self.isFrontCollision})
		self.inputs.update({"isRightCollision": self.isRightCollision})
		self.inputs.update({"isBackCollision": self.isBackCollision})
		self.inputs.update({"isLeftCollision": self.isLeftCollision})
		self.inputs.update({"getOrientation": self.getOrientation})
		self.inputs.update({"getMovementDirection": self.getMovementDirection})

		self.outputs = {}
		self.outputs.update({"setOrientation": self.setOrientation})
		self.outputs.update({"setMovementDirection": self.setMovementDirection})
		self.outputs.update({"move": self.move})

		self.brain = brainClass(self.inputs, self.outputs)
		self.mObj = gameMapObj
		self.setPosition(pos)
		self.ori = ori
		self.direction = bb.BaseBrain.DIRECTION_FOREWARD
		
	def setPosition(self, pos):
		if not pos:
			raise InvalidTypeException("pos can't be None!")
		if not isinstance(pos, c.Coordinate):
			raise InvalidTypeException("pos must be of type Coordinate!")
		if pos.y == 0 or pos.y == None:
			raise InvalidCoordinateException("y can't be zero!")
		if pos.x == 0 or pos.x == None:
			raise InvalidCoordinateException("x can't be zero!")
		if pos.y > self.mObj.getHeight():
			raise InvalidCoordinateException("y (%d) can't be outside of map!" % pos.y)
		if pos.x > len(self.mObj.getMapArray()[pos.y - 1]):
			raise InvalidCoordinateException("x (%d) can't be outside of map!" % pos.x)
		self.pos = copy.copy(pos)

	def getPosition(self):
		return copy.copy(self.pos)
		
	
# inputs for brain class:

	def genericIsCollision(self, kindOfCollision):
		k = kindOfCollision
		if not k in self.collisionType:
			raise Exception("Invalid collision type %s" % k)
		ori = self.ori
		if not ori in bb.BaseBrain.ORIENTATION:
			raise Exception("Invalid orientation %s" % ori)

		op = self.collisionTestOperation[k][ori]

		x = self.pos.x + op['x']
		y = self.pos.y + op['y']

		if self.mObj.getLocation(x, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
			return True
		else:
			return False

	def isFrontCollision(self):
		return self.genericIsCollision(self.FRONT_COLLISION)

	def isRightCollision(self):
		return self.genericIsCollision(self.RIGHT_COLLISION)

	def isBackCollision(self):
		return self.genericIsCollision(self.BACK_COLLISION)

	def isLeftCollision(self):
		return self.genericIsCollision(self.LEFT_COLLISION)
			
	def getMovementDirection(self):
		return self.direction
		
	def getOrientation(self):
		return self.ori
		
# outputs from brain class:
	
	def setMovementDirection(self, direction):
		self.direction = direction
	
	def setOrientation(self, ori):
		self.ori = ori

	def move(self):
		if not self.getPosition():
			raise Exception("POS CANNOT BE NONE!")

		direction = self.getMovementDirection()
		ori = self.getOrientation()
		pos = self.getPosition()

		nextPos = bb.BaseBrain.getNextPosition(pos, ori, direction)
		
		self.setPosition(nextPos)
		
# brain status:
		
	def isFinished(self):
		return self.brain.isFinished()
		
	def step(self):
		self.brain.step()
		
	def getPlayerMap(self):
		return self.brain.getBrainMap()