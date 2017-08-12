#!/usr/bin/python

import simLauncher
import sim
import os
import sys
from optparse import OptionParser

MAPFILE_DIR = "maps"	# TODO move to Sim()
MAPFILE_NAME_STARTSWITH = "test-room"
INVALID_MAPS = ["test-room0-empty.txt", "test-room0.1-open.txt"]
BRAIN_DIR = "."
INVALID_BRAINS = ["baseBrain.BaseBrain", "dullBrain.DullBrain"]

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

def launchSim(brainClass, gameMapFile, timeout, delay, follow, verbose):
	s = sim.Sim(gameMapFile, brainClass, timeout, delay, follow)

	brainName = brainClass.__name__.split(".")[-1]
	mapName = os.path.split(gameMapFile)[-1]
	msg_start = "%s %s ..." % (brainName, mapName)
	if (verbose):
		sys.stdout.write(msg_start)

	s.run()
	rep = s.getReport()

	if rep['exitCode'] == sim.Sim.EXITCODE_TIMEOUT:
		exitCodeMsg = "timeout!"
	elif rep['exitCode'] == sim.Sim.EXITCODE_MAPMISSMATCH:
		exitCodeMsg = "map missmatch!"
	elif rep['exitCode'] == sim.Sim.EXITCODE_MAPMATCH:
		exitCodeMsg = "success!"
	else:
		exitCodeMsg = "failure (unknown code %d)" % rep['exitCode']

	msg_end = ""
	if not verbose and rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH:
		msg_end = msg_start

	if verbose or rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH:
		startPos = s.getStartPosition()
		startOri = s.getStartOrientation()
		msg_end += " %s" % exitCodeMsg
		msg_end += " (start at x %d y %d ori. %d)" % (startPos['x'], startPos['y'], startOri)
		sys.stdout.write(msg_end)

	if verbose or (not verbose and rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH):
		sys.stdout.write("\n")

	return rep

def launchSimForAllMaps(brainClassPath, mapFileDir, mapFileNameStartsWith, excludeMaps,
			timeout, delay, follow, verbose):
	# default return value (0 is 'everything is fine')
	rv = 0

	# for each map

	for entry in sorted(os.listdir(mapFileDir)):
		if not entry.startswith(mapFileNameStartsWith):
			continue
		if entry in excludeMaps:
			continue
		gameMapFile = os.path.join(mapFileDir, entry)

		# execute simulator

		rep = launchSim(brainClassPath, gameMapFile, timeout, delay, follow, verbose)

		# set return value to 1 if there was a problem
		if rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH:
			rv = 1
	return rv

def prologue(verbose, mapFileDir, invalidMaps, brainDir, invalidBrains):
	if not verbose:
		return
	print "Using maps from directory \"%s\" (excluding %s)" % (mapFileDir, invalidMaps)
	print "Using brains from directory \"%s\" (excluding %s)" % (brainDir, invalidBrains)

def epilogue(verbose):
	if not verbose:
		return
	print "Finished simulation for all maps."

def main():
	rv = 0

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
	parser.add_option("-f", "--follow", dest="follow", default=False, action="store_true",
				help="draw map with player position for each simulator step")
	(options, args) = parser.parse_args()

	brainsToTest = []
	if len(args) > 0:
		brainsToTest.extend(args)
	else:
		brainsToTest = simLauncher.SimulatorLauncher.findBrainClasses(BRAIN_DIR)

	verbose			= options.verbose
	mapFileDir		= options.mapdir
	mapFileNameStartsWith	= MAPFILE_NAME_STARTSWITH
	invalidMaps		= INVALID_MAPS
	brainDir		= options.braindir
	invalidBrains		= INVALID_BRAINS
	timeout			= int(options.timeout)
	delay			= int(options.delay)
	follow			= options.follow

	prologue(verbose, mapFileDir, invalidMaps, brainDir, invalidBrains)

	for brainClassPath in brainsToTest:
		ignoreBrain = False
		for brainClassPathToIgnore in invalidBrains:
			if brainClassPath == brainClassPathToIgnore:
				ignoreBrain = True
		if ignoreBrain:
			continue

		brainClassPath = loadClass(brainClassPath)
		if not brainClassPath:
			rv = 2
			sys.exit(rv)

		if verbose:
			print "Testing brain \"%s\"" % brainClassPath

		rv = launchSimForAllMaps(brainClassPath, mapFileDir, mapFileNameStartsWith, invalidMaps, timeout, delay, follow, verbose)

	epilogue(verbose)

	sys.exit(rv)

if __name__ == '__main__':
    main()
