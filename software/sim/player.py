import copy
import gameMap
import baseBrain as bb
import coord as c

class InvalidTypeException(BaseException):
	pass
class InvalidCoordinateException(BaseException):
	pass


class Player():
	
	def __init__(self, brainClass, gameMapObj, pos, ori = bb.BaseBrain.ORIENTATION_UP):
		if not isinstance(gameMapObj, gameMap.GameMap):
			raise InvalidTypeException("gameMap not of type gameMap.GameMap!")

		self.inputs = {}
		self.inputs.update({"isCollision": self.isFrontCollision})
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

	# TODO refactor
	def isFrontCollision(self):
		x = self.pos.x
		y = self.pos.y
		if self.ori == bb.BaseBrain.ORIENTATION_UP:
			if self.mObj.getLocation(x, y + 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_RIGHT:
			if self.mObj.getLocation(x + 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_DOWN:
			if self.mObj.getLocation(x, y - 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_LEFT:
			if self.mObj.getLocation(x - 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False

	# TODO refactor
	def isRightCollision(self):
		x = self.pos.x
		y = self.pos.y
		if self.ori == bb.BaseBrain.ORIENTATION_UP:
			if self.mObj.getLocation(x + 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_RIGHT:
			if self.mObj.getLocation(x, y - 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_DOWN:
			if self.mObj.getLocation(x - 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_LEFT:
			if self.mObj.getLocation(x, y + 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False

	# TODO refactor
	def isBackCollision(self):
		x = self.pos.x
		y = self.pos.y
		if self.ori == bb.BaseBrain.ORIENTATION_UP:
			if self.mObj.getLocation(x, y - 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_RIGHT:
			if self.mObj.getLocation(x - 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_DOWN:
			if self.mObj.getLocation(x, y + 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_LEFT:
			if self.mObj.getLocation(x + 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False

	# TODO refactor
	def isLeftCollision(self):
		x = self.pos.x
		y = self.pos.y
		if self.ori == bb.BaseBrain.ORIENTATION_UP:
			if self.mObj.getLocation(x - 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_RIGHT:
			if self.mObj.getLocation(x, y + 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_DOWN:
			if self.mObj.getLocation(x + 1, y) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
		if self.ori == bb.BaseBrain.ORIENTATION_LEFT:
			if self.mObj.getLocation(x, y - 1) == gameMap.GameMap.COLLISION_FIELD_VALUE:
				return True
			else:
				return False
			
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