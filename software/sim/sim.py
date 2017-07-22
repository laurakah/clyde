class Sim():
	
	def __init__(self):
		self.runningState = False
	
	def getRunningState(self):
		return self.runningState
		
	def start(self):
		self.runningState = True