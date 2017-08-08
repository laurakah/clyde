import gameMap
import player
import time
import random
import copy

class Sim():
	
	DEFAULT_TIMEOUT = 10000
	EXITCODE_TIMEOUT = 1
	EXITCODE_MAPMISSMATCH = 2
	EXITCODE_MAPMATCH = 0
	
	def __init__(self, gameMapFile, brainClass, timeOut = DEFAULT_TIMEOUT, stepDelayMs = 0, follow = False):

		# object attributes with fixed initialization values

		self.runningState = False
		self.stepCount = 0
		self.exitCode = None

		# object attributes with variable initialization values (arguments to init())

		self.gameMapFile = gameMapFile
		self.brainClass = brainClass
		self.timeOut = timeOut
		self.stepDelayMs = stepDelayMs
		self.follow = follow

		# object attributes that depend on previously initialized attributes

		self.gameMap = gameMap.GameMap(self.gameMapFile)

		fields = self.gameMap.getNonCollisionFields()
		randomField = fields[random.randint(0, len(fields) - 1)]
		self.startPosition = randomField

		self.player = player.Player(self.brainClass, self.gameMapFile, self.startPosition)
		
		oris = player.Player.ORIENTATION
		orisCount = len(oris)
		self.startOrientation = oris[random.randint(0, orisCount - 1)]

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
		
	def followIsSet(self):
		return self.follow
	
	def getSimMap(self):
		return self.gameMap

	def getStartPosition(self):
		return self.startPosition
		
	def getStartOrientation(self):
		return self.startOrientation
	

	def getReport(self):
		rep = {}
		rep.update({"stepCount":		self.getStepCount()})
		rep.update({"gameMapFile":		self.gameMapFile})
		rep.update({"startPosition":	self.getStartPosition()})
		rep.update({"timeOut":			self.getTimeOut()})
		rep.update({"brainClass":		self.brainClass})
		rep.update({"exitCode":			self.getExitCode()})
		rep.update({"simMap":			self.getSimMap()})
		rep.update({"playerMap":		self.getPlayerMap()})
		return rep

	# methods that relate to the player or brain state

	def isFinished(self):
		return self.player.isFinished()
		
	def getPosition(self):
		return self.player.getPosition()
		
	def getPlayerMap(self):
		return self.player.getPlayerMap()
	

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
			if self.player.getPlayerMap() == self.getSimMap().getMapArray():
				self.exitCode = self.EXITCODE_MAPMATCH
			else:
				self.exitCode = self.EXITCODE_MAPMISSMATCH

	def run(self):
		self.start()
		while self.runningState:
			self.step()
			if self.followIsSet():
				self.draw()
			if self.runningState == True:
				time.sleep(self.stepDelayMs * (1.0 / 1000))
				

	def draw(self):
		return gameMap.GameMap.arrayToText(self.getPlayerMap())

	def drawSimMap(self):
		pos = self.getPosition()
		m = copy.deepcopy(self.getSimMap())
		m.setLocation(pos['x'], pos['y'], 2)
		return gameMap.GameMap.arrayToText(m.getMapArray())
