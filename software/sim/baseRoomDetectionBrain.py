class NotADictException(BaseException):
	pass

class IsEmptyException(BaseException):
	pass

class IsNotAKeyException(BaseException):
	pass
	
class NotAFunctionException(BaseException):
	pass



class BaseRoomDetectionBrain():
	
	def __init__(self, inputs, outputs):
		y = lambda element: element.startswith("is") and element.endswith("Collision")
		
		if not isinstance(inputs, dict):
			raise NotADictException("inputs")
		if not isinstance(outputs, dict):
			raise NotADictException("outputs")
		if len(inputs) == 0:
			raise IsEmptyException("inputs")
		if len(outputs) == 0:
			raise IsEmptyException("outputs")
		if not self._isInList(inputs.keys(), y):
			raise IsNotAKeyException("inputs: isCollision")
		if not "getOrientation" in inputs.keys():
			raise IsNotAKeyException("inputs: getOrientation")
		if not "getMovementDirection" in inputs.keys():
			raise IsNotAKeyException("inputs: getMovementDirection")
		if not "setOrientation" in outputs.keys():
			raise IsNotAKeyException("outputs: setOrientation")
		if not "setMovementDirection" in outputs.keys():
			raise IsNotAKeyException("outputs: setMovementDirection")
		if not "move" in outputs.keys():
			raise IsNotAKeyException("outputs: move")
		if not self._isCallable(inputs, y):
			raise NotAFunctionException("inputs: isCollision")
		if not callable(inputs["getOrientation"]):
			raise NotAFunctionException("inputs: getOrientation")
		if not callable(inputs["getMovementDirection"]):
			raise NotAFunctionException("inputs: getMovementDirection")
		if not callable(outputs["setOrientation"]):
			raise NotAFunctionException("outputs: setOrientation")
		if not callable(outputs["setMovementDirection"]):
			raise NotAFunctionException("outputs: setMovementDirection")
		if not callable(outputs["move"]):
			raise NotAFunctionException("outputs: move")
	
	def _isInList(self, inputList, x):
		for item in inputList:
			if x(item):
				return True
		return False
		
	def _isCallable(self, inputDict, x):
		check = []
		for item in inputDict.keys():
			if x(item):
				check.append(item)
		if len(check) == 0:
			return False
		for elem in check:
			if callable(inputDict[elem]):
				continue
			return False
		return True
	
	def getBrainMap(self):
		return []
		
	def isFinished(self):
		return False
		
	def step(self):
		return