import baseBrain
import player

class TheseusBrain(baseBrain.BaseBrain):
		
	def step(self):
		ori = self.inputs["getOrientation"]()
		if ori == 0:
			self.m.m.append([])
		elif ori == 1:
			self.m.m[0].append(75)
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