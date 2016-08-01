# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from messages import SayText2
from messages import HintText
from config.cvar import ConVar
from players.entity import Player
from listeners.tick import Delay
from players.constants import LifeState
from conquest.debug import msg
from mathlib import Vector
from random import choice as random_choice
from memory import make_object

class respawn:
	def __init__(self, callbacks):
		self.callbacks = callbacks
		self.respawn_time = ConVar("cq_respawn_time", '3', 'respawn interval')
		self.spawnprotection = ConVar("cq_spawnprotection", '2', 'spawn protection time (sec.)')
		self.msg_prepare = SayText2('prepare for respawn in {} seconds'.format(self.respawn_time.get_int()))
		self.msg_respawn = SayText2('welcome again, soldier!')
		self.msg_spawnprotection = HintText('Spawn protection disabled')
		# callbacks
		self.callbacks.register('player_is_spawned', 'respawn_spawnprotection_end', self.delay_spawnprotection_end)

	def get_player_team(self, player):
		try:
			if player.team == 3:
				return 'CT'
			elif player.team == 2:
				return 'T'
			else:
				return 'Unknown'
		except:
			msg('ERROR', 'could not get players team')
			return 'Unknown'

	def respawnplayer(self, userid):
		try:
			player = Player.from_userid(userid)
			if not player:
				return
			if not player.dead:
				return
			if player.team not in (2, 3):
				return
			self.msg_respawn.send(player.index)
			player.player_state = 0
			player.life_state = LifeState.ALIVE
			player.respawn()
		except:
			msg('ERROR', 'could not respawn player')

	def spawnprotection_start(self, player):
		try:
			player.set_godmode(True)
		except:
			msg('ERROR', 'could not enable godmode for player')

	def delay_spawnprotection_end(self, userid):
		player = Player.from_userid(userid)
		player.set_frozen(False)
		Delay(self.spawnprotection.get_float(), self.spawnprotection_end, userid)

	def spawnprotection_end(self, userid):
		try:
			player = Player.from_userid(userid)
			player.set_godmode(False)
			self.msg_spawnprotection.send(player.index)
		except:
			msg('ERROR', 'could not disable godmode for player')

	def get_random_spawnpoint(self, flags, team):
		spawnpoints = []
		for item in flags:
			if flags[item]['status'] == team:
				if int(flags[item]['spawnX']) != 0:
					spawnpoints.append(Vector(flags[item]['spawnX']+30, flags[item]['spawnY']+30, flags[item]['spawnZ']+10))
				else:
					spawnpoints.append(Vector(flags[item]['X']+30, flags[item]['Y']+30, flags[item]['Z']+10))
		if not spawnpoints:
			return None
		vector = random_choice(spawnpoints)
		return vector

	def player_spawn(self, userid, flags):
		try:
			player = Player.from_userid(userid)
			vector = self.get_random_spawnpoint(flags, self.get_player_team(player))
			self.spawnprotection_start(player)
			player.set_noblock(True)
			player.set_frozen(True)
			if not vector is None:
				player.origin = vector
			if not player.address:
				self.delay_spawnprotection_end(player.userid)
		except:
			msg('ERROR', 'could not spawn player at specific spawn point...')

	def player_death(self, userid):
		try:
			player = Player.from_userid(userid)
			self.msg_prepare.send(player.index)
			Delay(self.respawn_time.get_int(), self.respawnplayer, userid)
		except:
			msg('ERROR', 'could not respawn player after death')