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
		if ori == self.ORIENTATION_UP:
			loc = self._getLocValue(self.inputs)
			self.mObj.mArr.append([loc])
		elif ori == self.ORIENTATION_RIGHT:
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
		lastOri = self.lastOri
		if lastOri == None:
			return None
		ori = self.inputs["getOrientation"]()
		if (lastOri == self.ORIENTATION_UP and ori == self.ORIENTATION_LEFT) or (lastOri - 1 == ori):
			return 0
		elif (lastOri == self.ORIENTATION_LEFT and ori == self.ORIENTATION_UP) or (lastOri + 1 == ori):
			return 1
			
	def getNextOrientation(self, cw):
		ori = self.inputs["getOrientation"]()
		if cw == True:
			if ori == self.ORIENTATION_LEFT:
				return 0
			else:
				return ori + 1
		else:
			if ori == self.ORIENTATION_UP:
				return 3
			else:
				return ori - 1
		
		