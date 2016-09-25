# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community
from collections import OrderedDict
from threading import Lock
import time
import math

from config.cvar import ConVar
from engines.precache import Model
from colors import Color
from listeners.tick import GameThread
from mathlib import Vector
from filters.recipients import RecipientFilter
from engines.server import global_vars, engine_server
from cvars.flags import ConVarFlags
from effects import ball
from entities.entity import Entity
from messages import HintText
from filters.players import PlayerIter
from cvars import cvar
from menus import SimpleMenu
from players.entity import Player

from conquest.debug import msg

class flags:
	def __init__(self, db, rank, callbacks, sounds):
		self.num_tickets = ConVar("cq_numtickets", '500', 'number of tickets')
		self.tickets = {'t': self.num_tickets.get_int(), 'ct': self.num_tickets.get_int(), 'time': 0}
		self.color_ct = Color(0, 200, 255)
		self.color_n = Color(255, 255, 255)
		self.color_t = Color(255, 0, 0)
		self.flags = {}
		self.flags_lock = Lock()
		# height of the flag on pole
		self.flag_height = 120
		self.model_flag = Model('models/props_downtown/sign_stop.mdl')
		self.model_pole = Model('models/props/cs_italy/it_streetlampleg.mdl')
		self.model_beam = Model('sprites/laserbeam.vmt')
		self.db = db
		self.rank = rank
		self.callbacks = callbacks
		self.sounds = sounds
		self.last_ontick = 0
		self.ontick_time = 0
		self.is_endround = False
		# register callbacks
		self.callbacks.register('player_is_spawned', 'flags_info_menu', self.info_menu)

	def info_menu(self, userids = []):
		try:
			info_menu = SimpleMenu(build_callback=self.callback_info_menu)
			list = []
			if type(userids) is not list:
				player = Player.from_userid(userids)
				list = [player.index]
			else:
				for item in userids:
					player = Player.from_userid(item)
					list.append(player.index)
			info_menu.send(list)
		except:
			msg('ERROR', 'could not send info menu to one or more players')

	def callback_info_menu(self, menu, pindex):
		try:
			player = Player(pindex)
			if player.dead:
				menu.close()
			else:
				pdata = self.rank.get_player_cached_data(player.userid)
				cur_time = int(round(time.time(),0))
				menu.clear()
				menu.append('Tickets   T: ' + str(self.tickets['t']))
				menu.append('Tickets CT: ' + str(self.tickets['ct']))
				menu.append('{} rank: {}'.format(self.rank.classes[int(pdata['class'])]['name'],str(pdata['rank'][str(pdata['class'])])))
				menu.append('------------------')
				flags = OrderedDict(sorted(self.flags.items(), key=lambda x: x[1]['orderby']))
				for item in flags:
					time_left = int(int(self.flags[item]['timer']) - float(self.flags[item]['timestamp']))
					if int(self.flags[item]['draw']) == 1:
						menu.append(self.flags[item]['name'] + ': DRAW')
					elif float(self.flags[item]['timestamp']) > 0:
						if self.flags[item]['tmp_status'] == 'none':
							time_left += self.flags[item]['timer']
						menu.append(self.flags[item]['name'] + ': ' + self.flags[item]['tmp_conquered_by'] + ' in ' + str(time_left))
					else:
						menu.append(self.flags[item]['name'] + ': ' + self.flags[item]['status'])
		except:
			msg('ERROR', 'could not send callback info menu to player')
	def get_flags(self):
		try:
			sql = "SELECT map,name,X,Y,Z,spawn_X,spawn_Y,spawn_Z,type,distance,status,timer,orderby FROM flags WHERE map = %s ORDER BY orderby ASC"
			return self.db.query(sql, (global_vars.map_name,))
		except:
			msg('ERROR', 'could not fetch any flags')
			return {}

	def get_flag(self, name):
		try:
			sql = "SELECT map,name,X,Y,Z,spawn_X,spawn_Y,spawn_Z,type,distance,status,timer,orderby FROM flags WHERE map = %s and name = %s LIMIT 0,1"
			return self.db.query(sql, (global_vars.map_name,name), fetch_all=False)
		except:
			msg('ERROR', 'could not fetch specific flag')
			return {}

	def spawn_flag(self, options = {}, spawnflag = True):
		# spawn flag in extra thread (independent from server tick)
		t = GameThread(target=self._spawn_flag, args=(options,spawnflag, ))
		t.start()

	def _spawn_flag(self, options = {}, spawnflag = True):
		try:
			# stop if options dict is empty
			if not options:
				return False
			if options['status'] == 'T':
				color = self.color_t
			elif options['status'] == 'CT':
				color = self.color_ct
			else:
				color = self.color_n
			if spawnflag is False:
				tmp_flag = self.flags[options['name']]['entity']
				tmp_pole = self.flags[options['name']]['entity_pole']
			else:
				tmp_flag = Entity.create('prop_physics_override')
				tmp_pole = Entity.create('prop_physics_override')
				if options['name'] in self.flags:
					if self.flags[options['name']]['entity'] is not None:
						tmp = self.flags[options['name']]['entity']
						tmp.remove()
					if self.flags[options['name']]['entity_pole'] is not None:
						tmp = self.flags[options['name']]['entity_pole']
						tmp.remove()
			if options['status'] != 'none':
				tmp_flag.origin = Vector(options['X'], options['Y'], options['Z'] + self.flag_height)
			else:
				tmp_flag.origin = Vector(options['X'], options['Y'], options['Z'])
			tmp_flag.set_key_value_color('rendercolor', color)
			tmp_pole.set_key_value_color('rendercolor', color)
			if spawnflag is True:
				tmp_flag.model = self.model_flag
				tmp_flag.spawn_flags = 265
				tmp_pole.origin = Vector(options['X'], options['Y'], options['Z'])
				tmp_pole.model = self.model_pole
				tmp_pole.spawn_flags = 265
				tmp_flag.spawn()
				tmp_pole.spawn()
			self.flags_lock.acquire()
			self.flags[options['name']] = {
				'name': options['name'],
				'orderby': options['orderby'],
				'X': options['X'],
				'Y': options['Y'],
				'Z': options['Z'],
				'spawnX': options['spawn_X'],
				'spawnY': options['spawn_Y'],
				'spawnZ': options['spawn_Z'],
				'distance': options['distance'],
				'type': options['type'],
				'timer': options['timer'],
				'status': options['status'],
				'tmp_status': options['status'],
				'tmp_conquered_by': 'none',
				'draw': 0,
				'timestamp': '0',
				't_index' : [],
				'ct_index': [],
				'last_glow': 0,
				'entity': tmp_flag,
				'entity_pole': tmp_pole,
			}
			self.flags_lock.release()
		except:
			msg('ERROR', 'could not spawn flag')
	
	def spawn_flags(self):
		flags = self.get_flags()
		for row in flags:
			try:
				if row['name'] not in self.flags:
					self.respawn_flag(row['name'])
			except:
				msg('ERROR', 'could not spawn flags')

	def respawn_flag(self, name, status = 'default'):
		try:
			if global_vars.map_name:
				flag = self.get_flag(name)
				# if nothing sets the spawn status use default from mysql
				if status == 'default':
					status = flag['status']
				# choose color based on status
				if status == 'T':
					color = self.color_t
					flag['status'] = status
				elif status == 'CT':
					color = self.color_ct
					flag['status'] = status
				else:
					color = self.color_n
				if flag is not None:
					if flag['name'] not in self.flags:
						self.spawn_flag(flag)
					else:
						pass
						self.spawn_flag(flag, False)
		except:
			msg('ERROR', 'could not respawn a specific flag')

	def set_flag_height(self, item, direction = 0):
		if item in self.flags:
			tmp_flag = self.flags[item]['entity']
			time_left = int(self.flags[item]['timer']) - float(self.flags[item]['timestamp'])
			lowest_z = self.flags[item]['Z']
			if int(self.flags[item]['timer']) < time_left:
				time_left = int(self.flags[item]['timer'])
			# if the flag should go down
			if direction == 0:
				tmp = self.flag_height / (int(self.flags[item]['timer']))
				z = (time_left * tmp) + lowest_z
			# if the flag should go up
			else:
				tmp = self.flag_height / (int(self.flags[item]['timer']))
				z = (lowest_z + self.flag_height) - (time_left * tmp)
			tmp_flag.origin = Vector(tmp_flag.origin[0], tmp_flag.origin[1], z)



	def reset_flags(self):
		self.flags = {}

	def reset_tickets(self):
		self.tickets = {'t': self.num_tickets.get_int(), 'ct': self.num_tickets.get_int(), 'time': 0}
		self.is_endround = False

	def remove_flags(self):
		for item in self.flags:
			try:
				tmp_flag = self.flags[item]['entity']
				tmp_flag.remove()
				tmp_pole = self.flags[item]['entity_pole']
				tmp_pole.remove()
				del self.flags[item]
			except:
				msg('ERROR', 'could not destroy flag {}').format(item)

	def draw_flag(self, item):
		players = []
		if 'ct_index' in self.flags[item]:
			players.extend(self.flags[item]['ct_index'])
		if 't_index' in self.flags[item]:
			players.extend(self.flags[item]['t_index'])
		HintText(message='{}: enemy is near!'.format(item)).send(players)

	def capture_flag(self, item, team, attacker_team = 'none'):
		self.flags[item]['draw'] = 0
		if self.flags[item]['status'] != team:
			# first neutralize flag if is not "none"
			if self.flags[item]['status'] != 'none':
				self.flags[item]['tmp_status'] = 'none'
				tmp_direction = 0
			else:
				self.flags[item]['tmp_status'] = team
				tmp_direction = 1
			cur_time = int(round(time.time(),0))
			players = []
			if 'ct_index' in self.flags[item]:
				players.extend(self.flags[item]['ct_index'])
			if 't_index' in self.flags[item]:
				players.extend(self.flags[item]['t_index'])
			# calculate time left
			if float(self.flags[item]['timestamp']) == 0 or self.flags[item]['tmp_conquered_by'] != team:
				self.flags[item]['timestamp'] = self.ontick_time
				self.flags[item]['tmp_conquered_by'] = team
				time_left = int(int(self.flags[item]['timer']) - float(self.flags[item]['timestamp']))
				if self.flags[item]['tmp_status'] == 'none':
					time_left += self.flags[item]['timer']
				HintText(message='{} captured for {} in {}'.format(item,team,time_left)).send(players)
			elif float(self.flags[item]['timestamp']) < int(self.flags[item]['timer']):
				self.flags[item]['timestamp'] += self.ontick_time
				self.set_flag_height(item, tmp_direction)
				time_left = int(int(self.flags[item]['timer']) - float(self.flags[item]['timestamp']))
				if self.flags[item]['tmp_status'] == 'none':
					time_left += self.flags[item]['timer']
				HintText(message='{} captured for {} in {}'.format(item,team,time_left)).send(players)
			# if flag belongs to one of the teams and now is "none"
			elif self.flags[item]['tmp_status'] == 'none':
				self.flags[item]['timestamp'] = 0
				self.respawn_flag(item, 'none')
			else:
				HintText(message='{} is captured by {}!'.format(item,team)).send(players)
				for index in self.flags[item][team.lower() + '_index']:
					player = Player(index)
					self.rank.player_add_cash(player.userid, 100)
				self.respawn_flag(item, team)
		else:
			# respawn flag if neccessary
			if float(self.flags[item]['timestamp']) > 0:
				self.respawn_flag(item, team)
			if 'count_' + attacker_team.lower() in self.flags[item]:
				if int(self.flags[item]['count_' + attacker_team.lower()]) > 0:
					self.draw_flag(item)

	def neutralize_flag(self, item):
		cur_time = int(round(time.time(),0))
		players = []
		if 'ct_index' in self.flags[item]:
			players.extend(self.flags[item]['ct_index'])
		if 't_index' in self.flags[item]:
			players.extend(self.flags[item]['t_index'])
		self.flags[item]['draw'] = 1
		HintText(message='{} is in draw!'.format(item)).send(players)
	
	def flag_circle(self, vector, radius, r, g, b, a=255):
		vector = Vector(vector[0], vector[1], vector[2] + 50)
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
			life_time=2,
			start_width=1,
			fade_length=0,
			flags=0,
			frame_rate=1,
			start_frame=0
		)

	def player_death(self, userid):
		try:
			player = Player.from_userid(userid)
			if player.team not in (2, 3):
				return
			if player.team == 3:
				self.tickets['ct'] = int(self.tickets['ct']) - 1
			else:
				self.tickets['t'] = int(self.tickets['t']) - 1
		except:
			msg('ERROR', 'could not remove a ticket on player_death')

	def ontick_flags(self):
		cur_time = int(round(time.time(),0))
		# reset counter for teams at flags
		for item in self.flags:
			self.flags[item]['count_t'] = 0
			self.flags[item]['count_ct'] = 0
			self.flags[item]['ct_index'] = []
			self.flags[item]['t_index'] = []
		# count every player in near of the flags
		for player in PlayerIter():
			if player.dead:
				continue
			if player.team not in (2,3):
				continue
			if player.frozen:
				continue
			# check if player is in near of a flag
			for item in self.flags:
				#get objects
				tmp_flag = self.flags[item]['entity']
				tmp_pole = self.flags[item]['entity_pole']
				# if player is in near of that flag
				if player.origin.get_distance(tmp_pole.origin) <= self.flags[item]['distance']:
					# add player to the list of flags
					if player.team == 3:
						self.flags[item]['count_ct'] += 1
						self.flags[item]['ct_index'].append(player.index)
					else:
						self.flags[item]['count_t'] += 1
						self.flags[item]['t_index'].append(player.index)
					# player can't be in the near of another flag so break the for loop
					break
		# check flags for some players in radius
		for item in self.flags:
			# get objects
			tmp_flag = self.flags[item]['entity']
			tmp_pole = self.flags[item]['entity_pole']
			# draw circle to mark radius of flag
			if int(self.flags[item]['last_glow']) <= cur_time:
				self.flags[item]['last_glow'] = cur_time + 2
				if self.flags[item]['status'] == 'T':
					self.flag_circle(tmp_pole.origin, self.flags[item]['distance'], 255, 0, 0)
				elif self.flags[item]['status'] == 'CT':
					self.flag_circle(tmp_pole.origin, self.flags[item]['distance'], 0, 0, 255)
				else:
					self.flag_circle(tmp_pole.origin, self.flags[item]['distance'], 255, 255, 255)
			# if there are no player in radius
			if int(self.flags[item]['count_t']) == 0 and int(self.flags[item]['count_ct']) == 0:
				# reset flag state
				if float(self.flags[item]['timestamp']) != 0:
					self.respawn_flag(item, self.flags[item]['status'])
				continue
			# if more T then CT
			if int(self.flags[item]['count_t']) > int(self.flags[item]['count_ct']):
				self.capture_flag(item, 'T', 'CT')
			# if more CT then T
			elif int(self.flags[item]['count_t']) < int(self.flags[item]['count_ct']):
				self.capture_flag(item, 'CT', 'T')
			# if both teams have the same amount of players in radius
			elif int(self.flags[item]['count_t']) == int(self.flags[item]['count_ct']):
				self.neutralize_flag(item)

	def ontick_tickets(self):
		cur_time = int(round(time.time(),0))
		if int(self.tickets['time']) <= cur_time:
			self.tickets['time'] = cur_time + 1
			tmp_t = 0
			tmp_ct = 0
			for item in self.flags:
				if self.flags[item]['status'] == 'CT':
					tmp_ct += 1
				elif self.flags[item]['status'] == 'T':
					tmp_t += 1
			if tmp_t > tmp_ct:
				self.tickets['ct'] = int(self.tickets['ct']) - (tmp_t - tmp_ct)
				if int(self.tickets['ct']) <= 0:
					self.tickets['ct'] = 0
					self.endround(8)
			elif tmp_t < tmp_ct:
				self.tickets['t'] = int(self.tickets['t']) - (tmp_ct - tmp_t)
				if int(self.tickets['t']) <= 0:
					self.tickets['t'] = 0
					self.endround(7)

	def ontick(self):
		# do not work on every tick
		self.ontick_time += global_vars.frame_time
		self.last_ontick += 1
		if self.last_ontick >= 16:
			self.last_ontick = 0
			self.ontick_flags()
			self.ontick_tickets()
			self.ontick_time = 0

	def restartround(self):
		ENDROUND_TEXT = 'endround'
		CVAR_ENDROUND = cvar.find_base(ENDROUND_TEXT)
		CVAR_ENDROUND.remove_flags(ConVarFlags.CHEAT)
		engine_server.server_command('{0};'.format(ENDROUND_TEXT))
		engine_server.server_execute()
		CVAR_ENDROUND.add_flags(ConVarFlags.CHEAT)

	def endround(self, condition):
		"""CSS:
		0 TERRORIST     "Target_Bombed"
		1 CT            "VIP_Escaped"
		2 TERRORIST     "VIP_Assassinated"
		3 TERRORIST     "Terrorists_Escaped"
		4 CT            "CTs_PreventEscape"
		5 CT            "Escaping_Terrorists_Neutralized"
		6 CT            "Bomb_Defused"
		7 CT            "CTs_Win"
		8 TERRORIST        "Terrorists_Win"
		9 World            "Round_Draw"
		10 CT            "All_Hostages_Rescued"
		11 CT            "Target_Saved"
		12 TERRORIST     "Hostages_Not_Rescued"
		13 CT            "Terrorists_Not_Escaped"
		14 TERRORIST    "VIP_Not_Escaped"
		15 World        "Game_Commencing"
		16 World        "UNKNOWN"
		"""
		if self.is_endround == False:
			self.is_endround = True
			info_map_parameters = Entity.find_or_create("info_map_parameters")
			info_map_parameters.call_input('FireWinCondition', condition)
			# play sound
			self.sounds.play_random('endround')