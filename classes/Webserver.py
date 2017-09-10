import socket
import re
import time
import json

class Webserver:
	def __init__(self, host, port, interfacer, verbose_level):
		self.interfacer = interfacer
		self.host = host
		self.port = port
		self.run = True
		self.verbose_level = verbose_level

	def listen_http(self):
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    sock.bind((self.host, self.port))
	    sock.listen(1)
	    zones = False
	    areas = True

	    while self.run:
	    	csock, caddr = sock.accept()
	        req = csock.recv(1024) # get the request, 1kB max
	        # Look in the first line of the request for a move command
	        # A move command should be e.g. 'http://server/move?a=90'
	        self.handle_request(req, csock)
	        csock.close()

	def display_message(self, msg, verb):
		if verb <= self.verbose_level:
			print '\033[94m' + "* <WEBSERVER> : " + msg +  '\033[0m'

	def handle_request(self, req, csock):
		self.display_message(str(req), 2)
		http_header = "HTTP/1.1 200 OK\nServer: Python\nContent-Type: text/html\nConnection: close\n\n"  
		if self.interfacer.running and self.interfacer.connected:
			if re.match('GET /description', req):
				string = ""
				c = 0
				for i in range(0,len(self.interfacer.zones)):
					if self.interfacer.zones[i]["active"]:
						string += str(c) + " => " + str(self.interfacer.zones[i]["name"]) + "\n"
						c+=1
				csock.sendall(http_header+string)

			elif re.match('GET /status', req):
				status = {"status":"success", "state":self.interfacer.areas[0]["armed"], "detectors":[]}
				c = 0
				for e in self.interfacer.zones:
					if e["active"]:
						status["zone-"+str(c)] = e["status"]
					c+=1
				csock.sendall(http_header+json.dumps(status))

			elif re.match('GET /arm', req):
				self.interfacer.arm()
				csock.sendall(http_header+json.dumps({"status":"success"}))

			elif re.match('GET /desarm', req):
				self.interfacer.desarm()
				csock.sendall(http_header+json.dumps({"status":"success"}))

			elif re.match('GET /partiel', req):
				self.interfacer.partiel()
				csock.sendall(http_header+json.dumps({"status":"success"}))

			elif re.match('GET /stop', req):
				self.run = False
				self.interfacer.running = False
				csock.sendall(http_header+json.dumps({"status":"success"}))

			else:
				csock.sendall(http_header+json.dumps({"status":"error", "error":"HTTP 404"}))

		else:
			csock.sendall(http_header+json.dumps({"status":"error", "error":"Not connected", "details":json.dumps(self.interfacer.current_status)}))  
