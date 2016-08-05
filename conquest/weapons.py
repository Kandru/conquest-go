# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

import json
import time
from threading import Lock

from players.entity import Player
from filters.players import PlayerIter
from entities.entity import Entity
from weapons.entity import Weapon
from messages import SayText2
from engines.precache import Model
from colors import Color
from mathlib import Vector
from effects import ball
from filters.recipients import RecipientFilter

from conquest.debug import msg

class weapons:
	def __init__(self, db, downloads, rank):
		self.db = db
		self.downloads = downloads
		self.rank = rank
		self.color_ct = Color(0, 200, 255)
		self.color_t = Color(255, 0, 0)
		self.packs_lock = Lock()
		self.pack = {}
		self.last_ontick = 0
		
	def bomb_dropped(self, userid, bombentindex):
		# get c4
		tmp_bomb = Entity(bombentindex)
		# get origin of c4
		vector = tmp_bomb.origin
		# remove c4
		tmp_bomb.remove()
		# proof for a medkit
		self.create_medkit(userid, bombentindex, vector)
		# proof for an ammobox
		self.create_ammobox(userid, bombentindex, vector)

	def bomb_beep(self, bombentindex):
		# get c4
		tmp_bomb = Entity(bombentindex)
		# remove c4
		tmp_bomb.remove()

	def player_death(self, userid):
		self.delete_pack(userid)
		
	def player_disconnect(self, userid):
		self.delete_pack(userid)
		
	def delete_pack(self, userid):
		self.packs_lock.acquire()
		if userid in self.pack:
			self.pack[userid]['ent'].remove()
			del self.pack[userid]
		self.packs_lock.release()

	def create_medkit(self, userid, bombentindex, vector):
		try:
			locked = False
			# get player and team
			player = Player.from_userid(userid)
			pdata = self.rank.get_player_data(userid)
			if not int(pdata['class']) in self.rank.classes:
				return
			if not self.rank.classes[int(pdata['class'])]['can_have_medkit'] >= 1:
				return
			pteam = self.rank.get_player_team(userid)
			# create healthpack
			self.packs_lock.acquire()
			locked = True
			# delete old medkit if we spawn a new one
			if player.userid in self.pack:
				self.pack[player.userid]['ent'].remove()
				del self.pack[player.userid]
			# set medkit color
			if pteam == 'CT':
				color = self.color_ct
			else:
				color = self.color_t
			self.pack[player.userid] = {
				'ent': Entity.create('prop_physics_override'),
				'type': 'health',
				'amount': 200,
				'give': 10,
				'distance': 100,
				'userid': userid,
				'team': pteam,
				'next_glow': 0,
				'color': color,
			}
			self.pack[player.userid]['ent'].origin = vector
			self.pack[player.userid]['ent'].model = Model('models/props/cs_italy/bin01.mdl')
			self.pack[player.userid]['ent'].spawn_flags = 4
			self.pack[player.userid]['ent'].health = 10
			self.pack[player.userid]['ent'].color = color
			self.pack[player.userid]['ent'].health = 100
			# spawn healthpack
			self.pack[player.userid]['ent'].spawn()
			self.packs_lock.release()
			locked = False
		except:
			if locked:
				self.packs_lock.release()
			msg('ERROR', 'could not create healthpack')
			
	def create_ammobox(self, userid, bombentindex, vector):
		try:
			locked = False
			# get player and team
			player = Player.from_userid(userid)
			pdata = self.rank.get_player_data(userid)
			if not int(pdata['class']) in self.rank.classes:
				return
			if not self.rank.classes[int(pdata['class'])]['can_have_ammobox'] >= 1:
				return
			pteam = self.rank.get_player_team(userid)
			# create ammobox
			self.packs_lock.acquire()
			locked = True
			# delete old ammobox if we spawn a new one
			if player.userid in self.pack:
				self.pack[player.userid]['ent'].remove()
				del self.pack[player.userid]
			# set ammobox color
			if pteam == 'CT':
				color = self.color_ct
			else:
				color = self.color_t
			self.pack[player.userid] = {
				'ent': Entity.create('prop_physics_override'),
				'type': 'ammo',
				'amount': 200,
				'give': 10,
				'distance': 100,
				'userid': userid,
				'team': pteam,
				'next_glow': 0,
				'color': color,
			}
			self.pack[player.userid]['ent'].origin = vector
			self.pack[player.userid]['ent'].model = Model('models/props/cs_italy/bin02.mdl')
			self.pack[player.userid]['ent'].spawn_flags = 4
			self.pack[player.userid]['ent'].health = 10
			self.pack[player.userid]['ent'].color = color
			self.pack[player.userid]['ent'].health = 100
			# spawn healthpack
			self.pack[player.userid]['ent'].spawn()
			self.packs_lock.release()
			locked = False
		except:
			if locked:
				self.packs_lock.release()
			msg('ERROR', 'could not create healthpack')
		
	def weapon_circle(self, vector, radius, color, a=255):
		r = color[0]
		g = color[1]
		b = color[2]
		vector = Vector(vector[0], vector[1], vector[2])
		ball(
			RecipientFilter(),
			vector,
			radius,
			steps=1,
			upper_half=True,
			lower_half=False,
			alpha=a,
			blue=b,
			green=g,
			red=r,
			halo=Model('sprites/laserbeam.vmt'),
			model=Model('sprites/laserbeam.vmt'),
			amplitude=0,
			end_width=1,
			life_time=4,
			start_width=1,
			fade_length=0,
			flags=0,
			frame_rate=1,
			start_frame=0
		)

	def get_max_ammo_of_weapon(self, weapon_index):
		tmp_weap = Weapon(weapon_index)
		if tmp_weap:
			ammo = 10
			for item in self.rank.weapons:
				if self.rank.weapons[item]['slug'] == tmp_weap.classname:
					ammo = self.rank.weapons[item]['max_ammo']
					break
			return int(ammo)
		else:
			return int(0)
		
	def ontick(self):
		#try:
		# do not work on every tick
		cur_time = int(round(time.time(),0))
		if self.last_ontick <= cur_time:
			self.last_ontick = cur_time + 1;
			locked = False
			self.packs_lock.acquire()
			locked = True
			tmp_delete = []
			for item in self.pack:
				box = self.pack[item]['ent']
				give = self.pack[item]['give']
				if self.pack[item]['next_glow'] <= cur_time:
					self.pack[item]['next_glow'] = cur_time + 4
					self.weapon_circle(box.origin, self.pack[item]['distance'], self.pack[item]['color'])
				for player in PlayerIter():
					# if the box belongs to the same team and an alive and ready player
					if player.dead:
						continue
					if player.frozen:
						continue
					pteam = self.rank.get_player_team(player.userid)
					if pteam != self.pack[item]['team']:
						continue
					if give > self.pack[item]['amount']:
						give = self.pack[item]['amount']
					if player.origin.get_distance(box.origin) <= self.pack[item]['distance']:
						# health box
						if self.pack[item]['type'] == 'health':
							if player.health >= 100:
								continue
								old_health = player.health
								player.health += give
								if player.userid != int(self.pack[item]['userid']):
									self.rank.player_add_cash(self.pack[item]['userid'], give)
								if player.health > 100:
									player.health = 100
								self.pack[item]['amount'] -= give
						# ammo box
						if self.pack[item]['type'] == 'ammo':
							if player.get_primary():
								weapon = Weapon(player.get_primary())
								if weapon:
									current = int(weapon.get_property_short('m_iPrimaryReserveAmmoCount'))
									maxammo = self.get_max_ammo_of_weapon(player.get_primary())
									if current < maxammo:
										if not int(current) + int(give) < maxammo:
											give = int(maxammo) - int(current)
										if player.userid != int(self.pack[item]['userid']):
											self.rank.player_add_cash(self.pack[item]['userid'], give)
										weapon.set_property_short('m_iPrimaryReserveAmmoCount', int(current) + int(give))
										self.pack[item]['amount'] -= give
								weapon = Weapon(player.get_secondary())
								if weapon:
									current = int(weapon.get_property_short('m_iPrimaryReserveAmmoCount'))
									maxammo = self.get_max_ammo_of_weapon(player.get_secondary())
									if current < maxammo:
										if not int(current) + int(give) < maxammo:
											give = int(maxammo) - int(current)
										if player.userid != int(self.pack[item]['userid']):
											self.rank.player_add_cash(self.pack[item]['userid'], give)
										weapon.set_property_short('m_iPrimaryReserveAmmoCount', int(current) + int(give))
										self.pack[item]['amount'] -= give
							pass
					# remove empty boxes
					if int(self.pack[item]['amount']) <= 0:
						box.remove()
						tmp_delete.append(item)
			for item in tmp_delete:
				del self.pack[item]
			self.packs_lock.release()
			locked = False
		#except:
		#	if locked:
		#		self.packs_lock.release()
		#	msg('ERROR','could not finish class_weapon ontick')
