from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
	def __init__(self):
		self.data = []
		HTMLParser.__init__(self);

	def handle_data(self, data):
		self.data.append(data)