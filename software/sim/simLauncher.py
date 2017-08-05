class SimulatorLauncher():
	@staticmethod
	def loadClass(classPath):
		moduleName = classPath.split(".")[0]
		className = classPath.split(".")[1]
		moduleObj = __import__(moduleName)
		classObj = getattr(moduleObj, className)
		return classObj
