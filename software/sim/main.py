#!/usr/bin/python

import simLauncher
import sim
import coord
import baseBrain
import os
import sys
from optparse import OptionParser

MAPFILE_DIR = "maps"	# TODO move to Sim()
MAPFILE_NAME_STARTSWITH = "test-room"
INVALID_MAPS = ["test-room0-empty.txt", "test-room0.1-open.txt"]
BRAIN_DIR = "."
INVALID_BRAINS = ["baseBrain.BaseBrain", "dullBrain.DullBrain"]

slCls = simLauncher.SimulatorLauncher

def positionStrToValue(positionStr):
	if positionStr in slCls.RAND_STRINGS:
		position = None
	elif len(positionStr.split(",")) == 2:
		xyArr = positionStr.split(",")
		# TODO Move string to coordinate parsing into Coordinate class
		x = int(xyArr[0])
		y = int(xyArr[1])
		position = coord.Coordinate(x, y)
		# TODO might check if coordinate is within game map (requires creating a game map obj)
	else:
		sys.stderr.write("ERROR: Failed to parse coordinate \"%s\"!\n" % positionStr)
		sys.exit(1)
	return position

def orientationStrToValue(orientationStr):
	oriValues = baseBrain.BaseBrain.ORIENTATION_STR
	if orientationStr in slCls.RAND_STRINGS:
		orientation = None
	elif orientationStr in oriValues:
		orientation = oriValues.index(orientationStr)
	else:
		sys.stderr.write("ERROR: Invalid orientation \"%s\"!\n" % orientationStr)
		sys.exit(1)
	return orientation

def launchSimForAllBrains(brainsToTest, invalidBrains, mapsToTest,
				timeout, delay, follow, verbose,
				positionStr, orientationStr):

	# execute sim for list of brains (list might contain only one brain)

	for brainClassPath in brainsToTest:

		# skip specific brains

		if brainClassPath in invalidBrains:
			continue

		# load the brain class

		try:
			brainClassPath = slCls.loadClass(brainClassPath)
		except ImportError:
			sys.stderr.write("ERROR: modules does not exist!")
			sys.exit(1)
		except AttributeError:
			sys.stderr.write("ERROR: class does not exist!")
			sys.exit(1)

		if not brainClassPath:
			rv = 2
			sys.exit(rv)

		if verbose:
			print "Testing brain \"%s\"" % brainClassPath

		sl = slCls()
		sl.launchSim = launchSim	# install our non-TDD launchSim() over the currently stubbed one
		try:
			rv = sl.launchSimForAllMaps(brainClassPath, mapsToTest, timeout, delay, follow, verbose, positionStr, orientationStr)
		except KeyboardInterrupt:
			sys.stdout.write("\nInterrupted by user ... shutting down!")
			break

def launchSim(gameMapFile, brainClass, timeout, delay, follow, verbose, positionStr, orientationStr):
	brainName = brainClass.__name__.split(".")[-1]
	mapName = os.path.split(gameMapFile)[-1]

	msg_start = "%s %s ..." % (brainName, mapName)
	if (verbose):
		sys.stdout.write(msg_start)

	# transform position and orientation strings into objects

	position = positionStrToValue(positionStr)
	orientation = orientationStrToValue(orientationStr)

	# setup sim

	s = sim.Sim(gameMapFile, brainClass, timeout, delay, follow, position, orientation)
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
		msg_end += " (start at x %d y %d ori. %d)" % (startPos.x, startPos.y, startOri)
		sys.stdout.write(msg_end)

	if verbose or (not verbose and rep['exitCode'] != sim.Sim.EXITCODE_MAPMATCH):
		sys.stdout.write("\n")

	return rep

def prologue(verbose, mapFileDir, invalidMaps, brainDir, invalidBrains, posStr, oriStr):
	if not verbose:
		return
	print "Using maps from directory \"%s\" (excluding %s)" % (mapFileDir, invalidMaps)
	print "Using brains from directory \"%s\" (excluding %s)" % (brainDir, invalidBrains)
	print "Using start position \"%s\" and start orientation \"%s\"" % (posStr, oriStr)

def epilogue(verbose):
	if not verbose:
		return
	print "Finished simulation for all maps."

def parse_argv():
	default_verbose		= False
	default_timeout		= sim.Sim.DEFAULT_TIMEOUT
	default_delay		= 0
	default_mapfile_dir	= MAPFILE_DIR
	default_brain_dir	= BRAIN_DIR
	default_follow		= False
	default_position	= "random"
	default_orientation	= "random"

	parser = OptionParser()
	parser.add_option("-v", "--verbose", dest="verbose", default=default_verbose, action="store_true",
				help="show what is going on")
	parser.add_option("-t", "--timeout", dest="timeout", default=default_timeout,
				help="override step timeout")
	parser.add_option("-d", "--delay", dest="delay",
				help="set delay for step execution in milliseconds", default=default_delay)
	parser.add_option("-m", "--mapdir", dest="mapdir",
				help="set alternative directory to look for maps", default=default_mapfile_dir)
	parser.add_option("-b", "--braindir", dest="braindir",
				help="set alternative directory to look for brains", default=default_brain_dir)
	parser.add_option("-f", "--follow", dest="follow", default=default_follow, action="store_true",
				help="draw map with player position for each simulator step")
	parser.add_option("-p", "--position", dest="position", default=default_position,
				help="control start position behavior. can be \"random\" or \"x,y\" (default: random)")
	parser.add_option("-o", "--orientation", dest="orientation", default=default_orientation,
				help="control start orientation behavior can be \"random\", \"up\", \"right\", \"down\" or \"left\" (default: random)")
	return parser.parse_args()

def parse_arguments(args):
	brainsToTest = []
	mapsToTest = []
	if len(args) == 0:
		return (brainsToTest, mapsToTest)
	for argument in args:
		if argument.endswith("Brain"):
			brainsToTest.append(argument)
		elif argument.endswith(".txt"):
			mapsToTest.append(argument)
		else:
			sys.stderr.write("ERROR: Can't handle argument \"%s\"!\n" % argument)
			sys.exit(1)
	return (brainsToTest, mapsToTest)

def main():
	rv = 0

	(options, args) = parse_argv()
	(brainsToTest, mapsToTest) = parse_arguments(args)

	verbose			= options.verbose
	mapFileDir		= options.mapdir
	mapFileNameStartsWith	= MAPFILE_NAME_STARTSWITH
	invalidMaps		= INVALID_MAPS
	brainDir		= options.braindir
	invalidBrains		= INVALID_BRAINS
	timeout			= int(options.timeout)
	delay			= int(options.delay)
	follow			= options.follow
	positionStr		= options.position
	orientationStr		= options.orientation

	if len(brainsToTest) == 0:
		brainsToTest = slCls.findBrainClasses(brainDir)
	if len(mapsToTest) == 0:
		mapsToTest = slCls.findMapFiles(mapFileDir, mapFileNameStartsWith, invalidMaps)

	print "=" * 72
	print "brains to test: %s" % brainsToTest
	print "maps to test: %s" % mapsToTest
	print "=" * 72

	if positionStr and not slCls.isValidStartPosition(positionStr):
		sys.stderr.write("ERROR: invalid start position!\n")
		sys.exit(1)
	if orientationStr and not slCls.isValidStartOrientation(orientationStr):
		sys.stderr.write("ERROR: invalid start orientation!\n")
		sys.exit(1)

	prologue(verbose, mapFileDir, invalidMaps, brainDir, invalidBrains, positionStr, orientationStr)

	launchSimForAllBrains(brainsToTest, invalidBrains, mapsToTest,
				timeout, delay, follow, verbose,
				positionStr, orientationStr)

	epilogue(verbose)

	sys.exit(rv)

if __name__ == '__main__':
    main()
