import os
import sim

class SimulatorLauncher():

	def launchSim(self):
		rep = {}
		return rep

	def launchSimForAllMaps(self, brainClassPath,
					mapFiles, excludeMaps,
					timeOut, delay,
					follow, verbose,
					position, orientation):
		rv = 0
		for mf_path in mapFiles:
			mapFileDir, mf = os.path.split(mf_path)
			if mf in excludeMaps:
				continue
			gameMapFile = os.path.join(mapFileDir, mf)
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
			if not entry.endswith("Brain.py"):
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

	@staticmethod
	def isValidStartPosition(posStr):
		if posStr == "random" or posStr == "rand":
			return True
		pos = posStr.split(",")
		if len(pos) == 2 and int(pos[0]) > 0 and int(pos[1]) > 0:
			return True
		return False

	@staticmethod
	def isValidStartOrientation(oriStr):
		if oriStr == "random" or oriStr == "rand":
			return True
		if oriStr in ["up", "right", "down", "left"]:
			return True
		return False
