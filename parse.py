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

from lib import db 
from data.commands import commands

class InvalidCommand(Exception): pass

def Parse(text, session):
	"""This function will return a dictionary with parse results.
	It does not handle nor care about interactivity. That's a completely different ballpark."""
	text = text.strip()
	args = text.split(" ")
	try:
		func = commands[args[0]]
	except KeyError:
		raise InvalidCommand

	func(args[1:], session)
