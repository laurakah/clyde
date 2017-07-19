class GameMap():
	
	EMPTY_FIELD = " "
	COLLISION_FIELD = "#"
	
	def __init__(self, mapFile = None):
		if mapFile:
			self.m = GameMap.readMapFile(mapFile)
		else:
			self.m = []
	
	@staticmethod
	def readMapFile(mapFile):
		m = []
		txt = []
		f = open(mapFile)
		for line in f.readlines():
			txt.append(line)
		f.close()
		for line in txt:
			fields = []
			for c in line:
				if c == GameMap.COLLISION_FIELD:
					fields.append(1)
				if c == GameMap.EMPTY_FIELD:
					fields.append(0)
			m.append(fields)
		return m
	
	def getMap(self):
		return self.m