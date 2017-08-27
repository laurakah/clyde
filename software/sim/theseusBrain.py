import baseBrain
import player
import copy

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
	
	@staticmethod
	def _updateMap(b, ori, loc, pos):
		x = pos["x"]
		y = pos["y"]
		
		if ori == b.ORIENTATION_UP:
			b.mObj.expandMap(0, 1, True, True)
			b.mObj.setLocation(x, y + 1, loc)
		elif ori == b.ORIENTATION_RIGHT:
			b.mObj.expandMap(1, 0, True, True)
			b.mObj.setLocation(x + 1, y, loc)
		elif ori == b.ORIENTATION_DOWN:
			b.mObj.expandMap(0, 1, False, True)
			b.mObj.setLocation(x, y, loc)
			pos["y"] += 1
		elif ori == b.ORIENTATION_LEFT:
			b.mObj.expandMap(1, 0, True, False)
			b.mObj.setLocation(x, y, loc)
			pos["x"] += 1
		
	def step(self):
		ori = self.inputs["getOrientation"]()
		loc = self._getLocValue(self.inputs)
		pos = self._getPosition()

		self._updateMap(self, ori, loc, pos)

		# decide on where to go next depending on return of isCollision (orientation and
		# movement direction)

		if self.inputs["isCollision"]():
			self.lastOri = ori
			ori = self.getNextOrientation(True)
			self.outputs["setOrientation"](ori)
		else:
			nextPos = self.getNextPosition(pos, ori, self.inputs["getMovementDirection"]())
			self.pos = nextPos
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
			return self.COUNTER_CLOCKWISE
		elif (lastOri == self.ORIENTATION_LEFT and ori == self.ORIENTATION_UP) or (lastOri + 1 == ori):
			return self.CLOCKWISE
			
	def getNextOrientation(self, cw):
		ori = self.inputs["getOrientation"]()
		if cw == True:
			if ori == self.ORIENTATION_LEFT:
				return self.ORIENTATION_UP
			else:
				return ori + 1
		else:
			if ori == self.ORIENTATION_UP:
				return self.ORIENTATION_LEFT
			else:
				return ori - 1
		
		