class Player():
	
	DEFAULT_POSITION = {"x": 0, "y": 0}
	DIRECTION_FOREWARD = 1
	ORIENTATION_UP = 0
	ORIENTATION_RIGHT = 1
	ORIENTATION_DOWN = 2
	ORIENTATION_LEFT = 3
	
	def __init__(self, brainClass, gameMap, pos = DEFAULT_POSITION, ori = ORIENTATION_UP):
		self.inputs = [0]
		self.outputs = [1]
		self.brain = brainClass(self.inputs, self.outputs)
		self.m = gameMap
		self.pos = pos
		self.ori = ori
	
	# inputs for brain class:
	
	def getPosition(self):
		return self.pos
		
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
		#TODO: implement loops for other orientations
		
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
		return Player.DIRECTION_FOREWARD
		
	def getOrientation(self):
		return self.ori
		
	# outputs from brain class:
	
	def setOrientation(self, ori):
		self.ori = ori
		
	# brain status:
		
	def isFinished(self):
		return self.brain.isFinished()
		
	def step(self):
		self.brain.step()
		
	def getMap(self):
		return self.brain.getBrainMap()