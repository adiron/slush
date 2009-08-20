#!/usr/bin/python

import socket
import threading

from lib import db

# init sock

# load the db

def sendMotd(sock, who):
	sock.send(b"Hello there, welcome to this MUD.\nPlease log in:\n")
def handleData(sock, data):
	pass

def client(clientsock,addr):
	sendMotd(clientsock, addr)
	data = clientsock.recv(buff)
	while data:
		data = clientsock.recv(buff)
		try: data = str(data,"UTF-8")
		except UnicodeDecodeError: data = str(data,"CP1252")
		handleData(clientsock, data)
	clientsock.close()

host = 'localhost'
listenport = 2323
buff = 1024
ADDR = (host, listenport)
threads =  []
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(2)


# start accepting connections
wrapup = False
while not wrapup:
	# fork connection to new thread
	print ('waiting for connection…')
	clientsock, addr = serversock.accept()
	print ('…connected from:', addr)
	threads.append(threading.Thread(target=client, args=(clientsock, addr)))
	threads[len(threads)-1].start()
	
