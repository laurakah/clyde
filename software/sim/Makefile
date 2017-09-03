DELAY=250
TIMEOUT=200

default: all

all: test

test:
	python playerTest.py
	python gameMapTest.py
	python simTest.py
	python baseBrainTest.py
	python dullBrainTest.py
	python simLauncherTest.py
	python theseusBrainTest.py
	python coordTest.py
	python simpleBrainTest.py

sim:
	python main.py -v
vsim:
	python main.py -f -d $(DELAY) -t $(TIMEOUT)
clean:
	$(RM) -f *.pyc
