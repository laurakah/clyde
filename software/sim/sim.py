import gameMap
import player
import random

class Sim():
	
	DEFAULT_TIMEOUT = 10000
	EXITCODE_TIMEOUT = 1
	EXITCODE_MAPMISSMATCH = 2
	EXITCODE_MAPMATCH = 0
	
	def __init__(self, gameMapFile, brainClass, timeOut = DEFAULT_TIMEOUT, stepDelayMs = None):

		# object attributes with fixed initialization values

		self.runningState = False
		self.stepCount = 0
		self.exitCode = None

		# object attributes with variable initialization values (arguments to init())

		self.gameMapFile = gameMapFile
		self.brainClass = brainClass
		self.timeOut = timeOut
		self.stepDelayMs = stepDelayMs

		# object attributes that depend on previously initialized attributes

		self.gameMap = gameMap.GameMap(self.gameMapFile)

		fields = self.gameMap.getNonCollisionFields()
		randomField = fields[random.randint(0, len(fields) - 1)]
		self.startPosition = randomField

		self.player = player.Player(self.brainClass, self.gameMapFile, self.startPosition)

	# methods that relate to the simulator state
	
	def getRunningState(self):
		return self.runningState
		
	def getStepCount(self):
		return self.stepCount

	def getExitCode(self):
		return self.exitCode

	def getTimeOut(self):
		return self.timeOut

	def setTimeOut(self, timeOut):
		self.timeOut = timeOut

	def getStepDelay(self):
		return self.stepDelayMs

	def getMap(self):
		return self.gameMap

	def getStartPosition(self):
		return self.startPosition

	def getReport(self):
		rep = {}
		rep.update({"stepCount":	self.getStepCount()})
		rep.update({"gameMapFile":	self.gameMapFile})
		rep.update({"startPosition":	self.getStartPosition()})
		rep.update({"timeOut":		self.getTimeOut()})
		rep.update({"brainClass":	self.brainClass})
		rep.update({"exitCode":		self.getExitCode()})
		return rep

	# methods that relate to the player or brain state

	def isFinished(self):
		return self.player.isFinished()
		
	def getPosition(self):
		return self.player.getPosition()

	# operations

	def start(self):
		self.runningState = True
		
	def step(self):
		if self.runningState == False:
			return
		if self.stepCount >= self.timeOut:
			self.exitCode = self.EXITCODE_TIMEOUT
			self.runningState = False
			return
		self.stepCount += 1
		self.player.step()
		if self.player.isFinished():
			self.runningState = False
			if self.player.getMap() == self.gameMap.getMap():
				self.exitCode = self.EXITCODE_MAPMATCH
			else:
				self.exitCode = self.EXITCODE_MAPMISSMATCH

	def run(self):
		self.start()
		while self.runningState:
			self.step()

	def draw(self):
		return gameMap.GameMap.arrayToText(self.player.getMap())