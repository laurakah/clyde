class Player():
	
	DEFAULT_POSITION = {"x": 0, "y": 0}
	DIRECTION_FOREWARD = 1
	ORIENTATION_UP = 0
	ORIENTATION_RIGHT = 1
	ORIENTATION_DOWN = 2
	ORIENTATION_LEFT = 3
	
	def __init__(self, gameMap, pos = DEFAULT_POSITION, ori = ORIENTATION_UP):
		self.m = gameMap
		self.pos = pos
		self.ori = ori
	
	def getPosition(self):
		return self.pos
		
	def isGameOver(self):
		return False
		
	def isCollision(self):
		x = self.pos["x"]
		y = self.pos["y"]
		if self.m[y][x] == 0:
			return False
		else:
			return True
		
	def step(self):													#TODO: robot decision
		if self.isCollision():
			return
		
		self.pos = {"x": 1, "y": 2}
		
	def getMovementDirection(self):
		return Player.DIRECTION_FOREWARD
	
	def getOrientation(self):
		return self.ori
		
	def setOrientation(self, ori):
		self.ori = ori