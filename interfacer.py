import sys,os
import urllib2
from core_functions import *
from const import *
from parser import *
import random
import time
from threading import Thread
from threading import Lock
from Queue import Queue
import thread
import globals;
from globals import *
from webserver import listen_http

def paradox_connector():
	global Zones
	global Areas
	a = 1
	queue = Queue()
	mutex = Lock()

	if globals.Verbose:
		print '\033[94m' +  "* <INTERFACER> : VERBOSE mode activated" + '\033[0m'

	#web_thread = Thread(target = listen_http, args = (queue, ))

	print '\033[94m' + "* <INTERFACER> : Login to IP150..." + '\033[0m'
	loop_connect()

	print '\033[94m' + "* <INTERFACER> : Launching keep alive thread..." + '\033[0m'
	thread.start_new_thread(keep_alive, ())

	print '\033[94m' + "* <INTERFACER> : Retriving equipment..." + '\033[0m'
	equipment = get_equipment()
	if not equipment:
		raise ValueError('Error while retriving equipment informations')
	Zones = equipment[0]
	Areas = equipment[1]
	

	# Launch web server
	print '\033[94m' + "* <INTERFACER> : Starting HTTP Server" + '\033[0m'
	th = Thread(target=listen_http, args=(queue,mutex))
	th.start()
	# Loop update
	i = 0
	while (1):
		a = update_status(queue, mutex)
		time.sleep(STATUS_INTERVAL)

	print '\033[94m' + "* <INTERFACER> : Loging out of IP150..." + '\033[0m'
	logout()

def do_request(location):
	html = urllib2.urlopen("http://" + IP_ADDR + ":" + str(TCP_PORT) + "/" + location).read()
	if globals.Verbose:
		print '\033[94m' + "* <INTERFACER> : Making request to /" + location + '\033[0m'
		print html
	return html

def get_status():
	return {"test":"1"}

def arm():
	do_request("statuslive.html?area=00&value=r")

def desarm():
	do_request("statuslive.html?area=00&value=d")

def partiel():
	do_request("statuslive.html?area=00&value=s")

def login():
	html = do_request("login_page.html")
	js = js_from_html(html)
	print '\033[94m' + "* <INTERFACER> : Looking for someone connected..." + '\033[0m'
	if someone_connected(js):
		raise ValueError('Unable to login : someone is already connected')
	ses = parse_ses(js)
	if ses == False:
		raise ValueError('Unable to login : No SES value found')
	print '\033[94m' + "* <INTERFACER> : SES Value found, encrypting credentials..." + '\033[0m'
	credentials = login_encrypt(ses)
	print '\033[94m' + "* <INTERFACER> : Sending auth request..." + '\033[0m'
	html = do_request("default.html?u=" + str(credentials['user']) + "&p=" + str(credentials['password']))

def logout():
	do_request("logout.html")

def loop_connect():
	retry 	= True
	i 		= 0
	while retry: 
		try:
			login()
			retry = False
		except:
			i += 1
			if (i < LOGIN_MAX_RETRY):
				print '\033[94m' + "* <INTERFACER> : Unable to login, someone is probably already connected, waiting " + str(LOGIN_WAIT_TIME_START * LOGIN_WAIT_TIME_MULT * i) + " seconds before retring..." + '\033[0m'
				time.sleep(LOGIN_WAIT_TIME_START * LOGIN_WAIT_TIME_MULT * i)
			else:
				print '\033[94m' + "* <INTERFACER> : /!\ Sorry, " + str(i) + " login failure, I will stop now..." + '\033[0m'
				raise ValueError('Unable to login after ' + str(i) + ' attempts.')
	retry = True
	while retry:
		try:
			do_request("index.html")
			print '\033[94m' + "* <INTERFACER> : Seems ready." + '\033[0m'
			retry = False
		except:
			print '\033[94m' + "* <INTERFACER> : Not yet ready..." + '\033[0m'
		time.sleep(READY_WAIT_TIME)


def get_status():
	html = do_request("statuslive.html")
	js = js_from_html(html)
	return parse_status(js)

def get_equipment():
	html = do_request("index.html")
	js = js_from_html(html)
	return parse_equipment(js)

def keep_alive():
	while (1):
		#generate random id
		rand = random.randint(1000000000000000,9999999999999999)
		#print "* <INTERFACER> : <<< KEEP ALIVE : msgid=1&" + str(rand) + " >>>"
		do_request("keep_alive.html?msgid=1&" + str(rand))
		time.sleep(2.5)

def update_status(queue, mutex):
	global Zones
	global Areas

	#print "* <INTERFACER> : Retriving status"
	status = get_status()
	if not status:
		raise ValueError('Error while retrieving status informations')
	states = status[1]
	status = status[0]
	if len(status) == len(Zones):
		#print "* <INTERFACER> : All okay, updating status"
		for i in range(0, len(status)):
			Zones[i]["status"] = status[i]
	else:
		print "* <INTERFACER> : /!\ Erf, status (" + str(len(status)) + ") != zones (" + str(len(Zones)) + " )..."

	if len(states) == len(Areas):
		#print "* <INTERFACER> : All okay, updating states"
		for i in range(0, len(states)):
			Areas[i]["armed"] = states[i]
			
		mutex.acquire()
		if not queue.empty():
			#print "* <INTERFACER> : Clearing the queue..."
			queue.queue.clear()
		#print "* <INTERFACER> : Putting updates in queue..."
		queue.put((Zones,Areas))
		mutex.release()
	else:
		print '\033[94m' + "* <INTERFACER> : /!\ Erf, states (" + str(len(states)) + ") != areas (" + str(len(Areas)) + " )..." + '\033[0m'


