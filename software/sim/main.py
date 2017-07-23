#!/usr/bin/python

import sim
import os
import sys

MAPFILE_DIR = "maps"
MAPFILE_NAME_STARTSWITH = "test-room"
INVALID_MAPS = ["test-room0-empty.txt"]

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

def launchSim(brainClass, gameMapFile):
    s = sim.Sim(gameMapFile, brainClass)
    s.run()
    rep = s.getReport()
    return rep

def launchSimForAllMaps(brainClassPath, mapFileDir, mapFileNameStartsWith, excludeMaps):
    brainClass = loadClass(brainClassPath)
    if not brainClass:
        sys.exit(2)

    print "Testing brain \"%s\"" % brainClassPath
    print "Using maps from directory \"%s\" (excluding %s)" % (mapFileDir, excludeMaps)

    # for each map

    for entry in os.listdir(mapFileDir):
        if not entry.startswith(mapFileNameStartsWith):
            continue
        if entry in excludeMaps:
            continue
        gameMapFile = os.path.join(mapFileDir, entry)

        # execute simulator

        rep = launchSim(brainClass, gameMapFile)
        print "Sim executed %d steps on map %s" % (rep['stepCount'], rep['gameMapFile'])

def main():
    if len(sys.argv) == 1:
        print "USAGE: %s <roomDetectionBrain-moduleName.ClassName>" % sys.argv[0]
        sys.exit(1)
    brainClassPath = sys.argv[1]

    mapFileDir              = MAPFILE_DIR
    mapFileNameStartsWith   = MAPFILE_NAME_STARTSWITH
    invalidMaps             = INVALID_MAPS

    launchSimForAllMaps(brainClassPath, mapFileDir, mapFileNameStartsWith, invalidMaps)

    print "Finished simulation for all maps."

if __name__ == '__main__':
    main()
