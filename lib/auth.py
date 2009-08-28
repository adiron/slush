# Slush - A Python MUD/MUSH server
# Copyright (C) 2009 Adi Ron
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# <http://www.gnu.org/licenses/>.

from hashlib import md5
import datetime

class Session():
	def __init__(self, socket, address, data):
		self.user = None # The user associated with the session.
		self.socket = socket # The socket associated with the session.
		self.address = address
		self.data = data

class User():
	# The user object is oblivious to the game world.
	# It's unaware of anything around it.
	# It is SOLELY for the use of a session.
	# Nothing more.
	def __init__(self, data): # Reference is a SlushTableRow with that user.
		self.username = ""
		self.info = info
		self.authenticated = False # Whether the user is authenticated or not
	
	
	def Authenticate(self, passwd):
		"""Returns true upon correct login. False upon incorrect login."""
		# First we make a reference out of a username. Not hard:
		reference = database.users[database.users.where(self.username)[0]["idx"]]
		if reference["banned"] == True:
			return False
		if reference["password"] == md5(bytes(pw,"UTF-8")+ info["salt"]).digest():
			reference["login_attempts"] = 0
			reference["last_login"] = datetime.datetime.now()
			self.authenticated = True
			return True
		else:
			reference["login_attempts"] == reference["login_attempts"] + 1
			if reference["login_attempts"] >= info["allowed_attempts"]:
				reference["banned"] = True
				reference["ban_reason"] = "Too many login attempts."
			return False

	# More to come. Eventually.