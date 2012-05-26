#!/usr/local/bin/python2.6

from lib import server
from lib import db

slush = server.Server(db.Database("slushworld.db"), verbosive=True)

try:
	slush.start()
except KeyboardInterrupt:
	slush.stop()