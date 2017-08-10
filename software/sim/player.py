import copy

class Player():
	
	# TODO refactor to x: 1, y: 1
	DEFAULT_POSITION = {"x": 2, "y": 2}

	DIRECTION_FOREWARD = 1
	DIRECTION_BACKWARD = -1

	ORIENTATION_UP = 0
	ORIENTATION_RIGHT = 1
	ORIENTATION_DOWN = 2
	ORIENTATION_LEFT = 3
	ORIENTATION = [ORIENTATION_UP, ORIENTATION_RIGHT, ORIENTATION_DOWN, ORIENTATION_LEFT]
	
	def __init__(self, brainClass, gameMap, pos = DEFAULT_POSITION, ori = ORIENTATION_UP):
		# TODO refactor
		self.inputs = {"isCollision": self.isFrontCollision,
				"getOrientation": self.getOrientation,
				"getMovementDirection": self.getMovementDirection}
		# TODO refactor
		self.outputs = {"setOrientation": self.setOrientation,
				"setMovementDirection": self.setMovementDirection,
				"move": self.move}
		self.brain = brainClass(self.inputs, self.outputs)
		self.m = gameMap
		self.pos = copy.copy(pos)
		self.ori = ori
		self.direction = self.DIRECTION_FOREWARD
		
	# not called - only used for testing
	# TODO Have test to check for x or y == 0 (and raise Exception)
	def setPosition(self, pos):
		self.pos["x"] = pos["x"]
		self.pos["y"] = pos["y"]

	# TODO have test to assert address of array is unequal its source
	def getPosition(self):
		return copy.copy(self.pos)
		
	
	# inputs for brain class:

	# TODO refactor
	def isFrontCollision(self):
		x = self.pos["x"]
		y = self.pos["y"]
		if self.ori == self.ORIENTATION_UP:
			if self.m[x][y + 1] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_RIGHT:
			if self.m[x + 1][y] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_DOWN:
			if self.m[x][y - 1] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_LEFT:
			if self.m[x - 1][y] == 1:
				return True
			else:
				return False

	# TODO refactor
	def isRightCollision(self):
		x = self.pos["x"]
		y = self.pos["y"]
		if self.ori == self.ORIENTATION_UP:
			if self.m[x + 1][y] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_RIGHT:
			if self.m[x][y - 1] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_DOWN:
			if self.m[x - 1][y] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_LEFT:
			if self.m[x][y + 1] == 1:
				return True
			else:
				return False

	# TODO refactor
	def isBackCollision(self):
		x = self.pos["x"]
		y = self.pos["y"]
		if self.ori == self.ORIENTATION_UP:
			if self.m[x][y - 1] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_RIGHT:
			if self.m[x - 1][y] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_DOWN:
			if self.m[x][y + 1] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_LEFT:
			if self.m[x + 1][y] == 1:
				return True
			else:
				return False

	# TODO refactor
	def isLeftCollision(self):
		x = self.pos["x"]
		y = self.pos["y"]
		if self.ori == self.ORIENTATION_UP:
			if self.m[x - 1][y] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_RIGHT:
			if self.m[x][y + 1] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_DOWN:
			if self.m[x + 1][y] == 1:
				return True
			else:
				return False
		if self.ori == self.ORIENTATION_LEFT:
			if self.m[x][y - 1] == 1:
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

	# TODO refactor
	def move(self):
		direction = self.getMovementDirection()
		ori = self.getOrientation()
		if ori == self.ORIENTATION_UP and direction == self.DIRECTION_FOREWARD:
			self.pos["y"] += 1
		elif ori == self.ORIENTATION_UP and direction == self.DIRECTION_BACKWARD:
			self.pos["y"] -= 1
		elif ori == self.ORIENTATION_RIGHT and direction == self.DIRECTION_FOREWARD:
			self.pos["x"] += 1
		elif ori == self.ORIENTATION_RIGHT and direction == self.DIRECTION_BACKWARD:
			self.pos["x"] -= 1
		elif ori == self.ORIENTATION_DOWN and direction == self.DIRECTION_FOREWARD:
			self.pos["y"] -= 1
		elif ori == self.ORIENTATION_DOWN and direction == self.DIRECTION_BACKWARD:
			self.pos["y"] += 1
		elif ori == self.ORIENTATION_LEFT and direction == self.DIRECTION_FOREWARD:
			self.pos["x"] -= 1
		elif ori == self.ORIENTATION_LEFT and direction == self.DIRECTION_BACKWARD:
			self.pos["x"] += 1
		
	# brain status:
		
	def isFinished(self):
		return self.brain.isFinished()
		
	def step(self):
		self.brain.step()
		
	def getPlayerMap(self):
		return self.brain.getBrainMap()