#!/usr/bin/python

# TODO test all brains when no brain passed
# TODO make brain argument optional (test all brains in default brain directory)
# TODO implement sim.draw() (in sim duh)

import sim
import os
import sys
from optparse import OptionParser

MAPFILE_DIR = "maps"	# TODO move to Sim()
MAPFILE_NAME_STARTSWITH = "test-room"
INVALID_MAPS = ["test-room0-empty.txt", "test-room0.1-open.txt"]
BRAIN_DIR = "brains"

def loadClass(classPath):
	moduleName = classPath.split(".")[0]
	className = classPath.split(".")[1]
	# check module exists. if so, load it
	if not os.path.exists("%s.py" % moduleName):
		print "ERROR: module does not exist!"
		return None
	moduleObj = __import__(moduleName)
	try:
		classObj = getattr(moduleObj, className)
	except AttributeError:
		print "ERROR: class does not exist!"
		return None
	return classObj

def launchSim(brainClass, gameMapFile, timeout, delay):
	s = sim.Sim(gameMapFile, brainClass, timeout, delay)
	s.run()
	rep = s.getReport()
	return rep

def launchSimForAllMaps(brainClassPath, mapFileDir, mapFileNameStartsWith, excludeMaps,
			timeout, delay, verbose):
	brainClass = loadClass(brainClassPath)
	if not brainClass:
		sys.exit(2)

	# default return value (0 is 'everything is fine')
	rv = 0

	if (verbose):
		print "Testing brain \"%s\"" % brainClassPath
		print "Using maps from directory \"%s\" (excluding %s)" % (mapFileDir, excludeMaps)

	# for each map

	for entry in sorted(os.listdir(mapFileDir)):
		if not entry.startswith(mapFileNameStartsWith):
			continue
		if entry in excludeMaps:
			continue
		gameMapFile = os.path.join(mapFileDir, entry)

		# execute simulator

		rep = launchSim(brainClass, gameMapFile, timeout, delay)
		if rep['exitCode'] == sim.Sim.EXITCODE_TIMEOUT:
			exitCodeMsg = "failure (timeout)!"
		elif rep['exitCode'] == sim.Sim.EXITCODE_MAPMISSMATCH:
			exitCodeMsg = "failure (map missmatch)!"
		elif rep['exitCode'] == sim.Sim.EXITCODE_MAPMATCH:
			exitCodeMsg = "success (map matched)!"
		else:
			exitCodeMsg = "failure (unknown code %d)" % rep['exitCode']

		# set return value to 1 if there was a problem
		if rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH:
			rv = 1

		if verbose or rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH:
			print "%s - %s with %d steps in %s" % (exitCodeMsg, brainClassPath, rep['stepCount'], os.path.split(rep['gameMapFile'])[-1])
	return rv

def main():
	parser = OptionParser()
	parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
				help="show what is going on")
	parser.add_option("-t", "--timeout", dest="timeout", default=sim.Sim.DEFAULT_TIMEOUT,
				help="override step timeout")
	parser.add_option("-d", "--delay", dest="delay",
				help="set delay for step execution in milliseconds", default=0)
	parser.add_option("-m", "--mapdir", dest="mapdir",
				help="set alternative directory to look for maps", default=MAPFILE_DIR)
	parser.add_option("-b", "--braindir", dest="braindir",
				help="set alternative directory to look for brains", default=BRAIN_DIR)

	(options, args) = parser.parse_args()

	if len(args) == 0:
		print "USAGE: %s <roomDetectionBrain-moduleName.ClassName>" % sys.argv[0]
		sys.exit(1)

	brainClassPath = args[0]

	verbose			= options.verbose
	mapFileDir		= options.mapdir
	mapFileNameStartsWith	= MAPFILE_NAME_STARTSWITH
	invalidMaps		= INVALID_MAPS
	brainDir		= options.braindir
	timeout			= int(options.timeout)
	delay			= int(options.delay)

	# TODO have launchSimForAllBrains() on braindir

	rv = launchSimForAllMaps(brainClassPath, mapFileDir, mapFileNameStartsWith, invalidMaps, timeout, delay, verbose)

	if verbose:
		print "Finished simulation for all maps."
	sys.exit(rv)

if __name__ == '__main__':
    main()
