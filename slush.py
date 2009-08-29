#!/usr/bin/python

from lib import server
from lib import db

database = db.SlushDict(file="slushworld.db", table="info")

db.Database(database.__db__)
slush = server.Server(db.Database(database.__db__))

try:
	slush.start()
except KeyboardInterrupt:
	slush.stop()