import sqlite3

class SlushDict(dict):
	def __init__(self, file=None, table="slush", cursor=None):
		self.file = file
		self.table = table
		if file and (cursor == None): # If file is provided, this table is a master table.
			self.__conn__ = sqlite3.connect(file, isolation_level=None)
			self.__db__ = self.__conn__.cursor()
		else:
			self.__db__ = cursor
		self.__db__.execute("create table if not exists %s (key, value)" % self.table)
		
	def __todict__(self):
		end = dict()
		everything = self.__db__.execute("select * from %s order by key" % self.table).fetchall()
		for a in everything:
			end[a[0]] = a[1]
		return end
		
		
	def __getitem__(self, item):
		try:
			return self.__db__.execute('select value from %s where key=?' % self.table, (item,)).fetchone()[0]
		except TypeError:
			raise KeyError
			
	def __setitem__(self, key, value):
		try:
			self[key]
			self.__db__.execute('update %s set value=? where key=?' % self.table, (value, key))
		except KeyError:
			self.__db__.execute('insert into %s values (?, ?)' % self.table, (key, value))
	def execute(self, command):
		self.__db__.execute(command)		
		
	def __contains__(self,key):
		try:
			if self[key] is not None: return True
		except KeyError:
			return False
		

	def __delitem__(self, key): #deletes a key
		self.__db__.execute('delete from %s where key=?' % self.table, (key,))
	
	def __repr__(self): #string representation
		return self.__todict__().__repr__()

	def __ne__(self, other):
		return not self == other
		
	def keys(self):
		return self.__todict__().keys()
		
	def values(self):
		return self.__todict__().values()
	
	def __iter__(self):
		return self.__todict__().__iter__()
		
	def __eq__(self, a):
		return self.__todict__().__eq__(a)
		
	def derive(self, tbl):
		"""This function returns an object of the same class as its parent based on a cursor from it. In other words, it allows several slush DB objects to be used at the same time."""
		return SlushDict(cursor=self.__db__, table=tbl)
		
class SlushTableRow():
	def __init__(self, parent, idx):
		'''fields is a list that contains the name of all columns.'''
		self.parent = parent
		self.fields = self.parent.fields
		self.idx = idx
		self.table = self.parent.table
		self.__db__ = self.parent.__db__
		
	def __getitem__(self, col):
		if type(col).__name__ == "int":
			return self.__db__.execute('select %s from %s where idx=?' % (self.fields[col],self.table), (self.idx,) ).fetchone()[0]
		if type(col).__name__ == "str":
			return self.__db__.execute('select %s from %s where idx=?' % (col,self.table), (self.idx,) ).fetchone()[0]
		else:
			print(type(col).__name__)
	
	def __setitem__(self, col, value):
		if type(col).__name__ == "int":
			self.__db__.execute('update %s set %s=? where idx=?' % (self.table, self.fields[col]), (value,self.idx) )
		if type(col).__name__ == "str":
			self.__db__.execute('update %s set %s=? where idx=?' % (self.table, col), (value,self.idx) )
	def toDict(self):
		end = dict()
		for a in ["idx"] + list(self.fields):
			end[a]=self[a]
		return end
	def __repr__(self):
		"""Will fix this eventually to display the ACTUAL order..."""
		return self.toDict().__repr__()
	
	def __len__(self):
		return len(self.fields)
		

		
class SlushTable():
	def __init__(self, file=None, table="slush", fields=None, cursor=None):
		'''fields is a list that contains the name of all columns.'''
		self.file = file
		if file and (cursor == None): # If file is provided, this table is a master table.
			
			self.__conn__ = sqlite3.connect(file, isolation_level=None)
			self.__db__ = self.__conn__.cursor()
		else: # Making a DB from a cursor provided
			self.__db__ = cursor
		
		self.table = table
		if fields:
			self.fields = fields
		else:
			a = self.__db__.execute("pragma table_info(%s)" % self.table).fetchall()
			fields = list()
			for b in a:
				fields.append(b[1])
			if fields[0] == "idx":
				del fields[0]
			self.fields = fields

		 

		self.__db__.execute("create table if not exists %s (%s)" % (self.table, "idx INTEGER PRIMARY KEY, " + ", ".join(fields) ) )
	
	def isEmpty(self, idx):
		a = self.__db__.execute("select * from %s where idx=?" % (self.table), (idx,) ).fetchone()
		if a:
			return False
		else:
			return True
		
	def __getitem__(self, item):
		if not self.isEmpty(item):
			return SlushTableRow(self, item)
		else:
			raise KeyError
	def __iter__(self):
		"""RETURNS A COPY!"""
		return self.where("").__iter__()
			
	def where(self, expression, expansions=() ):
		"""Iterate except with the SQL WHERE expression as requested. Returns a COPY!"""
		if expression:
			where = "where " + expression
		else:
			where = ""
		
		data = self.execute("select * from %s %s" % (self.table, where), expansions ).fetchall()
		# Dictify it
		end = list()
		for a in data:
			end.append( dict(zip(["idx"] + self.fields, a)) )
		return end
				
	
	def __setitem__(self, index, value):
		if not self.isEmpty(index):
			try:
				self[index]
				if type(value).__name__ == "tuple" or type(value).__name__ == "list":
					pass # TODO
					
				if type(value).__name__ == "dict":
					for (k,v) in value.items():
						self[index][k] = v
				else:
					raise TypeError
			except sqlite3.OperationalError:
				raise ValueError
		else:
			raise IndexError
			
	def __delitem__(self, index):
		if not self.isEmpty(index):
			self.execute("delete from %s where idx=?" % (self.table), expansions=index )
		else:
			raise ValueError
						
	def __len__(self):
		return len(self.__db__.execute("select idx from %s" % self.table).fetchall())
		
	def __repr__(self):
		end = "{\n"
		for a in self.where(""):
			end = end + "\t" + a.__repr__() + "\n"
		return end + "}"

					
	def execute(self, command, expansions=()):
		if (type(expansions).__name__ != "NoneType") and (type(expansions).__name__ != "list") and (type(expansions).__name__ != "tuple"):
			expansions = (expansions,)
			
		a = self.__db__.execute(command, expansions)
		return a
		
	def clear(self):
		for a in self.where(""):
			del self[a["idx"]]
		
	def append(self, item):
		if len(item) != len(self.fields):
			raise TypeError
		for a in item:
			try:
				self.fields.index(a)
			except ValueError:
				raise KeyError
				
		self.__db__.execute('insert into %s values (NULL, %s)' % (self.table, ", ".join(["NULL"]*len(self.fields))))
		self[self.__db__.execute('select idx from %s where idx = (select max(idx) from %s);' % (self.table, self.table)).fetchone()[0]] = item
		
		
	def derive(self, tbl, cols=None):
		"""This function returns an object of the same class as its parent based on a cursor from it. In other words, it allows several slush DB objects to be used at the same time."""
		return SlushTable(cursor=self.__db__, table=tbl, fields=cols)
		



