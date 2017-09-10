from classes.Parser import Parser
from classes.Paracrypt import Paracrypt
from threading import Thread
import urllib2
import time
import random

class Interfacer:
	def __init__(self, ip, port, username, password, verbose_level, zones_identifier, 
		area_identifier, ses_identifier, status_identifier, states_identifier, keep_alive_allowed_errors):

		self.ip = ip
		self.port = str(port)
		self.username = str(username)
		self.password = str(password)
		self.connected = False
		self.verbose_level = verbose_level
		self.parser = Parser(self, zones_identifier, area_identifier, ses_identifier, status_identifier, states_identifier)
		self.current_status = "Init phase"
		self.paracrypt = Paracrypt(username, password)
		self.running = False
		self.keep_alive_allowed_errors = keep_alive_allowed_errors;
		self.keep_alive_errors = 0


	### Main method ###

	def run(self, login_max_try, ready_wait_time, update_time_interval):
		th = Thread(target=self.keep_alive)

		if not self.loop_login(login_max_try, ready_wait_time):
			return False
		self.connected = True
		equipment = self.get_equipment()
		if not equipment:
			return False
		print equipment
		self.zones = equipment[0]
		self.areas = equipment[1]
		self.update_status()
		self.running = True
		self.current_status = "Running"
		th.start()
		while self.running and self.connected:
			self.update_status()
			time.sleep(update_time_interval)
		running = False
		th.join()
		if self.connected:
			self.logout()



	### These methods provide some usefull features to help ###

	def display_message(self, msg, verbose_level):
		if verbose_level <= self.verbose_level:
			print '\033[94m' + "* <INTERFACER> : " + msg +  '\033[0m'
	def raise_error(self, msg):
		print '\033[94m' + "* <INTERFACER> : /!\ " + msg + '\033[0m'
		self.current_status = msg

	def do_request(self, location):
		try:
			html = urllib2.urlopen("http://" + self.ip + ":" + self.port + "/" + location, timeout=1).read()
			self.display_message("Making request to /" + location, 2)
			return html
		except Exception:
			self.raise_error('Unable to make request to /' + location)
			return False


	### Login/logout methods ###

	def loop_login(self, login_max_try, ready_wait_time):
		# Trying to connect
		retry = True
		i = 0
		while retry:
			if self.login():
				retry = False
			else:
				i += 1
				if (i == login_max_try):
					return False

		# Waiting for server to be ready
		while not self.do_request("index.html"):
			self.raise_error("Not yes ready...")
			time.sleep(ready_wait_time)
		self.display_message("Seems to be ready", 1)
		return True

	def login(self):
		html = self.do_request("login_page.html")
		if not html:
			return False
		js = self.parser.js_from_html(html)
		if not js:
			return False

		self.display_message("Looking for someone connected...", 1)
		if self.parser.someone_connected(js):
			self.raise_error('Unable to login : someone is already connected')
			time.sleep(30)
			return False

		ses = self.parser.parse_ses(js)
		if ses == False:
			self.raise_error('Unable to login : No SES value found')

		self.display_message('SES Value found, encrypting credentials...', 2)
		credentials = self.paracrypt.login_encrypt(ses)
		self.display_message('Sending auth request...', 2)

		html = self.do_request("default.html?u=" + str(credentials['user']) + "&p=" + str(credentials['password']))
		if not html:
			return False
		return True

	def logout(self):
		self.connected = False
		return self.do_request("logout.html")


	### Status/equipment methods ###

	def get_status(self):
		html = self.do_request("statuslive.html")
		if not html:
			return False
		js = self.parser.js_from_html(html)
		if not js:
			return False
		return self.parser.parse_status(js)

	def get_equipment(self):
		html = self.do_request("index.html")
		if not html:
			return False
		js = self.parser.js_from_html(html)
		if not js:
			return False
		return self.parser.parse_equipment(js)


	def update_status(self):
		status = self.get_status()
		if not status:
			return False
		states = status[1]
		status = status[0]
		if len(status) == len(self.zones):
			for i in range(0, len(status)):
				self.zones[i]["status"] = status[i]
		else:
			self.raise_error("status (" + str(len(status)) + ") != zones (" + str(len(self.zones)) + " )...")
			return False

		if len(states) == len(self.areas):
			for i in range(0, len(states)):
				self.areas[i]["armed"] = states[i]
		else:
			self.raise_error("Erf, states (" + str(len(states)) + ") != areas (" + str(len(Areas)) + " )...")
			return False
		return True


	### Stay connected ###
	def keep_alive(self):
		while (self.running):
			#generate random id
			rand = random.randint(1000000000000000,9999999999999999)

			html = self.do_request("keep_alive.html?msgid=1&" + str(rand))
			if not html:
				self.keep_alive_errors += 1
				if self.keep_alive_allowed_errors == self.keep_alive_errors:
					self.raise_error("Keep alive errors exceeded")
					self.running = False
					return False
			else:
				if "javascript" in html:
					self.raise_error("Connection lost")
					self.running = False
					self.connected = False
					return False
			time.sleep(2.5)


	### Commands methods ###

	def arm(self):
		do_request("statuslive.html?area=00&value=r")

	def desarm(self):
		do_request("statuslive.html?area=00&value=d")

	def partiel(self):
		do_request("statuslive.html?area=00&value=s")