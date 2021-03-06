import baseBrain
import player
import copy
import coord as c
import sys

class SimpleBrain(baseBrain.BaseBrain):
	
	
	
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
	def _updateMap(b, ori):
		x = b.pos.x
		y = b.pos.y
		loc = b._getLocValue(b.inputs)
		
		if ori == b.ORIENTATION_UP:
			y += 1
			if not b.mObj.withinMap(x, y):
				b.mObj.expandMap(0, 1, True, True)
				
		elif ori == b.ORIENTATION_RIGHT:
			x += 1
			if not b.mObj.withinMap(x, y):
				b.mObj.expandMap(1, 0, True, True)
				
		elif ori == b.ORIENTATION_DOWN:
			if not b.mObj.withinMap(x, y - 1):
				b.mObj.expandMap(0, 1, False, True)
				
				b.startPos.translate(0, 1)
				
				if b.firstCollision != None:
					b.firstCollision.translate(0, 1)
				
				for entry in b.stepLog:
					entry["pos"].translate(0, 1)
					
				b.pos.y += 1
				
			else:
				y -= 1
			
		elif ori == b.ORIENTATION_LEFT:
			if not b.mObj.withinMap(x - 1, y):
				b.mObj.expandMap(1, 0, True, False)
				
				b.startPos.translate(1, 0)
				
				if b.firstCollision != None:
					b.firstCollision.translate(1, 0)
				
				for entry in b.stepLog:
					entry["pos"].translate(1, 0)
					
				b.pos.x += 1
					
			else:
				x -= 1
			
		else:
			print "WARNING! INVALID ORIENTATION"
			sys.exit(1)
			
		b.mObj.setLocation(x, y, loc)
			
		
	def step(self):
		ori = self.inputs["getOrientation"]()
		direction = self.inputs["getMovementDirection"]()
		stepLog = self.stepLog
		
		# append step log by current position, orientation and movement direction before changing anything
		stepLogEntry = {"pos": self._getPosition(), "ori": ori, "direction": direction}
		self.stepLog.append(stepLogEntry)
		
		# update internal brain map with current location value
		self._updateMap(self, ori)

		# decide on where to go next depending on return of isCollision (orientation and
		# movement direction)
		if self.inputs["isCollision"]():
		
			if self.firstCollision == None:
				self.firstCollision = self._getPosition()
		
		
		# standard behaviour
			nextOriChange = True
			if self.getLastOrientationChange() == self.CLOCKWISE:
				nextOriChange = False
		
				
		# special behaviour	
			if len(stepLog) > 2 and (stepLog[-3]["pos"] == stepLog[-2]["pos"] == stepLog[-1]["pos"]):
				if self.getLastOrientationChange() == self.CLOCKWISE:
					nextOriChange = True
				else:
					nextOriChange = False
		
					
		# applying decisions			
			self.lastOri = ori
			ori = self.getNextOrientation(nextOriChange)
			self.outputs["setOrientation"](ori)
		else:
			self.lastPos = self.pos
			nextPos = self.getNextPosition(self.pos, ori, self.inputs["getMovementDirection"]())
			self.pos = nextPos
			if nextPos == self.firstCollision:
				self.finished = True
			self.outputs["move"]()
			
	def isFinished(self):
		return self.finished
		
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
		
		