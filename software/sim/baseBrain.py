import gameMap
import copy
import coord as c

class NotADictException(BaseException):
	pass

class IsEmptyException(BaseException):
	pass

class IsNotAKeyException(BaseException):
	pass
	
class NotAFunctionException(BaseException):
	pass
	
class ArgumentIsNoneException(BaseException):
	pass



class BaseBrain():

	FILENAME_ENDSWITH = "Brain.py"
	
	DIRECTION_FOREWARD = 1
	DIRECTION_BACKWARD = -1

	ORIENTATION_UP = 0
	ORIENTATION_RIGHT = 1
	ORIENTATION_DOWN = 2
	ORIENTATION_LEFT = 3
	ORIENTATION = [ORIENTATION_UP, ORIENTATION_RIGHT, ORIENTATION_DOWN, ORIENTATION_LEFT]

	# used by simLauncher in argument parsing

	ORIENTATION_UP_STR = "up"
	ORIENTATION_RIGHT_STR = "right"
	ORIENTATION_DOWN_STR = "down"
	ORIENTATION_LEFT_STR = "left"
	ORIENTATION_STR = [ORIENTATION_UP_STR, ORIENTATION_RIGHT_STR, ORIENTATION_DOWN_STR, ORIENTATION_LEFT_STR]

	CLOCKWISE = 1
	COUNTER_CLOCKWISE = 0
	
	def __init__(self, inputs, outputs):
		
		self.inputs = None
		self.outputs = None
		
		y = lambda element: element.startswith("is") and element.endswith("Collision")

		arg = "inputs"
		if not isinstance(inputs, dict):
			raise NotADictException(arg)
		arg = "outputs"
		if not isinstance(outputs, dict):
			raise NotADictException(arg)
		arg = "inputs"
		if len(inputs) == 0:
			raise IsEmptyException(arg)
		arg = "outputs"
		if len(outputs) == 0:
			raise IsEmptyException(arg)

		# test keys in inputs argument exists

		arg = "inputs"
		field = "isCollision"
		if not self._isInList(inputs.keys(), y):
			raise IsNotAKeyException("%s: %s" % (arg, field))
		field = "getOrientation"
		if not field in inputs.keys():
			raise IsNotAKeyException("%s: %s" % (arg, field))
		field = "getMovementDirection"
		if not field in inputs.keys():
			raise IsNotAKeyException("%s: %s" % (arg, field))

		# test keys in outputs argument exist

		arg = "outputs"
		field = "setOrientation"
		if not field in outputs.keys():
			raise IsNotAKeyException("%s: %s" % (arg, field))
		field = "setMovementDirection"
		if not field in outputs.keys():
			raise IsNotAKeyException("%s: %s" % (arg, field))
		field = "move"
		if not field in outputs.keys():
			raise IsNotAKeyException("%s: %s" % (arg, field))

		# test values of inputs argument dict are callable

		arg = "inputs"
		field = "isCollision"
		if not self._isCallable(inputs, y):
			raise NotAFunctionException("%s: %s" % (arg, field))
		field = "getOrientation"
		if not callable(inputs[field]):
			raise NotAFunctionException("%s: %s" % (arg, field))
		field = "getMovementDirection"
		if not callable(inputs[field]):
			raise NotAFunctionException("%s: %s" % (arg, field))

		# test values of outputs argument dict are callable

		arg = "outputs"
		field = "setOrientation"
		if not callable(outputs[field]):
			raise NotAFunctionException("%s: %s" % (arg, field))
		field = "setMovementDirection"
		if not callable(outputs[field]):
			raise NotAFunctionException("%s: %s" % (arg, field))
		field = "move"
		if not callable(outputs[field]):
			raise NotAFunctionException("%s: %s" % (arg, field))
			
		self.inputs = inputs
		self.outputs = outputs
		
		self.mObj = gameMap.GameMap()
		self.mObj.mArr.append([0])
		
		self.startPos = c.Coordinate(1, 1)
		
		self.pos = c.Coordinate(1, 1)
		self.lastPos = None
		
		self.firstCollision = None
		
		self.stepLog = []
	
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
		
	def _getPosition(self):
		return copy.copy(self.pos)
		
	def _getLastPosition(self):
		return copy.copy(self.lastPos)
		
	def _getStepLog(self):
		return copy.deepcopy(self.stepLog)
		
	def _getStartPosition(self):
		return copy.copy(self.startPos)
		
	def _getFirstCollisionPos(self):
		return self.firstCollision
		
	@staticmethod
	def getNextPosition(pos, ori, direction):
		
		if pos == None:
			raise ArgumentIsNoneException("Position can't be None!")
		if ori == None:
			raise ArgumentIsNoneException("Orientation can't be None!")
		if direction == None:
			raise ArgumentIsNoneException("Direction can't be None!")
		
		foreward = BaseBrain.DIRECTION_FOREWARD
		backward = BaseBrain.DIRECTION_BACKWARD
		up = BaseBrain.ORIENTATION_UP
		right = BaseBrain.ORIENTATION_RIGHT
		down = BaseBrain.ORIENTATION_DOWN
		left = BaseBrain.ORIENTATION_LEFT
		
		nextPos = copy.deepcopy(pos)
		
		if ori == up and direction == foreward:
			nextPos.y += 1
		elif ori == up and direction == backward:
			nextPos.y -= 1
		elif ori == right and direction == foreward:
			nextPos.x += 1
		elif ori == right and direction == backward:
			nextPos.x -= 1
		elif ori == down and direction == foreward:
			nextPos.y -= 1
		elif ori == down and direction == backward:
			nextPos.y += 1
		elif ori == left and direction == foreward:
			nextPos.x -= 1
		elif ori == left and direction == backward:
			nextPos.x += 1
		else:
			return
		return nextPos
	
	def getBrainMap(self):
		return copy.deepcopy(self.mObj)
		
	def isFinished(self):
		raise NotImplementedError
		
	def step(self):
		raise NotImplementedError