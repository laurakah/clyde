import os

class SimulatorLauncher():

	def launchSim(self):
		return

	def launchSimForAllMaps(self, mapFileDir):
		for mf in os.listdir(mapFileDir):
			self.launchSim()

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
