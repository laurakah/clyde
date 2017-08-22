import baseBrain
import player

class TheseusBrain(baseBrain.BaseBrain):
	
	def __init__(self, inputs, outputs):
		baseBrain.BaseBrain.__init__(self, inputs, outputs)
		self.lastOri = None
	
	@staticmethod
	def _getLocValue(inputs):
		loc = None
		if inputs["isCollision"]():
			loc = 1
		else:
			loc = 0
		return loc
		
	def step(self):
		ori = self.inputs["getOrientation"]()
		if ori == 0:
			loc = self._getLocValue(self.inputs)
			self.mObj.mArr.append([loc])
		elif ori == 1:
			loc = self._getLocValue(self.inputs)
			self.mObj.mArr[0].append(loc)
		if self.inputs["isCollision"]():
			self.lastOri = ori
			ori = self.getNextOrientation(True)
			self.outputs["setOrientation"](ori)
		else:
			self.outputs["move"]()
			
	def isFinished(self):
		return False
		
	def getLastOrientation(self):
		return self.lastOri
		
	def getLastOrientationChange(self):
		ori = self.inputs["getOrientation"]()
		lastOri = self.lastOri
		if lastOri == 0 and ori == 3:
			return 0
		elif lastOri == 0 and ori == 1:
			return 1
		elif lastOri == 3 and ori == 0:
			return 1
			
	def getNextOrientation(self, cw):
		ori = self.inputs["getOrientation"]()
		if cw == True:
			if ori == 3:
				return 0
			else:
				return ori + 1
		else:
			if ori == 0:
				return 3
			else:
				return ori - 1
		
		