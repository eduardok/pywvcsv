
.PHONY: all

all: _wvcsv.so

_wvcsv.so: wvcsv.cc _wvcsvmodule.cc setup.py
	@python setup.py build
	@cp build/*/_wvcsv.so .
	
tests: all

runtests: tests
	./wvtest.py $(wildcard t/t*.py)
	
test:
	./wvtestrun $(MAKE) runtests

clean:
	rm -rf build _wvcsv.so *.pyc t/*.pyc .*~ *~
