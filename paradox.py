from classes.Interfacer import Interfacer
from classes.Webserver import Webserver
import os, sys
from const import *
from threading import Thread
import signal
import time


if len(sys.argv) > 1:
	for i in range(1,len(sys.argv)):
		if sys.argv[i] == "-v":
			globals.Verbose = True
		else:
			print "Unknown argument " + sys.argv[i]
			exit()


inter = Interfacer(IP_ADDR, TCP_PORT, USER_CODE, PASSWORD, VERBOSE_LEVEL, PARSER_ZONES_IDENTIFIER, PARSER_AREAS_IDENTIFIER,
	PARSER_SES_IDENTIFIER, PARSER_STATUS_IDENTIFIER, PARSER_STATES_IDENTIFIER, KEEP_ALIVE_ALLOWED_ERRORS)
web = Webserver(WEBSERVER_HOST, WEBSERVER_PORT, inter, VERBOSE_LEVEL)
th1 = Thread(target=web.listen_http)
th2 = Thread(target=inter.run, args=(LOGIN_MAX_RETRY, READY_WAIT_TIME, STATUS_INTERVAL))

th1.start();
th2.start();

run = True

while (run):
	if th1.isAlive():
		if not th2.isAlive():
			th2 = Thread(target=inter.run, args=(LOGIN_MAX_RETRY, READY_WAIT_TIME, STATUS_INTERVAL))
			th2.run()
	else:
		if th2.isAlive():
			inter.running = False
		run = False
	time.sleep(1)

