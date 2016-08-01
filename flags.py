# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from config.cvar import ConVar
from engines.precache import Model
from colors import Color
from listeners.tick import GameThread
from mathlib import Vector
from filters.recipients import RecipientFilter
from engines.server import global_vars, engine_server
from cvars.flags import ConVarFlags
from effects import polygon
from entities.entity import Entity
from messages import HintText
from filters.players import PlayerIter
from cvars import cvar
from menus import SimpleMenu
from players.entity import Player

from conquest.debug import msg
import time
import math

class flags:
	def __init__(self, db, rank, callbacks):
		self.num_tickets = ConVar("cq_numtickets", '500', 'number of tickets')
		self.tickets = {'t': self.num_tickets.get_int(), 'ct': self.num_tickets.get_int(), 'time': 0}
		self.color_ct = Color(0, 200, 255)
		self.color_n = Color(255, 255, 255)
		self.color_t = Color(255, 0, 0)
		self.flags = {}
		# height of the flag on pole
		self.flag_height = 120
		#self.model_flag = Model('models/props_equipment/light_floodlight.mdl')
		self.model_flag = Model('models/props_downtown/sign_stop.mdl')
		self.model_pole = Model('models/props/cs_italy/it_streetlampleg.mdl')
		self.model_beam = Model('sprites/laserbeam.vmt')
		self.db = db
		self.rank = rank
		self.callbacks = callbacks
		self.last_ontick = 0
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
				for item in self.flags:
					time_left = int(self.flags[item]['timestamp']) - cur_time
					if int(self.flags[item]['draw']) == 1:
						menu.append(self.flags[item]['name'] + ': DRAW')
					elif int(self.flags[item]['timestamp']) > 0 and time_left > 0:
						menu.append(self.flags[item]['name'] + ': ' + self.flags[item]['tmp_status']+ ' in ' + str(time_left))
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

	def spawn_flags(self):
		flags = self.get_flags()
		for row in flags:
			try:
				if row['name'] not in self.flags:
					# choose color based on status
					if row['status'] == 'T':
						color = self.color_t
					elif row['status'] == 'CT':
						color = self.color_ct
					else:
						color = self.color_n
					tmp_flag = Entity.create('prop_physics_override')
					tmp_flag.origin = Vector(row['X'], row['Y'], row['Z'] + self.flag_height)
					tmp_flag.model = self.model_flag
					tmp_flag.spawn_flags = 265
					tmp_flag.set_key_value_color('rendercolor', color)
					tmp_flag.spawn()
					tmp_pole = Entity.create('prop_physics_override')
					tmp_pole.origin = Vector(row['X'], row['Y'], row['Z'])
					tmp_pole.model = self.model_pole
					tmp_pole.spawn_flags = 265
					tmp_pole.set_key_value_color('rendercolor', color)
					tmp_pole.spawn()
					self.flags[row['name']] = {
						'name': row['name'],
						'X': row['X'],
						'Y': row['Y'],
						'Z': row['Z'],
						'spawnX': row['spawn_X'],
						'spawnY': row['spawn_Y'],
						'spawnZ': row['spawn_Z'],
						'distance': row['distance'],
						'type': row['type'],
						'timer': row['timer'],
						'status': row['status'],
						'tmp_status': row['status'],
						'draw': 0,
						'timestamp': '0',
						't_index' : [],
						'ct_index': [],
						'last_glow': 0,
						'entity': tmp_flag,
						'entity_pole': tmp_pole,
					}
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
				elif status == 'CT':
					color = self.color_ct
				else:
					color = self.color_n
				if flag is not None:
					if flag['name'] not in self.flags:
						tmp_flag = Entity.create('prop_physics_override')
						tmp_flag.origin = Vector(flag['X'], flag['Y'], flag['Z'] + self.flag_height)
						tmp_flag.model = self.model_flag
						tmp_flag.spawn_flags = 265
						tmp_flag.set_key_value_color('rendercolor', color)
						tmp_flag.spawn()
						tmp_pole = Entity.create('prop_physics_override')
						tmp_pole.origin = Vector(flag['X'], flag['Y'], flag['Z'])
						tmp_pole.model = self.model_pole
						tmp_pole.spawn_flags = 265
						tmp_pole.set_key_value_color('rendercolor', color)
						tmp_pole.spawn()
						self.flags[flag['name']] = {
							'name': flag['name'],
							'X': flag['X'],
							'Y': flag['Y'],
							'Z': flag['Z'],
							'spawnX': flag['spawn_X'],
							'spawnY': flag['spawn_Y'],
							'spawnZ': flag['spawn_Z'],
							'distance': flag['distance'],
							'type': flag['type'],
							'timer': flag['timer'],
							'status': status,
							'tmp_status': status,
							'draw': 0,
							'timestamp': '0',
							't_index' : [],
							'ct_index': [],
							'last_glow': 0,
							'entity': tmp_flag,
							'entity_pole': tmp_pole,
						}
					else:
						tmp_flag = self.flags[name]['entity']
						tmp_flag.remove()
						tmp_pole = self.flags[name]['entity_pole']
						tmp_pole.remove()
						del self.flags[name]
						del tmp_flag
						tmp_flag = Entity.create('prop_physics_override')
						tmp_flag.origin = Vector(flag['X'], flag['Y'], flag['Z'] + self.flag_height)
						tmp_flag.model = self.model_flag
						tmp_flag.spawn_flags = 265
						tmp_flag.set_key_value_color('rendercolor', color)
						tmp_flag.spawn()
						tmp_pole = Entity.create('prop_physics_override')
						tmp_pole.origin = Vector(flag['X'], flag['Y'], flag['Z'])
						tmp_pole.model = self.model_pole
						tmp_pole.spawn_flags = 265
						tmp_pole.set_key_value_color('rendercolor', color)
						tmp_pole.spawn()
						self.flags[flag['name']] = {
							'name': flag['name'],
							'X': flag['X'],
							'Y': flag['Y'],
							'Z': flag['Z'],
							'spawnX': flag['spawn_X'],
							'spawnY': flag['spawn_Y'],
							'spawnZ': flag['spawn_Z'],
							'distance': flag['distance'],
							'type': flag['type'],
							'timer': flag['timer'],
							'status': status,
							'tmp_status': status,
							'draw': 0,
							'timestamp': '0',
							't_index' : [],
							'ct_index': [],
							'last_glow': 0,
							'entity': tmp_flag,
							'entity_pole': tmp_pole,
						}
		except:
			msg('ERROR', 'could not respawn a specific flag')

	def set_flag_height(self, item):
		if item in self.flags:
			tmp_flag = self.flags[item]['entity']
			cur_time = int(round(time.time(),0))
			time_left = int(self.flags[item]['timestamp']) - cur_time
			lowest_z = self.flags[item]['Z']
			flag_height = self.flag_height
			tmp = flag_height / self.flags[item]['timer']
			z = (time_left * tmp) + lowest_z
			tmp_flag.origin = Vector(tmp_flag.origin[0], tmp_flag.origin[1], z)



	def reset_flags(self):
		self.flags = {}

	def reset_tickets(self):
		self.tickets = {'t': self.num_tickets.get_int(), 'ct': self.num_tickets.get_int(), 'time': 0}

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

	def capture_flag(self, item, team):
		self.flags[item]['draw'] = 0
		if self.flags[item]['status'] != team:
			self.flags[item]['tmp_status'] = team
			cur_time = int(round(time.time(),0))
			players = []
			if 'ct_index' in self.flags[item]:
				players.extend(self.flags[item]['ct_index'])
			if 't_index' in self.flags[item]:
				players.extend(self.flags[item]['t_index'])
			if int(self.flags[item]['timestamp']) == 0:
				self.flags[item]['timestamp'] = cur_time + int(self.flags[item]['timer'])
				time_left = int(self.flags[item]['timestamp']) - cur_time
				HintText(message='{} captured for {} in {}'.format(item,team,time_left)).send(players)
			elif int(self.flags[item]['timestamp']) > cur_time:
				time_left = int(self.flags[item]['timestamp']) - cur_time
				self.set_flag_height(item)
				HintText(message='{} captured for {} in {}'.format(item,team,time_left)).send(players)
			else:
				HintText(message='{} is captured by {}!'.format(item,team)).send(players)
				for index in self.flags[item][team.lower() + '_index']:
					player = Player(index)
					self.rank.player_add_cash(player.userid, 100)
				self.respawn_flag(item, team)

	def neutralize_flag(self, item):
		cur_time = int(round(time.time(),0))
		players = []
		if 'ct_index' in self.flags[item]:
			players.extend(self.flags[item]['ct_index'])
		if 't_index' in self.flags[item]:
			players.extend(self.flags[item]['t_index'])
		self.flags[item]['draw'] = 1
		# in draw the countdown should not go on.. so we need to "freeze" the time
		self.flags[item]['timestamp'] = (int(self.flags[item]['timestamp']) - cur_time) + cur_time
		HintText(message='{} is in draw!'.format(item)).send(players)

	def spawn_flag_circle(self, vector, radius, r, g, b, a=255):
		t = GameThread(target=self.flag_circle, args=(vector, radius, r, g, b, a,))
		t.start()

	def flag_circle(self, vector, radius, r, g, b, a=255):
		try:
			xc = vector[0]
			yc = vector[1]
			zc = vector[2]
			points = []
			for steps in range(1, 42):
				phi = (2*math.pi/40)*steps
				x = radius*math.cos(phi)
				y = radius*math.sin(phi)
				points.append(Vector(xc+x,yc+y,zc+50))
			polygon(
				RecipientFilter(),
				points,
				alpha=a,
				blue=b,
				green=g,
				red=r,
				amplitude=0,
				end_width=1,
				life_time=2,
				start_width=1,
				fade_length=0,
				flags=0,
				frame_rate=1,
				halo=self.model_beam,
				model=self.model_beam,
				start_frame=0
			)
		except:
			msg('ERROR', 'could not spawn a circle for flag')
			return None

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

	def ontick(self):
		cur_time = int(round(time.time(),0))
		self.last_ontick += 1
		if self.last_ontick >= 32:
			self.last_ontick = 0
			# reset counter for all flags (we need to count them again)
			for item in self.flags:
				self.flags[item]['count_t'] = 0
				self.flags[item]['count_ct'] = 0
				self.flags[item]['ct_index'] = []
				self.flags[item]['t_index'] = []
			# count every player in near of the flags
			for player in PlayerIter():
				if player.dead:
					continue
				if player.team not in (2, 3):
					continue
				if player.frozen:
					continue
				for item in self.flags:
					tmp_flag = self.flags[item]['entity']
					tmp_pole = self.flags[item]['entity_pole']
					if player.origin.get_distance(tmp_pole.origin) <= self.flags[item]['distance']:
						if player.team == 3:
							self.flags[item]['count_ct'] += 1
							self.flags[item]['ct_index'].append(player.index)
						else:
							self.flags[item]['count_t'] += 1
							self.flags[item]['t_index'].append(player.index)
			# if some players in the radius of a flag
			for item in self.flags:
				tmp_flag = self.flags[item]['entity']
				tmp_pole = self.flags[item]['entity_pole']
				# if more T then CT
				if self.flags[item]['count_t'] > self.flags[item]['count_ct']:
					self.capture_flag(item, 'T')
				# if more CT then T
				elif self.flags[item]['count_t'] < self.flags[item]['count_ct']:
					self.capture_flag(item, 'CT')
				# if we have both teams same size in the near
				elif self.flags[item]['count_t'] > 0 and self.flags[item]['count_ct'] > 0:
					self.neutralize_flag(item)
				# reset the flag state...
				elif self.flags[item]['timestamp'] != '0':
					self.respawn_flag(item, self.flags[item]['status'])
				# circle around flags
				if int(self.flags[item]['last_glow']) <= cur_time:
					self.flags[item]['last_glow'] = cur_time + 2
					if self.flags[item]['status'] == 'T':
						self.spawn_flag_circle(Vector(self.flags[item]['X'], self.flags[item]['Y'], self.flags[item]['Z']), self.flags[item]['distance'], 255, 0, 0)
					elif self.flags[item]['status'] == 'CT':
						self.spawn_flag_circle(Vector(self.flags[item]['X'], self.flags[item]['Y'], self.flags[item]['Z']), self.flags[item]['distance'], 0, 0, 255)
					else:
						self.spawn_flag_circle(Vector(self.flags[item]['X'], self.flags[item]['Y'], self.flags[item]['Z']), self.flags[item]['distance'], 255, 255, 255)
		if int(self.tickets['time']) <= cur_time:
			self.tickets['time'] = cur_time + 1
			tmp_t = 0
			tmp_ct = 0
			for item in self.flags:
				if self.flags[item]['status'] == 'CT':
					tmp_ct += 1
				elif self.flags[item]['status'] == 'T':
					tmp_t += 1
			if tmp_t > tmp_ct and int(self.tickets['ct']) > 0:
				self.tickets['ct'] = int(self.tickets['ct']) - (tmp_t - tmp_ct)
				if int(self.tickets['ct']) <= 0:
					self.tickets['ct'] = 0
					self.endround(8)
			elif tmp_t < tmp_ct and int(self.tickets['t']) > 0:
				self.tickets['t'] = int(self.tickets['t']) - (tmp_ct - tmp_t)
				if int(self.tickets['t']) <= 0:
					self.tickets['t'] = 0
					self.endround(7)
			else:
				if int(self.tickets['ct']) <= 0 or int(self.tickets['t']) <= 0:
					if int(self.tickets['ct']) < int(self.tickets['t']):
						self.endround(8)
					elif int(self.tickets['ct']) > int(self.tickets['t']):
						self.endround(7)

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
		info_map_parameters = Entity.find_or_create("info_map_parameters")
		info_map_parameters.call_input('FireWinCondition', condition)