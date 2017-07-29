class InputsNotADictException(BaseException):
	pass
	
class OutputsNotADictException(BaseException):
	pass

class InputsEmptyException(BaseException):
	pass

class OutputsEmptyException(BaseException):
	pass
	
class InputsHasNoIsCollisionKeyException(BaseException):
	pass
	
class InputsHasNoGetOrientationKeyException(BaseException):
	pass

class InputsHasNoGetMovementDirectionKeyException(BaseException):
	pass
	
class OutputsHasNoSetOrientationKeyException(BaseException):
	pass
	
class OutputsHasNoSetMovementDirectionKeyException(BaseException):
	pass
	
class OutputsHasNoMoveKeyException(BaseException):
	pass
	
class NotAFunctionException(BaseException):
	pass



class BaseRoomDetectionBrain():
	
	def __init__(self, inputs, outputs):
		if not isinstance(inputs, dict):
			raise InputsNotADictException()
		if not isinstance(outputs, dict):
			raise OutputsNotADictException()
		if len(inputs) == 0:
			raise InputsEmptyException()
		if len(outputs) == 0:
			raise OutputsEmptyException()
		if not "isCollision" in inputs.keys():
			raise InputsHasNoIsCollisionKeyException()
		if not "getOrientation" in inputs.keys():
			raise InputsHasNoGetOrientationKeyException()
		if not "getMovementDirection" in inputs.keys():
			raise InputsHasNoGetMovementDirectionKeyException()
		if not "setOrientation" in outputs.keys():
			raise OutputsHasNoSetOrientationKeyException()
		if not "setMovementDirection" in outputs.keys():
			raise OutputsHasNoSetMovementDirectionKeyException()
		if not "move" in outputs.keys():
			raise OutputsHasNoMoveKeyException()
		if not callable(inputs["isCollision"]):
			raise NotAFunctionException("isCollision")
		if not callable(inputs["getOrientation"]):
			raise NotAFunctionException("getOrientation")
		if not callable(inputs["getMovementDirection"]):
			raise NotAFunctionException("getMovementDirection")
		if not callable(outputs["setOrientation"]):
			raise NotAFunctionException("setOrientation")
		if not callable(outputs["setMovementDirection"]):
			raise NotAFunctionException("setMovementDirection")
		if not callable(outputs["move"]):
			raise NotAFunctionException("move")
	
	def getBrainMap(self):
		return []
		
	def isFinished(self):
		return False
		
	def step(self):
		return