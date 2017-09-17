import os
import sim
import baseBrain

class SimulatorLauncher():

	RAND_STRINGS = ["random", "rand"]

	def launchSim(self):
		rep = {}
		return rep

	def launchSimForAllMaps(self, brainClassPath,
					mapFiles,
					timeOut, delay,
					follow, verbose,
					position, orientation):
		rv = 0
		for gameMapFile in mapFiles:
			rep = self.launchSim(gameMapFile, brainClassPath, timeOut, delay, follow, verbose, position, orientation)
			if rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH:
				rv = 1
		return rv

	@staticmethod
	def loadClass(classPath):
		moduleName = classPath.split(".")[0]
		className = classPath.split(".")[1]
		moduleObj = __import__(moduleName)
		classObj = getattr(moduleObj, className)
		return classObj

	@staticmethod
	def findBrainClasses(brainDir):
		brains = []
		for entry in os.listdir(brainDir):
			if not entry.endswith(baseBrain.BaseBrain.FILENAME_ENDSWITH):
				continue
			moduleName = entry.split(".")[:-1][0]
			className = moduleName[0].upper() + moduleName[1:]
			classPath = moduleName + "." + className
			brains.append(classPath)
		return brains

	@staticmethod
	def findMapFiles(mapDir, mapFileNameStartsWith=None, excludeMaps=[]):
		maps = []
		for entry in sorted(os.listdir(mapDir)):
			if mapFileNameStartsWith and not entry.startswith(mapFileNameStartsWith):
				continue
			if len(excludeMaps) > 0 and entry in excludeMaps:
				continue
			maps.append(os.path.join(mapDir,entry))
		return maps

	@classmethod
	def isValidStartPosition(cls, posStr):
		if posStr in cls.RAND_STRINGS:
			return True
		pos = posStr.split(",")
		if len(pos) == 2 and int(pos[0]) > 0 and int(pos[1]) > 0:
			return True
		return False

	@classmethod
	def isValidStartOrientation(cls, oriStr):
		if oriStr in cls.RAND_STRINGS:
			return True
		if oriStr in baseBrain.BaseBrain.ORIENTATION_STR:
			return True
		return False
