import os

class SimulatorLauncher():
	@staticmethod
	def loadClass(classPath):
		moduleName = classPath.split(".")[0]
		className = classPath.split(".")[1]
		moduleObj = __import__(moduleName)
		classObj = getattr(moduleObj, className)
		return classObj

	@staticmethod
	def findBrainModules(brainDir):
		brains = []
		for entry in os.listdir(brainDir):
			if not entry.endswith("Brain.py"):
				continue
			brains.append(os.path.join(brainDir, entry))
		return brains
