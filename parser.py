# -*-coding:Latin-1 -*
import sys,os
from MyHTMLParser import *
from pyjsparser import PyJsParser
from parser_const import *
import globals


def js_from_html(html):
	parser = MyHTMLParser()
	parser.feed(html)
	return parser.data

def parse_js(js_html):
	try:
		p = PyJsParser()
		js_ast = p.parse(js_html)
	except:
		return False
	return js_ast

def parse_equipment(js_html_list):
	js_stripped = []
	for s in js_html_list:
		js_stripped.append(remove_special_chars(s))
	js_html_list = js_stripped
	zones = False
	areas = False
	for js_html in js_html_list:
		js_ast = parse_js(js_html)
		if js_ast:
			for element in js_ast["body"]:
				if element["type"] == "ExpressionStatement":
					if element["expression"]["type"] == "AssignmentExpression":
						if element["expression"]["left"]["type"] == "Identifier":
							if element["expression"]["left"]["name"] == PARSER_ZONES_IDENTIFIER:
								if element["expression"]["right"]["type"] == "NewExpression":
									zones = element["expression"]["right"]["arguments"]
						if element["expression"]["left"]["type"] == "Identifier":
							if element["expression"]["left"]["name"] == PARSER_AREAS_IDENTIFIER:
								if element["expression"]["right"]["type"] == "NewExpression":
									areas = element["expression"]["right"]["arguments"]
	if not zones or not areas:
		if globals.Verbose:
			if not zones:
				print '\033[91m' + "* <PARSER> : Unable to locate zones" + '\033[0m'
			if not areas:
				print'\033[91m' + "* <PARSER> : Unable to locate areas" + '\033[0m'
		return False
	if globals.Verbose:
		print '\033[94m' + "* <PARSER> : Zones & areas found, parsing..." + '\033[0m'
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
	if globals.Verbose:
		print '\033[94m' + "* <PARSER> : Zones & areas parsed" + '\033[0m'
	return (parsed_zones, parsed_areas)

def parse_ses(js_html_list):
	ses = False
	for js_html in js_html_list:
		js_ast = parse_js(js_html)
		if js_ast:
			for element in js_ast["body"]:
				if element["type"] == "ExpressionStatement":
					if element["expression"]["type"] == "AssignmentExpression":
						if element["expression"]["right"]["type"] == "CallExpression":
							if element["expression"]["right"]["callee"]["type"] == "Identifier":
								if element["expression"]["right"]["callee"]["name"] == PARSER_SES_IDENTIFIER:
									ses = element["expression"]["right"]["arguments"][0]["value"]
	return ses

def parse_status(js_html_list):
	status_list = False
	for js_html in js_html_list:
		js_ast = parse_js(js_html)
		if js_ast:
			for element in js_ast["body"]:
				if element["type"] == "ExpressionStatement":
					if element["expression"]["type"] == "AssignmentExpression":
						if element["expression"]["left"]["type"] == "Identifier":
							if element["expression"]["left"]["name"] == PARSER_STATUS_IDENTIFIER:
								if element["expression"]["right"]["type"] == "NewExpression":
									status_list = element["expression"]["right"]["arguments"]
							if element["expression"]["left"]["name"] == PARSER_STATES_IDENTIFIER:
								if element["expression"]["right"]["type"] == "NewExpression":
									states_list = element["expression"]["right"]["arguments"]
	if not status_list or not states_list:
		if globals.Verbose:
			if not status_list:
				print '\033[91m' + "* <PARSER> : Unable to locate status" + '\033[0m'
			if not states_list:
				print '\033[91m' + "* <PARSER> : Unable to parse states" + '\033[0m'
		return False
	if globals.Verbose:
		print '\033[94m' + "* <PARSER> : Status & states found, parsing..." + '\033[0m'
	status = []
	states = []
	for element in status_list:
		status.append(element["value"])
	for element in states_list:
		states.append(element["value"])
	if globals.Verbose:
		print '\033[94m' + "* <PARSER> : Status & states parsed" + '\033[0m'
	return (status,states)

def remove_special_chars(string):
	characters = ("é", "è", "ë", "ê", "È", "É", "Ê", "Ë", "Â", "Á", "Ã", "Ä", "à", "â", "ã", "ï", "î", "ô", "ö", "'", "ù", "ç", "û", "ù", "’");
	replace = ("e", "e", "e", "e", "e", "e", "e", "e", "a", "a", "a", "a", "a", "a", "a", "i", "i", "o", "o", " ", "u", "c", "u", "u", " ");
	for i in range(0, len(characters)):
		string = string.replace(characters[i], replace[i])
	return string

def someone_connected(js_html_list):
	connected = False
	for js_html in js_html_list:
		js_ast = parse_js(js_html)
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