default: all

all: test

test:
	python playerTest.py
	python gameMapTest.py
	python simTest.py
	python baseRoomDetectionBrainTest.py
	python simLauncher.py

sim:
	python main.py baseRoomDetectionBrain.BaseRoomDetectionBrain

clean:
	$(RM) -f *.pyc
