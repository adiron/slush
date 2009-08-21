# karmaUser.py
from hashlib import md5
import datetime
#class userlist():
#	def __init__(self):
salt = b"FPBfQnuoOF5nlpIqw2do"
class user():
	def __init__(self, name, pw):
		self.name = name
		self.passwd = md5(bytes(pw,"UTF-8") + salt).digest()
		self.chars = [] # chars that the player plays
		self.registered = datetime.datetime.now()
		self.last_login = datetime.datetime.now()
		self.roles = []
				
	def authenticate(self, pw):
		if self.passwd == md5(bytes(pw,"UTF-8")+salt).digest():
			return True
		else:
			return False
			
	def hasRole(self, role):
		try: 
			if roles.index(role):
				return True
			else:
				return False
		except:
			return False
		
	
	def grantRole(self, role):
		if not self.hasRole(role):
			self.roles.append(role)

class PC():
	def __init__(self, charname):
		self.name = charname
		self.inventory = []
		self.position = 0
		self.attributes = {}
		
	def __getitem__(self, index):
		return self.attributes[index]
		
	def __setitem__(self, index, val):
		self.attributes[index] = val
		
class object():
	def __init__(self, name, desc=""):
		self.name = name
		self.description = desc
		self.attributes = {}
	
	def __getitem__(self, index):
		try:
			return self.attributes[index]
		except KeyError:
			return None
		
	def __setitem__(self, index, val):
		self.attributes[index] = val
		
class Session():
	def __init__(self):
		self.user = None
		self.logged_in = False

		
		