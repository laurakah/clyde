import baseBrain
import player

class TheseusBrain(baseBrain.BaseBrain):
	
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
			if ori == player.Player.ORIENTATION_LEFT:
				ori = player.Player.ORIENTATION_UP
			else:
				ori += 1
			self.outputs["setOrientation"](ori)
		else:
			self.outputs["move"]()
			
	def isFinished(self):
		return False