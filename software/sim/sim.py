import gameMap
import player

class Sim():
	
	DEFAULT_TIMEOUT = 10000
	EXITCODE_TIMEOUT = 1
	EXITCODE_MAPMISSMATCH = 2
	EXITCODE_MAPMATCH = 0
	
	def __init__(self, gameMapFile, brainClass, timeOut = DEFAULT_TIMEOUT):
		self.runningState = False
		self.gameMapFile = gameMapFile
		self.gameMap = gameMap.GameMap(self.gameMapFile)
		self.stepCount = 0
		self.timeOut = timeOut
		self.brainClass = brainClass
		self.player = player.Player(self.brainClass, self.gameMapFile)
		self.exitCode = None
	
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
			self.stepCount += 1
			self.player.step()
			if self.player.isFinished():
				self.runningState = False
				if self.player.getMap() == self.gameMap.getMap():
					self.exitCode = self.EXITCODE_MAPMATCH
				else:
					self.exitCode = self.EXITCODE_MAPMISSMATCH
		else:
			self.exitCode = self.EXITCODE_TIMEOUT
			self.runningState = False
			
	def getExitCode(self):
		return self.exitCode
			
	def getReport(self):
		rep = {"stepCount" : self.getStepCount(), "gameMapFile" : self.gameMapFile, "timeOut" : self.getTimeOut(), "brainClass": self.brainClass}
		return rep
