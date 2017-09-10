# -*-coding:Latin-1 -*

from classes.MyHTMLParser import MyHTMLParser
from pyjsparser import PyJsParser
from const import *

class Parser:
	def __init__(self, interfacer, zones_identifier, area_identifier, ses_identifier, status_identifier, states_identifier):
		self.interfacer = interfacer
		self.zones_identifier = zones_identifier
		self.area_identifier = area_identifier
		self.ses_identifier = ses_identifier
		self.status_identifier = status_identifier
		self.states_identifier = states_identifier

	def js_from_html(self, html):
		parser = MyHTMLParser()
		parser.feed(html)
		return parser.data

	def parse_js(self, js_html):
		try:
			p = PyJsParser()
			js_ast = p.parse(js_html)
		except:
			self.interfacer.raise_error("Unable to get a JS AST")
			return False
		return js_ast

	def parse_equipment(self, js_html_list):
		js_stripped = []
		for s in js_html_list:
			js_stripped.append(self.remove_special_chars(s))
		js_html_list = js_stripped
		zones = False
		areas = False
		for js_html in js_html_list:
			js_ast = self.parse_js(js_html)
			if js_ast:
				for element in js_ast["body"]:
					if element["type"] == "ExpressionStatement":
						if element["expression"]["type"] == "AssignmentExpression":
							if element["expression"]["left"]["type"] == "Identifier":
								if element["expression"]["left"]["name"] == self.zones_identifier:
									if element["expression"]["right"]["type"] == "NewExpression":
										zones = element["expression"]["right"]["arguments"]
							if element["expression"]["left"]["type"] == "Identifier":
								if element["expression"]["left"]["name"] == self.area_identifier:
									if element["expression"]["right"]["type"] == "NewExpression":
										areas = element["expression"]["right"]["arguments"]
		if not zones:
			self.interfacer.raise_error("Unable to locate zones")
			return False
		if not areas:
			self.interfacer.raise_error("Unable to locate areas")
			return False
			
		self.interfacer.display_message("Zones & areas found, parsing...", 1)
		parsed_zones = []
		parsed_areas = []
		active = False
		for i in range(0, len(zones)):
			if i % 2 == 0:
				active = False if zones[i]["value"] == 0.0 else True
			else:
				parsed_zones.append({"name":zones[i]["value"], "active":active, "status": 0})
		for element in areas:
			parsed_areas.append({"name": element["value"], "armed": False})
		
		self.interfacer.display_message("Zones & areas parsed", 1)
		return (parsed_zones, parsed_areas)

	def parse_ses(self, js_html_list):
		ses = False
		for js_html in js_html_list:
			js_ast = self.parse_js(js_html)
			if js_ast:
				for element in js_ast["body"]:
					if element["type"] == "ExpressionStatement":
						if element["expression"]["type"] == "AssignmentExpression":
							if element["expression"]["right"]["type"] == "CallExpression":
								if element["expression"]["right"]["callee"]["type"] == "Identifier":
									if element["expression"]["right"]["callee"]["name"] == self.ses_identifier:
										ses = element["expression"]["right"]["arguments"][0]["value"]
		return ses

	def parse_status(self, js_html_list):
		status_list = False
		for js_html in js_html_list:
			js_ast = self.parse_js(js_html)
			if js_ast:
				for element in js_ast["body"]:
					if element["type"] == "ExpressionStatement":
						if element["expression"]["type"] == "AssignmentExpression":
							if element["expression"]["left"]["type"] == "Identifier":
								if element["expression"]["left"]["name"] == self.status_identifier:
									if element["expression"]["right"]["type"] == "NewExpression":
										status_list = element["expression"]["right"]["arguments"]
								if element["expression"]["left"]["name"] == self.states_identifier:
									if element["expression"]["right"]["type"] == "NewExpression":
										states_list = element["expression"]["right"]["arguments"]
		if not status_list:
			self.interfacer.raise_error("Unable to locate status")
			return False
		if not states_list:
			self.interfacer.raise_error("Unable to parse states")
			return False
		self.interfacer.display_message("Status & states found, parsing...", 1)
		status = []
		states = []
		for element in status_list:
			status.append(element["value"])
		for element in states_list:
			states.append(element["value"])
		
		self.interfacer.display_message("Status & states parsed", 1)
		return (status,states)

	def remove_special_chars(self, string):
		characters = ("é", "è", "ë", "ê", "È", "É", "Ê", "Ë", "Â", "Á", "Ã", "Ä", "à", "â", "ã", "ï", "î", "ô", "ö", "'", "ù", "ç", "û", "ù", "’");
		replace = ("e", "e", "e", "e", "e", "e", "e", "e", "a", "a", "a", "a", "a", "a", "a", "i", "i", "o", "o", " ", "u", "c", "u", "u", " ");
		for i in range(0, len(characters)):
			string = string.replace(characters[i], replace[i])
		return string

	def someone_connected(self, js_html_list):
		connected = False
		for js_html in js_html_list:
			js_ast = self.parse_js(js_html)
			if js_ast:
				for element in js_ast["body"]:
					if element["type"] == "ExpressionStatement":
						if element["expression"]["type"] == "AssignmentExpression":
							if element["expression"]["left"]["type"] == "MemberExpression":
								if element["expression"]["left"]["object"]["type"] == "CallExpression":
									for arg in element["expression"]["left"]["object"]["arguments"]:
										if arg["value"] == "ERROR":
											connected = True
		return connected
			