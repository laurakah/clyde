#!/usr/bin/python

import sim
import os
import sys

def main(brainClassPath, mapFileDir, excludeMaps):

    brainModule = brainClassPath.split(".")[0]
    brainClass = brainClassPath.split(".")[1]

    print "Testing brain \"%s\" with maps from directory \"%s\" (excluding %s)" % (brainClass, mapFileDir, excludeMaps)

    if not os.path.exists("%s.py" % brainModule):
        print "ERROR: brain module does not exist!"
        sys.exit(2)
    mod = __import__(brainModule)

    for entry in os.listdir(mapFileDir):
        if not entry.startswith("test-room"):
            continue
        if entry in excludeMaps:
            continue
        gameMapFile = os.path.join(mapFileDir, entry)
        s = sim.Sim(gameMapFile, getattr(mod, brainClass))
        s.run()
        rep = s.getReport()
        print "Sim executed %d steps on map %s" % (rep['stepCount'], rep['gameMapFile'])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "USAGE: %s <roomDetectionBrain-moduleName.ClassName>" % sys.argv[0]
        sys.exit(1)
    brainClassPath = sys.argv[1]
    mapFileDir = "maps"
    invalidMaps = ["test-room0-empty.txt"]
    main(brainClassPath, mapFileDir, invalidMaps)
