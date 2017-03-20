import os,sys
import globals
from interfacer import paradox_connector

globals.Verbose = False;

if len(sys.argv) > 1:
	for i in range(1,len(sys.argv)):
		if sys.argv[i] == "-v":
			globals.Verbose = True
		else:
			print "Unknown argument " + sys.argv[i]
			exit()
paradox_connector() # starting Paradox interfacer
