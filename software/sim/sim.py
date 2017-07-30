import gameMap
import player
import random

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

		fields = self.gameMap.getNonCollisionFields()
		randomField = fields[random.randint(0, len(fields) - 1)]
		self.startPosition = randomField

		self.player = player.Player(self.brainClass, self.gameMapFile, self.startPosition)
		self.exitCode = None
	
	def getRunningState(self):
		return self.runningState
		
	def isFinished(self):
		return self.player.isFinished()
		
	def getTimeOut(self):
		return self.timeOut
		
	def setTimeOut(self, timeOut):
		self.timeOut = timeOut
		
	def getStartPosition(self):
		return self.startPosition

	def getStepCount(self):
		return self.stepCount
		
	def getStepDelay(self):
		return None

	def getMap(self):
		return self.gameMap
		
	def getPosition(self):
		return self.player.getPosition()
		
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
		rep = {}
		rep.update({"stepCount" : self.getStepCount()})
		rep.update({"gameMapFile" : self.gameMapFile})
		rep.update({"startPosition" : self.getStartPosition()})
		rep.update({"timeOut" : self.getTimeOut()})
		rep.update({"brainClass": self.brainClass})
		rep.update({"exitCode": self.getExitCode()})
		return rep

	def draw(self):
		return gameMap.GameMap.arrayToText(self.player.getMap())