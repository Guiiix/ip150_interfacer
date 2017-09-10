import numpy

class Paracrypt:

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def unsigned_right_shift_32(self, a, b):
		return (a & 0xFFFFFFFF) >> b

	def binl2hex(self, binarray):
		hex_tab = "0123456789ABCDEF"
		str = ""
		for i in range(0, len(binarray) * 4):
			str += hex_tab[(binarray[i >> 2] >> ((i % 4) * 8 + 4)) & 0xF] + hex_tab[(binarray[i >> 2] >> ((i % 4) * 8)) & 0xF]
		return str

	def bit_rol(self, num, cnt):
		a = (num << cnt) | (self.unsigned_right_shift_32(num,(32 - cnt)))
		return a

	def core_md5(self, x, size):
		#Patch for undefined offsets
		if ((size >> 5) not in x.keys()): 
			x[size >> 5] = 0
		#End patch

		x[size >> 5] |= 0x80 << ((size) % 32)
		x[((self.unsigned_right_shift_32((size + 64),9)) << 4) + 14] = size

		a = numpy.int32(1732584193)
		b = numpy.int32(-271733879)
		c = numpy.int32(-1732584194)
		d = numpy.int32(271733878)
		for i in range(0,len(x), 16):
			#Patch for undefined offsets
			for j in range (0, 16):
				if ((i+j) not in x.keys()):
					x[i+j] = 0
			#End patch
			olda = a
			oldb = b
			oldc = c
			oldd = d
			a = self.md5_ff(a, b, c, d, x[i + 0], 7, -680876936)
	        d = self.md5_ff(d, a, b, c, x[i + 1], 12, -389564586)
	        c = self.md5_ff(c, d, a, b, x[i + 2], 17, 606105819)
	        b = self.md5_ff(b, c, d, a, x[i + 3], 22, -1044525330)
	        a = self.md5_ff(a, b, c, d, x[i + 4], 7, -176418897)
	        d = self.md5_ff(d, a, b, c, x[i + 5], 12, 1200080426)
	        c = self.md5_ff(c, d, a, b, x[i + 6], 17, -1473231341)
	        b = self.md5_ff(b, c, d, a, x[i + 7], 22, -45705983)
	        a = self.md5_ff(a, b, c, d, x[i + 8], 7, 1770035416)
	        d = self.md5_ff(d, a, b, c, x[i + 9], 12, -1958414417)
	        c = self.md5_ff(c, d, a, b, x[i + 10], 17, -42063)
	        b = self.md5_ff(b, c, d, a, x[i + 11], 22, -1990404162)
	        a = self.md5_ff(a, b, c, d, x[i + 12], 7, 1804603682)
	        d = self.md5_ff(d, a, b, c, x[i + 13], 12, -40341101)
	        c = self.md5_ff(c, d, a, b, x[i + 14], 17, -1502002290)
	        b = self.md5_ff(b, c, d, a, x[i + 15], 22, 1236535329)
	        a = self.md5_gg(a, b, c, d, x[i + 1], 5, -165796510)
	        d = self.md5_gg(d, a, b, c, x[i + 6], 9, -1069501632)
	        c = self.md5_gg(c, d, a, b, x[i + 11], 14, 643717713)
	        b = self.md5_gg(b, c, d, a, x[i + 0], 20, -373897302)
	        a = self.md5_gg(a, b, c, d, x[i + 5], 5, -701558691)
	        d = self.md5_gg(d, a, b, c, x[i + 10], 9, 38016083)
	        c = self.md5_gg(c, d, a, b, x[i + 15], 14, -660478335)
	        b = self.md5_gg(b, c, d, a, x[i + 4], 20, -405537848)
	        a = self.md5_gg(a, b, c, d, x[i + 9], 5, 568446438)
	        d = self.md5_gg(d, a, b, c, x[i + 14], 9, -1019803690)
	        c = self.md5_gg(c, d, a, b, x[i + 3], 14, -187363961)
	        b = self.md5_gg(b, c, d, a, x[i + 8], 20, 1163531501)
	        a = self.md5_gg(a, b, c, d, x[i + 13], 5, -1444681467)
	        d = self.md5_gg(d, a, b, c, x[i + 2], 9, -51403784)
	        c = self.md5_gg(c, d, a, b, x[i + 7], 14, 1735328473)
	        b = self.md5_gg(b, c, d, a, x[i + 12], 20, -1926607734)
	        a = self.md5_hh(a, b, c, d, x[i + 5], 4, -378558)
	        d = self.md5_hh(d, a, b, c, x[i + 8], 11, -2022574463)
	        c = self.md5_hh(c, d, a, b, x[i + 11], 16, 1839030562)
	        b = self.md5_hh(b, c, d, a, x[i + 14], 23, -35309556)
	        a = self.md5_hh(a, b, c, d, x[i + 1], 4, -1530992060)
	        d = self.md5_hh(d, a, b, c, x[i + 4], 11, 1272893353)
	        c = self.md5_hh(c, d, a, b, x[i + 7], 16, -155497632)
	        b = self.md5_hh(b, c, d, a, x[i + 10], 23, -1094730640)
	        a = self.md5_hh(a, b, c, d, x[i + 13], 4, 681279174)
	        d = self.md5_hh(d, a, b, c, x[i + 0], 11, -358537222)
	        c = self.md5_hh(c, d, a, b, x[i + 3], 16, -722521979)
	        b = self.md5_hh(b, c, d, a, x[i + 6], 23, 76029189)
	        a = self.md5_hh(a, b, c, d, x[i + 9], 4, -640364487)
	        d = self.md5_hh(d, a, b, c, x[i + 12], 11, -421815835)
	        c = self.md5_hh(c, d, a, b, x[i + 15], 16, 530742520)
	        b = self.md5_hh(b, c, d, a, x[i + 2], 23, -995338651)
	        a = self.md5_ii(a, b, c, d, x[i + 0], 6, -198630844)
	        d = self.md5_ii(d, a, b, c, x[i + 7], 10, 1126891415)
	        c = self.md5_ii(c, d, a, b, x[i + 14], 15, -1416354905)
	        b = self.md5_ii(b, c, d, a, x[i + 5], 21, -57434055)
	        a = self.md5_ii(a, b, c, d, x[i + 12], 6, 1700485571)
	        d = self.md5_ii(d, a, b, c, x[i + 3], 10, -1894986606)
	        c = self.md5_ii(c, d, a, b, x[i + 10], 15, -1051523)
	        b = self.md5_ii(b, c, d, a, x[i + 1], 21, -2054922799)
	        a = self.md5_ii(a, b, c, d, x[i + 8], 6, 1873313359)
	        d = self.md5_ii(d, a, b, c, x[i + 15], 10, -30611744)
	        c = self.md5_ii(c, d, a, b, x[i + 6], 15, -1560198380)
	        b = self.md5_ii(b, c, d, a, x[i + 13], 21, 1309151649)
	        a = self.md5_ii(a, b, c, d, x[i + 4], 6, -145523070)
	        d = self.md5_ii(d, a, b, c, x[i + 11], 10, -1120210379)
	        c = self.md5_ii(c, d, a, b, x[i + 2], 15, 718787259)
	        b = self.md5_ii(b, c, d, a, x[i + 9], 21, -343485551)
	        a = self.safe_add(a, olda)
	        b = self.safe_add(b, oldb)
	        c = self.safe_add(c, oldc)
	        d = self.safe_add(d, oldd)        
		return (a, b, c, d)

	def dh2(self, d):
		hD = "0123456789ABCDEF"
		h = hD[(d & 15)]
		while (d > 15):
			d >>= 4
			h = hD[(d & 15)] + h
		if (len(h) == 1):
			h = "0" + h
		return h

	def hex_md5(self, str):
		a = self.binl2hex(self.core_md5(self.str2binl(str), len(str) * 8))
		return a

	def keeplowbyte(self, svalue):
		sre = ""
		for i in range (0, len(svalue)):
			short_val = ord(svalue[i])
			short_val %= 256
			ctemp = chr(short_val)
			sre += ctemp
		return sre

	def login_encrypt(self, ses):
		tmp_pass = self.keeplowbyte(self.password)
		tmp_pass = self.hex_md5(tmp_pass)
		tmp_pass = tmp_pass + ses
		user_enc = self.rc4(tmp_pass, self.username)
		pass_enc = self.hex_md5(tmp_pass)
		return {'user': user_enc, 'password': pass_enc}
		
	def md5_cmn(self, q, a, b, x, s, t):
		return self.safe_add(self.bit_rol(self.safe_add(self.safe_add(a, q), self.safe_add(x, t)), s), b)

	def md5_ff(self, a, b, c, d, x, s, t):
		return self.md5_cmn((b & c) | ((~b) & d), a, b, x, s, t)

	def md5_gg(self, a, b, c, d, x, s, t):
		return self.md5_cmn((b & d) | (c & (~d)), a, b, x, s, t)

	def md5_hh(self, a, b, c, d, x, s, t):
		return self.md5_cmn(b ^ c ^ d, a, b, x, s, t)

	def md5_ii(self, a, b, c, d, x, s, t):
		return self.md5_cmn(c ^ (b | (~d)), a, b, x, s, t)

	def rc4(self, key, text):
		text = str(text)
		kl = len(key)
		s = {}
		for i in range(0, 256):
			s[i] = i
		y = 0
		x = kl-1
		while (x >= 0):
			y = (ord(key[x]) + s[x] + y) % 256
			t = s[x]
			s[x] = s[y]
			s[y] = t
			x -= 1
		x = 0
		y = 0
		z = ""
		for x in range (0, len(text)):
			x2 = x & 255
			y = (s[x2] + y) & 255
			t = s[x2]
			s[x2] = s[y]
			s[y] = t
			temp = chr(ord(text[x]) ^ s[(s[x2] + s[y]) % 256])
			z += self.dh2(ord(temp[0]))
		return z

	def safe_add(self, x, y):
		lsw = (x & 0xFFFF) + (y & 0xFFFF)
		msw = (x >> 16) + (y >> 16) + (lsw >> 16)
		return (msw << 16) | (lsw & 0xFFFF)

	def str2binl(self, str):
		bin = {}
		mask = (1 << 8) - 1
		for i in range(0, len(str) * 8, 8):
			if ((i >> 5) not in bin.keys()): 
				bin[i >> 5] = 0
			bin[i >> 5] |= (ord(str[i/8]) & mask) << (i % 32)
		return bin
