# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

import pymysql
import uuid
from queue import Queue
from threading import Lock
from listeners.tick import GameThread
from conquest.debug import msg
class mysql:
	def __init__(self):
		self.socket = None
		self.cursor = None
		self.connect()
		self.queue = Queue()
		self.queue_lock = Lock()
		self.queue_queries = {}
		t = GameThread(target=self.queueworker, args=())
		t.start()

	def connect(self):
		try:
			if self.socket is None:
				self.socket = pymysql.connect(
					host='localhost',
					user='csgo_1',
					password='',
					db='csgo_1',
					charset='utf8mb4',
					autocommit=True,
					cursorclass=pymysql.cursors.DictCursor)
				self.cursor = self.socket.cursor()
				msg('INFO', 'successfully connected to mysql server')
			else:
				msg('INFO', 'reconnecting to mysql server')
				self.disconnect()
				self.connect()
		except:
			msg('ERROR', 'could not connect to mysql server')

	def query(self, query, params=[], fetch_all=True, wait=True):
		uid = uuid.uuid4()
		self.queue.put({
			'uid': uid,
			'query': query,
			'params': params,
			'fetch_all': fetch_all
		})
		if wait is True:
			while True:
				self.queue_lock.acquire()
				if uid in self.queue_queries:
					tmp = self.queue_queries[uid]
					del self.queue_queries[uid]
					self.queue_lock.release()
					return tmp
				self.queue_lock.release()
		
	def do_query(self, uid, query, params=[], fetch_all=True):
		try:
			self.cursor.execute(query, params)
			if fetch_all is True:
				return self.cursor.fetchall()
			else:
				return self.cursor.fetchone()
		except:
			msg('ERROR', 'could not perform query - mysql connection lost?')
			self.connect()
			self.query(query, params, fetch_all)

	def queueworker(self):
		while True:
			item = self.queue.get()
			if item is None:
				break
			self.queue_lock.acquire()
			self.queue_queries[item['uid']] = self.do_query(item['uid'], item['query'], item['params'], fetch_all=item['fetch_all'])
			self.queue_lock.release()
			
	def disconnect(self):
		self.socket.close()
		self.socket = None
		msg('INFO', 'disconnected from mysql server')