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

def launchSim(gameMapFile, brainClass, timeout, delay, follow, verbose, position, orientation):
	brainName = brainClass.__name__.split(".")[-1]
	mapName = os.path.split(gameMapFile)[-1]

	msg_start = "%s %s ..." % (brainName, mapName)
	if (verbose):
		sys.stdout.write(msg_start)

	# setup sim

	s = sim.Sim(gameMapFile, brainClass, timeout, delay, follow)
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
	parser.add_option("-p", "--position", dest="position", default="random",
				help="control start position behavior. can be \"random\" or \"x,y\" (default: random)")
	parser.add_option("-o", "--orientation", dest="orientation", default="random",
				help="control start orientation behavior can be \"random\", \"up\", \"right\", \"down\" or \"left\" (default: random)")
	(options, args) = parser.parse_args()

	brainsToTest = []
	mapsToTest = []
	if len(args) > 0:
		for argument in args:
			if argument.endswith("Brain"):
				brainsToTest.append(argument)
			elif argument.endswith(".txt"):
				mapsToTest.append(argument)
			else:
				sys.stderr.write("ERROR: Can't handle argument \"%s\"!\n" % argument)
				sys.exit(1)

	if len(brainsToTest) == 0:
		brainsToTest = simLauncher.SimulatorLauncher.findBrainClasses(BRAIN_DIR)
	if len(mapsToTest) == 0:
		mapsToTest = simLauncher.SimulatorLauncher.findMapFiles(MAPFILE_DIR, MAPFILE_NAME_STARTSWITH, INVALID_MAPS)

	print "=" * 72
	print "brains to test: %s" % brainsToTest
	print "maps to test: %s" % mapsToTest
	print "=" * 72

	verbose			= options.verbose
	mapFileDir		= options.mapdir
	mapFileNameStartsWith	= MAPFILE_NAME_STARTSWITH
	invalidMaps		= INVALID_MAPS
	brainDir		= options.braindir
	invalidBrains		= INVALID_BRAINS
	timeout			= int(options.timeout)
	delay			= int(options.delay)
	follow			= options.follow
	position		= options.position
	orientation		= options.orientation

	if position and not simLauncher.SimulatorLauncher.isValidStartPosition(position):
		sys.stderr.write("ERROR: invalid start position!\n")
		sys.exit(1)
	if orientation and not simLauncher.SimulatorLauncher.isValidStartOrientation(orientation):
		sys.stderr.write("ERROR: invalid start orientation!\n")
		sys.exit(1)

	prologue(verbose, mapFileDir, invalidMaps, brainDir, invalidBrains, position, orientation)

	# execute sim for list of brains (list might contain only one brain)

	for brainClassPath in brainsToTest:

		# skip specific brains

		ignoreBrain = False
		for brainClassPathToIgnore in invalidBrains:
			if brainClassPath == brainClassPathToIgnore:
				ignoreBrain = True
		if ignoreBrain:
			continue

		# load the brain class

		try:
			brainClassPath = simLauncher.SimulatorLauncher.loadClass(brainClassPath)
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

		sl = simLauncher.SimulatorLauncher()
		sl.launchSim = launchSim	# install our non-TDD launchSim() over the currently stubbed one
		try:
			rv = sl.launchSimForAllMaps(brainClassPath, mapsToTest, mapFileNameStartsWith, invalidMaps, timeout, delay, follow, verbose, position, orientation)
		except KeyboardInterrupt:
			sys.stdout.write("\nInterrupted by user ... shutting down!")
			return

	epilogue(verbose)

	sys.exit(rv)

if __name__ == '__main__':
    main()
