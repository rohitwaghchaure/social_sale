from flask import  redirect, Flask, render_template, url_for
import MySQLdb
import warnings
import datetime

class Database(object):
	"""docstring for database"""
	def __init__(self, arg):
		if arg:
			self._db = MySQLdb.connect(arg.get('host'),arg.get('user'),arg.get('password'), arg.get('database'))
			self._cursor = self._db.cursor()

	def sql(self, query, auto_commit=0):
		try:
			if self._cursor:
				self.data = self._cursor.execute(query)
				if auto_commit:
					self.commit()
		except Exception:
			self.sql("rollback")

		if self.data:
			return self._cursor.fetchall()

	def commit(self):
		self.sql("commit")

	def close(self):
		if self._db:
			self._cursor.close()
			self._db.close()
			self._db = None
			self._cursor = None
