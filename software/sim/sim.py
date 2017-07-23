import gameMap

class Sim():
	
	DEFAULT_TIMEOUT = 10000
	
	def __init__(self, gameMapFile, timeOut = DEFAULT_TIMEOUT):
		self.runningState = False
		self.gameOverState = False
		self.gameMapFile = gameMapFile
		self.gameMap = gameMap.GameMap(self.gameMapFile)
		self.stepCount = 0
		self.timeOut = timeOut
	
	def getRunningState(self):
		return self.runningState
		
	def getGameOverState(self):
		return self.gameOverState
		
	def getTimeOut(self):
		return self.timeOut
		
	def setTimeOut(self, timeOut):
		self.timeOut = timeOut
		
	def getStepCount(self):
		return self.stepCount
		
	def getMap(self):
		return self.gameMap
		
	def start(self):
		self.runningState = True
		
	def run(self):
		self.start()
		while self.runningState:
			self.step()
		
	def step(self):
		if self.runningState == False:
			return
		if self.stepCount < self.timeOut:
			self.stepCount += 1
		else:
			self.gameOverState = True
			self.runningState = False