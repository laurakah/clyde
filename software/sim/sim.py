import gameMap

class Sim():
	
	def __init__(self, gameMapFile):
		self.runningState = False
		self.gameMapFile = gameMapFile
		self.gameMap = gameMap.GameMap(self.gameMapFile)
	
	def getRunningState(self):
		return self.runningState
		
	def getMap(self):
		return self.gameMap
		
	def start(self):
		self.runningState = True