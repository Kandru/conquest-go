# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

import time
import random

from engines.sound import StreamSound
from engines.sound import Channel
from filters.players import PlayerIter

from conquest.debug import msg

class sounds:
	def __init__(self, db, downloads):
		self.db = db
		self.downloads = downloads
		self.sounds = {}
		self.get_sounds()

	def get_sounds(self):
		sql = "SELECT * FROM sounds ORDER BY id ASC"
		rows = self.db.query(sql)
		for row in rows:
			if row['type'] not in self.sounds:
				self.sounds[row['type']] = {}
			self.sounds[row['type']][row['id']] = row
			self.downloads.add('sound/' + row['file'].strip())

	def get_player(self):
		list = []
		for item in PlayerIter():
			list.append(item.index)
		return list

	def play(self, type, id, player = [], channel = Channel.STREAM):
		if type in self.sounds:
			if int(id) in self.sounds[type]:
				print(self.sounds[type][id]['file'])
				file = StreamSound(self.sounds[type][id]['file'], channel=channel)
				if not player:
					player = self.get_player()
				file.play(player)
				msg('DEBUG','played sound type {} with id {}'.format(type, id))
				return
		msg('WARNING','could not find sound type {} with id {}'.format(type, id))
		
	def play_random(self, type, player = [], channel = Channel.STREAM):
		if type in self.sounds:
			if not player:
				player = self.get_player()
			sound = self.sounds[type]
			sound = random.choice(list(sound))
			self.play(type, sound, player, channel)
