import socket
import re
from Queue import Queue
import globals
from globals import *
import time
import json


def listen_http(queue, mutex):
    from interfacer import desarm
    from interfacer import arm
    from interfacer import partiel
    # Standard socket stuff:
    host = '' # do we need socket.gethostname() ?
    port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1) # don't queue up any requests
    # Loop forever, listening for requests:
    zones = False
    areas = True
    run = True
    while run:
        csock, caddr = sock.accept()
        req = csock.recv(1024) # get the request, 1kB max
        # Look in the first line of the request for a move command
        # A move command should be e.g. 'http://server/move?a=90'
        updated = False;
        mutex.acquire()
        if not queue.empty():
            picked = queue.get()
            zones = picked[0]
            areas = picked[1]
            updated = True
        mutex.release()
        if re.match('GET /description', req):
            if globals.Verbose:
                print '\033[94m' + "* <WEBSERVER> : GET /description" + '\033[0m'
            string = ""
            c = 0
            for i in range(0,len(zones)):
                if zones[i]["active"]:
                    string += str(c) + " => " + str(zones[i]["name"]) + "\n"
                    c+=1
            csock.sendall(string);
        elif re.match('GET /status', req):
            if globals.Verbose:
                print '\033[94m' + "* <WEBSERVER> : GET /status" + '\033[0m'
            status = {"state":areas[0]["armed"], "detectors":[]}
            c = 0
	    for e in zones:
                if e["active"]:
                    status["zone-"+str(c)] = e["status"]
		    c+=1
            csock.sendall(json.dumps(status))
        elif re.match('GET /arm', req):
            if globals.Verbose:
                print '\033[94m' + "* <WEBSERVER> : GET arm" + '\033[0m'
            arm()
	    csock.sendall("Armed")
        elif re.match('GET /desarm', req):
            if globals.Verbose:
                print '\033[94m' + "* <WEBSERVER> : GET /desarm" + '\033[0m'
            desarm()
	    csock.sendall("Desarm")
        elif re.match('GET /partiel', req):
            if globals.Verbose:
                print '\033[94m' + "* <WEBSERVER> : GET /partiel" + '\033[0m'
	    partiel()
            csock.sendall("Partiel")
        elif re.match('GET /stop', req):
            run = False
            if globals.Verbose:
                print '\033[94m' + "* <WEBSERVER> : GET /stop" + '\033[0m'
            csock.sendall("Okay.")
        else:
            # If there was no recognised command then return a 404 (page not found)
            #print "Returning 404"
            csock.sendall("HTTP/1.0 404 Not Found\r\n")
        csock.close()
