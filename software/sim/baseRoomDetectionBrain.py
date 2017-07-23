class InputsEmptyException(BaseException):
	pass

class OutputsEmptyException(BaseException):
	pass

class BaseRoomDetectionBrain():
	
	def __init__(self, inputs, outputs):
		if len(inputs) == 0:
			raise InputsEmptyException()
		if len(outputs) == 0:
			raise OutputsEmptyException()
	
	def getBrainMap(self):
		return []
		
	def isFinished(self):
		return False
		
	def step(self):
		return