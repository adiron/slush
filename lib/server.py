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

import socket
import threading
import auth
import parse

class Server():
	def __init__(self, database):
		"""Where database is a simple database object"""
		self.data = database
		self.port = self.data.info["port"]
		self.clients = HolesList()
		self.wrapup = False # Internal use only. This is true when you want the server to go down.
	def newSession(self, sock, address):
		a = self.clients.append(
			auth.Session(sock, address, self.data))
		return self.clients[a]
	def newConnection(self, session):
		"""This function handles new connections."""
		while not session.wrapup:
			a = self.recv(session.socket)
			while a:
				if session.user.authenticated:
					parse.Parse(a, session)
				else:
					parse.Login(a, session)
		session.sock.close()
			
		
		while session.user.authenticated == False:
			# Display the "login prompt" mode
			# More stuff will come here relating to
			# disconnecting idiots.
			
		
		# After that is done, display the usual prompt.
	
	def recv(clientsock, buff):
		"""This is a function to use as a kind of utility. It is called by other functions here and
		returns some input from the socket. It's done this way to ease future developments."""
		
		data = clientsock.recv(buff)
		try:
			data = str(data,"UTF-8")
		except UnicodeDecodeError:
			data = str(data,"CP1252")
		return data
	
	def start():
		"""Start the server."""
		# start accepting connections
		self.wrapup = False
		while not self.wrapup:
			# fork connection to new thread
			print ('Listening...')
			clientsock, addr = serversock.accept()
			print ('Incoming connection from: ', addr)
			session = newSession(clientsock, addr)
			self.threads.append(threading.Thread(target=newConnection, args=(session)))
			self.threads[len(self.threads)-1].start()


class HolesList(list):
	def __delitem__(self, i):
		if i == len(self) - 1:
			list.__delitem__(self, i)
		else:
			self[i] = None
		for j in range(len(self) - 1, -1, -1):
			if self[j] != None:
				break
			else:
				list.__delitem__(self, j)

	def __add__(self, thelist):
		if type(thelist) not in [type([]), type(HolesList())]:
			raise(TypeError("can only concatenate list and HolesList to HolesList"))
		indexes = []
		for x in thelist:
			indexes.append(self.append(x))
		return indexes

	def __contains__(self, item):
		if item == None:
			return False
		else:
			return list.__contains__(self, item)

	def append(self, item):
		for i in range(len(self)):
			if self[i] == None:
				self[i] = item
				return i
		#We will only get here if there were no empty slots
		list.append(self, item)
		return len(self) - 1

	def count(self, item):
		if item == None:
			return 0
		else:
			return list.count(self, item)

	def index(self, value, start=0, stop=None):
		if value == None:
			raise(ValueError("HolesList.index(x): x not in list"))
		else:
			if stop == None:
				stop = len(self)
			return list.index(self, value, start, stop)

	def remove(self, value):
		del self[self.index(value)]