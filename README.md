# pyMOOS

Python bindings for the [Mission Oriented Software Suite (MOOS)](http://www.robots.ox.ac.uk/~mobile/MOOS/wiki/pmwiki.php), developed at Oxford University and hosted on [GitHub](https://github.com/themoos).


## Changelog

* **v2020.01**
  * Fixed CMake to use whatever version of Python 3 available on the system.
  * Added binary message data type support.
  * Clean up code (clang-format and black).
* **v2019.07**
  * Forked https://github.com/davidhodo/pymoos
  * Updated to latest MOOS API (10.5.0)
  * Fixed CMake to find MOOS libs
  * Updated to Python 3.7


## Dependencies

* MOOS Core
* Python 3
* Boost libraries (Boost Python compiled against Python 3)

Newer Ubuntu installations ship with both 2.7 and 3 versions of the Boost Python library.  For older versions (or other OS's) Boost Python must be compiled and linked against Python 3.

### Building MOOS
The pymoos bindings require that the core MOOS packages be installed:

	git clone https://github.com/themoos/core-moos.git
	cd core-moos
	mkdir build
	cd build
	cmake ..
	make


## Building and Installation

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

## History 
The `pymoos` bindings were originally written by [Ian Baldwin](http://sourceforge.net/projects/pymoos/) and then fixed up by [David Hodo](https://github.com/davidhodo/pymoos), but this repository hasn't seen an update in some years.