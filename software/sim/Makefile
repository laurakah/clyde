DELAY=250
TIMEOUT=200

default: all

all: test

test:
	for t in *Test.py; do python $$t ; done
vtest:
	for t in *Test.py; do python $$t -v; done
sim:
	python main.py -v
vsim:
	python main.py -f -d $(DELAY) -t $(TIMEOUT)
clean:
	$(RM) -f *.pyc
