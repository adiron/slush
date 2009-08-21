from hashlib import md5
import datetime

class User():
	def __init__(self, reference, info): # Reference is a SlushTableRow with that user.
		self.reference = reference
		self.info = info
	
	def Authenticate(self, passwd):
		"""Returns true upon correct login. False upon incorrect login."""
		if reference["password"] == md5(bytes(pw,"UTF-8")+ info["salt"]).digest():
			return True
		else:
			return False

	# More to come. Eventually.