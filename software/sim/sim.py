import gameMap
import player
import time
import random
import copy
import sys
import baseBrain as bb
import coord as c

class Sim():
	
	DEFAULT_TIMEOUT = 10000
	EXITCODE_TIMEOUT = 1
	EXITCODE_MAPMISSMATCH = 2
	EXITCODE_MAPMATCH = 0
	
	def __init__(self, gameMapFile, brainClass, timeOut = DEFAULT_TIMEOUT, stepDelayMs = 0, follow = False,
			startPosition = None, startOrientation = None):

		# object attributes with fixed initialization values

		self.reset()

		# object attributes with variable initialization values (arguments to init())

		self.gameMapFile = gameMapFile
		self.brainClass = brainClass
		self.timeOut = timeOut
		self.stepDelayMs = stepDelayMs
		self.follow = follow

		# object attributes that depend on previously initialized attributes

		self.init_gameMap(self.gameMapFile)

		self.init_player(startPosition, startOrientation)

	def reset(self):
		self.runningState = False
		self.stepCount = 0
		self.exitCode = None

	def init_gameMap(self, gameMapFile):
		self.gameMap = gameMap.GameMap()
		self.gameMap.loadMapFile(self.gameMapFile)

	def init_player(self, startPosition=None, startOrientation=None):
		fields = self.gameMap.getNonCollisionFields()
		if startPosition == None:
			randomField = fields[random.randint(0, len(fields) - 1)]
			self.startPosition = randomField
		else:
			if not isinstance(startPosition, c.Coordinate):
				raise Exception("startPosition is not a Coordinate object!")
			if not startPosition in fields:
				raise Exception("startPosition is not a non-collision field (in this map)!")
			self.startPosition = startPosition
		
		oris = bb.BaseBrain.ORIENTATION
		if startOrientation == None:
			orisCount = len(oris)
			self.startOrientation = oris[random.randint(0, orisCount - 1)]
		else:
			if not startOrientation in oris:
				raise Exception("startOrientation is invalid!")
			self.startOrientation = startOrientation

		self.player = player.Player(self.brainClass, self.gameMap, self.startPosition, self.startOrientation)

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
		rep.update({"playerMap":		self.getPlayerMap().getMapArray()})
		return rep

	# methods that relate to the player or brain state

	def isFinished(self):
		return self.player.isFinished()
		
	def getPosition(self):
		return self.player.getPosition()
		
	def getOrientation(self):
		return self.player.getOrientation()
		
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
			if self.player.getPlayerMap().getMapArray() == self.getSimMap().getMapArray():
				self.exitCode = self.EXITCODE_MAPMATCH
			else:
				self.exitCode = self.EXITCODE_MAPMISSMATCH

	def _print(self, s):
		sys.stdout.write(s)

	def run(self):
		self.start()
		while self.runningState:
			self.step()
			if self.followIsSet():
				self._print(self.draw())
			if self.runningState == True:
				time.sleep(self.stepDelayMs * (1.0 / 1000))
				

	def drawPlayerMap(self):
		return self.getPlayerMap().toText()

	def drawSimMap(self):
		pos = self.getPosition()
		ori = self.getOrientation()
		playerValue = [
			gameMap.GameMap.PLAYER_POSITION_UP_VALUE,
			gameMap.GameMap.PLAYER_POSITION_RIGHT_VALUE,
			gameMap.GameMap.PLAYER_POSITION_DOWN_VALUE,
			gameMap.GameMap.PLAYER_POSITION_LEFT_VALUE,
		]
		mObj = copy.deepcopy(self.getSimMap())
		mObj.setLocation(pos.x, pos.y, playerValue[ori])
		return mObj.toText()

	def draw(self):
		txt = ""

		txtSimMap = self.drawSimMap()
		txtPlayerMap = self.drawPlayerMap()

		txtSimMapArr = txtSimMap.rstrip().split("\n")
		txtPlayerMapArr = txtPlayerMap.rstrip().split("\n")

		simMapHeight = self.getSimMap().getHeight()
		playerMapHeight = len(txtPlayerMapArr)

		playerMapOffset = simMapHeight - playerMapHeight

		i_player = 0
		for i_sim in range(0, simMapHeight):
			txt += txtSimMapArr[i_sim]
			if i_sim >= playerMapOffset:
				txt += " "
				txt += txtPlayerMapArr[i_player]
				i_player += 1
			txt += "\n"
		return txt
