import baseBrain
import player

class TheseusBrain(baseBrain.BaseBrain):
		
	def step(self):
		if self.inputs["isCollision"]():
			ori = self.inputs["getOrientation"]()
			if ori == player.Player.ORIENTATION_LEFT:
				ori = player.Player.ORIENTATION_UP
			else:
				ori += 1
			self.outputs["setOrientation"](ori)
		else:
			self.outputs["move"]()
			
	def isFinished(self):
		return False