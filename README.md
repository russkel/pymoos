# PYMOOS - Python binds for MOOS

Python interface for the Mission Oriented Software Suite (MOOS), developed at Oxford University [http://www.robots.ox.ac.uk/~mobile/MOOS/wiki/pmwiki.php] and hosted on GitHub [https://github.com/themoos]

The pymoos bindings were originally written by Ian Baldwin and hosted at http://sourceforge.net/projects/pymoos/.

## Dependencies

The pymoos bindings require at a minimum that the core MOOS packages be installed.

	git clone https://github.com/themoos/core-moos.git
	cd core-moos
	mkdir build
	cd build
	cmake ..
	make

Boost Python compiled against Python3 is also required.  Newer Ubuntu installations ship with both 2.7 and 3 versions of the Boost Python library.  For older versions (or other OS's) Boost Python must be compiled and linked against Python 3.

## Installation

The pymoos bindings can be downloaded and installed by:

	git clone git@github.com:davidhodo/pymoos.git
	cd pymoos
	mkdir build
	cmake ../
	make
	sudo make install

The installation can be tested by:

	python3
	import pymoos.MOOSCommClient

If an import error occurs check that the installation directory (usually /usr/local/lib/python3/dist-packages on Ubuntu) is included in your PYTHONPATH.  If not it can be added by:

	export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3/dist-packages

## Example Usage

The following code snippet creates a MOOS comm client from Python and connects to a database hosted on the local machine.  From a Python3 interpreter, run:

	import pymoos.MOOSCommClient
	m = pymoos.MOOSCommClient.MOOSApp()
	m.Run( "127.0.0.1", 9000, "pymoos_test", 10)
