import gameMap
import player

class Sim():
	
	DEFAULT_TIMEOUT = 10000
	
	def __init__(self, gameMapFile, brainClass, timeOut = DEFAULT_TIMEOUT):
		self.runningState = False
		self.gameMapFile = gameMapFile
		self.gameMap = gameMap.GameMap(self.gameMapFile)
		self.stepCount = 0
		self.timeOut = timeOut
		self.brainClass = brainClass
		self.player = player.Player(self.brainClass, self.gameMapFile)
	
	def getRunningState(self):
		return self.runningState
		
	def isFinished(self):
		return self.player.isFinished()
		
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
			self.player.step()
			self.stepCount += 1
		else:
			self.runningState = False
			
	def getReport(self):
		rep = {"stepCount" : self.getStepCount(), "gameMapFile" : self.gameMapFile, "timeOut" : self.getTimeOut(), "brainClass": self.brainClass}
		return rep
