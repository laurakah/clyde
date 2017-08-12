import baseRoomDetectionBrain

class TheseusBrain(baseRoomDetectionBrain.BaseRoomDetectionBrain):
		
	def step(self):
		if self.inputs["isCollision"]():
			ori = self.inputs["getOrientation"]()
			if ori == 3:
				ori = 0
			else:
				ori += 1
			self.outputs["setOrientation"](ori)
		self.outputs["move"]()