
.PHONY: all

all: pywvcsv.so

pywvcsv.so: ../cli/wvcsv.cc pywvcsvmodule.cc setup.py
	@python setup.py build
	@cp build/*/pywvcsv.so .

clean:
	rm -rf build pywvcsv.so *.pyc t/*.pyc .*~ *~
