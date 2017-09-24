DELAY=250
TIMEOUT=200

default: all

all: test

test:
	python -m unittest discover -p"*Test.py"
vtest:
	python -m unittest discover -p"*Test.py" -v
sim:
	python main.py -v
vsim:
	python main.py -f -d $(DELAY) -t $(TIMEOUT)
clean:
	$(RM) -f *.pyc
