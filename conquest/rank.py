# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

import json
from threading import Lock

from players.entity import Player
from entities.entity import Entity
from menus import PagedOption
from messages import SayText2
from engines.precache import Model
from colors import Color

from conquest.debug import msg
from conquest.extendedpagedmenu import ExtendedPagedMenu

class rank:
	def __init__(self, db, callbacks, downloads):
		self.db = db
		self.callbacks = callbacks
		self.downloads = downloads
		self.color_ct = Color(0, 200, 255)
		self.color_n = Color(255, 255, 255)
		self.color_t = Color(255, 0, 0)
		self.ranks = {}
		self.players = {}
		self.classes = {}
		self.weapons = {}
		self.skins = {}
		self.get_ranks()
		self.get_classes()
		self.get_weapons()
		self.get_skins()
		self.player_data_lock = Lock()

	def get_ranks(self):
		sql = "SELECT * FROM ranks ORDER BY id ASC"
		rows = self.db.query(sql)
		for row in rows:
			self.ranks[row['id']] = row

	def get_classes(self):
		sql = "SELECT * FROM classes ORDER BY id ASC"
		rows = self.db.query(sql)
		for row in rows:
			self.classes[row['id']] = row

	def get_weapons(self):
		sql = "SELECT * FROM weapons ORDER BY id ASC"
		rows = self.db.query(sql)
		for row in rows:
			self.weapons[row['id']] = row
			
	def get_skins(self):
		sql = "SELECT * FROM skins ORDER BY id ASC"
		rows = self.db.query(sql)
		for row in rows:
			if row['downloadlist']:
				for item in row['downloadlist'].splitlines():
					self.downloads.add(item.strip())
			row['model'] = Model(row['modelpath'])
			self.skins[row['id']] = row

	def get_player_cached_data(self, userid):
		try:
			player = Player.from_userid(userid)
			self.player_data_lock.acquire()
			if player.steamid in self.players:
				row = self.players[player.steamid]
			else:
				row = None
			self.player_data_lock.release()
			return row
		except:
			msg('ERROR','could not get player cached data')
	
	def get_player_data(self, userid):
		try:
			player = Player.from_userid(userid)
			sql = "SELECT * FROM players WHERE steamid = %s LIMIT 0,1"
			row = self.db.query(sql, (player.steamid,), fetch_all = False)
			if row:
				player.cash = row['cash']
				if row['rank']:
					row['rank'] = json.loads(row['rank'])
				if row['skin']:
					row['skin'] = json.loads(row['skin'])
			else:
				# if user does not exist in our database
				self.insert_player_data(userid)
				row = self.get_player_data(userid)
			self.player_data_lock.acquire()
			self.players[player.steamid] = row
			self.player_data_lock.release()
			return row
		except:
			msg('ERROR','could not get player data')

	def insert_player_data(self, userid):
		try:
			player = Player.from_userid(userid)
			tmp_rank = {}
			for item in self.classes:
				tmp_rank[item] = 1
			sql = "INSERT INTO `players` (`steamid`, `username`, `rank`, `cash`)VALUES(%s,%s,%s,%s)"
			self.db.query(sql, (player.steamid,player.name,json.dumps(tmp_rank),0,))
		except:
			msg('ERROR', 'could not insert player data')

	def update_player_data(self, userid, data):
		try:
			player = Player.from_userid(userid)
			tmp_keys = ''
			tmp_values = []
			lock = False
			self.player_data_lock.acquire()
			lock = True
			for item in data:
				tmp_keys = tmp_keys + ', ' + item + ' = %s'
				tmp_values.append(data[item])
				if item == 'rank':
					data[item] = json.loads(data[item])
				self.players[player.steamid][item] = data[item]
			self.player_data_lock.release()
			lock = False
			tmp_values.append(player.steamid)
			sql = "UPDATE `players` SET " + tmp_keys[1:] + " WHERE steamid = %s"
			self.db.query(sql, tmp_values)
		except:
			if lock:
				self.player_data_lock.release()
			msg('ERROR', 'could not update player data')
			
	def player_connect_full(self, userid):
		# initialize player data
		self.get_player_data(userid)
		# reset player data
		self.update_player_data(userid, {'spawn_menu_active': 0})
			
	def player_spawn(self, userid):
		try:
			player = Player.from_userid(userid)
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			# update player data dict (to have right cash value etc)
			pdata = self.get_player_data(userid)
			# only in real match, not in warmup...
			if int(pdata['spawn_menu_active']) == 0:
				self.update_player_data(userid, {'spawn_menu_active': 1})
				if int(pdata['class']) == 0:
					self.menu_select_class(userid)
				# if a user does not have chosen a weapon we need to help him...
				elif not pdata['loadout1']: #fixme open menu if someone hasnt a weapon for a specific class...
					self.menu_select_pweapon(userid)
				else:
					# if player want to change weapons on next respawn
					if int(pdata['change_loadout1']) == 1:
						self.update_player_data(player.userid, {
							'change_loadout1': 0
						})
						self.menu_select_pweapon(userid)
					elif int(pdata['change_class']) == 1:
						self.update_player_data(player.userid, {
							'change_class': 0
						})
						self.menu_select_class(userid)
					elif int(pdata['change_skin']) == 1:
						self.update_player_data(player.userid, {
							'change_skin': 0
						})
						self.menu_select_skin(userid)
					else:
						self.player_give_weapon(userid)
			else:
				self.player_give_weapon(userid)
			# set player skin
			if pteam in pdata['skin']:
				if int(pdata['skin'][pteam]) != 0:
					self.player_set_model(userid, pdata['skin'][pteam])
		except:
			msg('ERROR', 'could not grep player rank data')

	def player_death(self, userid, attacker):
		try:
			player = Player.from_userid(attacker)
			self.update_player_data(attacker, {
				'cash': player.cash,
				'username': player.name,
				'spawn_menu_active': 0
			})
			self.player_check_rank(attacker)
			player = Player.from_userid(userid)
			self.update_player_data(userid, {
				'cash': player.cash,
				'username': player.name,
				'spawn_menu_active': 0
			})
			self.player_check_rank(userid)
		except:
			msg('ERROR', 'could not save player rank data')

	def player_say(self, userid, text):
		try:
			player = Player.from_userid(userid)
			self.player_data_lock.acquire()
			if player.steamid not in self.players:
				self.player_data_lock.release()
				return
			self.player_data_lock.release()
			# change weapons
			change_weapons = ['!weapon','!weapons','!changeweapon','!changeweapons','!loadout','!changeloadout','!w','!cw']
			if text in change_weapons:
				self.update_player_data(userid, {
					'change_loadout1': 1
				})
				SayText2('You can change your loadout on next respawn!').send(player.index)
			# change class
			change_class = ['!class','!selectclass','!changeclass','!c','!sc']
			if text in change_class:
				self.update_player_data(userid, {
					'change_class': 1
				})
			# change skin
			change_skin = ['!skin','!selectskin','!changeskin','!s']
			if text in change_skin:
				self.update_player_data(userid, {
					'change_skin': 1
				})
				SayText2('You can change your skin on next respawn!').send(player.index)
		except:
			msg('ERROR', 'could not work with player say event')

	def player_set_model(self, userid, modelid):
		try:
			player = Player.from_userid(userid)
			if int(modelid) in self.skins:
				player.model = self.skins[int(modelid)]['model']
		except:
			msg('ERROR', 'could not set player model')
			
	def player_check_rank(self, userid):
		try:
			player = Player.from_userid(userid)
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			pdata = self.get_player_data(userid)
			if player.steamid in self.players:
				new_rank = int(pdata['rank'][str(pdata['class'])]) + 1
				if new_rank in self.ranks:
					if player.cash >= int(self.ranks[new_rank]['points_needed']):
						player.cash = player.cash - int(self.ranks[new_rank]['points_needed'])
						pdata['rank'][str(pdata['class'])] = int(new_rank)
						self.update_player_data(userid, {
							'cash': player.cash,
							'rank': json.dumps(pdata['rank'])
						})
						SayText2('New Rank: {} ({})'.format(str(new_rank), self.classes[pdata['class']]['name'])).send(player.index)
						for item in self.weapons:
							if int(self.weapons[item]['rank']) == int(new_rank) and pteam == self.weapons[item]['team'] and int(pdata['class']) == self.weapons[item]['class']:
								SayText2('New Weapon: {}'.format(self.weapons[item]['name'])).send(player.index)
								# ability to change weapon on next spawn because of a new weapon
								self.update_player_data(userid, {
									'change_loadout1': 1
								})
						self.player_check_rank(userid)
						#TODO: notification for new rank (e.G. Sound?)
		except:
			msg('ERROR', 'could not check player rank')
			self.player_data_lock.release()

	def player_add_cash(self, userid, amount):
		try:
			player = Player.from_userid(userid)
			player.cash = player.cash + amount
			self.update_player_data(userid, {
				'cash': player.cash
			})
			self.player_check_rank(userid)
		except:
			msg('ERROR', 'could not add {} cash to userid {}'.format(amount, userid))

	def player_give_weapon(self, userid):
		try:
			player = Player.from_userid(userid)
			if not player.address:
				return
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			pdata = self.get_player_data(userid)
			for index in player.weapon_indexes():
				weapon = Entity(index)
				player.drop_weapon(weapon.pointer, player.origin, player.origin)
				weapon.remove()
			# get new weapons
			player.give_named_item('weapon_knife', 0, None, True)
			loadout1 = json.loads(pdata['loadout1'])
			if pteam in loadout1:
				if str(pdata['class']) in loadout1[pteam]:
					if 'primary' in loadout1[pteam][str(pdata['class'])]:
						player.give_named_item(loadout1[pteam][str(pdata['class'])]['primary'], 0, None, True)
					if 'secondary' in loadout1[pteam][str(pdata['class'])]:
						player.give_named_item(loadout1[pteam][str(pdata['class'])]['secondary'], 0, None, True)
					for item in self.weapons:
						if int(self.weapons[item]['rank']) <= int(pdata['rank'][str(pdata['class'])]) and int(self.weapons[item]['type']) == 3 and pteam == self.weapons[item]['team'] and int(pdata['class']) == self.weapons[item]['class']:
							for x in range(0, self.weapons[item]['amount']):
								player.give_named_item(self.weapons[item]['slug'], 0, None, True)
			# give kevlar (and helmet on lvl 20 or above)
			if int(pdata['rank'][str(pdata['class'])]) < 20:
				player.give_named_item('item_kevlar', 0, None, True)
			else:
				player.give_named_item('item_assaultsuit', 0, None, True)
			# ready for spawn let other plugins know
			self.callbacks.execute('player_is_spawned', player.userid)
		except:
			msg('INFO', 'could not give weapon to player')

	def menu_select_class(self, userid):
		player = Player.from_userid(userid)
		pdata = self.get_player_data(userid)
		menu = ExtendedPagedMenu(title='Select Class', select_callback=self.menu_select_class_callback, on_close_menu=self.menu_select_class_close_callback)
		for item in self.classes:
			menu.append(PagedOption('{}, Rank: {}'.format(self.classes[item]['name'], pdata['rank'][str(item)]), str(item), selectable=True))
		menu.send(player.index)

	def menu_select_class_callback(self, menu, pindex, option):
		try:
			player = Player(pindex)
			self.update_player_data(player.userid, {
				'class': option.value
			})
			self.menu_select_pweapon(player.userid)
		except:
			msg('ERROR', 'could not send select class callback to player')

	def menu_select_class_close_callback(self, menu, pindex):
		try:
			player = Player(pindex)
			self.menu_select_class(player.userid)
		except:
			msg('ERROR', 'could not send class close callback to player')
			
	def menu_select_skin(self, userid):
		player = Player.from_userid(userid)
		if player.team == 3:
			pteam = 'CT'
		else:
			pteam = 'T'
		pdata = self.get_player_data(userid)
		menu = ExtendedPagedMenu(title='Select Skin', select_callback=self.menu_select_skin_callback, on_close_menu=self.menu_skin_close_callback)
		for item in self.skins:
			# only if the usergroup is high enough
			if int(self.skins[item]['group']) <= int(pdata['group']) and (self.skins[item]['team'] == pteam or not self.skins[item]['team']):
				menu.append(PagedOption('{}'.format(self.skins[item]['name']), str(item), selectable=True))
		menu.append(PagedOption('default skin', str(0), selectable=True))
		menu.send(player.index)

	def menu_select_skin_callback(self, menu, pindex, option):
		#try:
		player = Player(pindex)
		self.player_set_model(player.userid, option.value)
		if player.team == 3:
			pteam = 'CT'
		else:
			pteam = 'T'
		pdata = self.get_player_data(player.userid)
		if not pdata['skin']:
			pdata['skin'] = {pteam: option.value}
		pdata['skin'][pteam] = option.value
		self.update_player_data(player.userid, {
			'change_skin': 0,
			'skin': json.dumps(pdata['skin'])
		})
		self.player_give_weapon(player.userid)
		#except:
		#	msg('ERROR', 'could not send select skin callback to player')
	
	def menu_skin_close_callback(self, menu, pindex):
		try:
			player = Player(pindex)
			self.player_give_weapon(player.userid)
		except:
			msg('ERROR', 'could not send skin callback menu to player')	
	
	def menu_select_pweapon(self, userid):
		try:
			player = Player.from_userid(userid)
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			pdata = self.get_player_data(userid)
			menu = ExtendedPagedMenu(title='Primary Weapon', select_callback=self.menu_select_pweapon_callback, on_close_menu=self.menu_select_pweapon_close_callback)
			for item in self.weapons:
				if int(self.weapons[item]['rank']) <= int(pdata['rank'][str(pdata['class'])]) and int(self.weapons[item]['type']) == 1 and pteam == self.weapons[item]['team'] and int(pdata['class']) == self.weapons[item]['class']:
					menu.append(PagedOption('{}'.format(self.weapons[item]['name']), str(item), selectable=True))
			menu.send(player.index)
		except:
			msg('ERROR', 'could not send select pweapon menu to player')

	def menu_select_pweapon_callback(self, menu, pindex, option):
		try:
			player = Player(pindex)
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			pdata = self.get_player_data(player.userid)
			if pdata['loadout1']:
				loadout1 = json.loads(pdata['loadout1'])
			else:
				loadout1 = {}
			if pteam not in loadout1:
				loadout1[pteam] = {}
			if str(pdata['class']) not in loadout1[pteam]:
				loadout1[pteam][str(pdata['class'])] = {}
			if 'primary' not in loadout1[pteam][str(pdata['class'])]:
				loadout1[pteam][str(pdata['class'])]['primary'] = ''
			loadout1[pteam][str(pdata['class'])]['primary'] = self.weapons[int(option.value)]['slug']
			self.update_player_data(player.userid, {
				'loadout1': json.dumps(loadout1)
			})
			self.menu_select_sweapon(player.userid)
		except:
			msg('ERROR', 'could not send select pweapon callback menu to player')

	def menu_select_pweapon_close_callback(self, menu, pindex):
		try:
			player = Player(pindex)
			self.menu_select_pweapon(player.userid)
		except:
			msg('ERROR', 'could not send pweapon close callback menu to player')

	def menu_select_sweapon(self, userid):
		try:
			player = Player.from_userid(userid)
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			pdata = self.get_player_data(userid)
			menu = ExtendedPagedMenu(title='Secondary Weapon', select_callback=self.menu_select_sweapon_callback, on_close_menu=self.menu_select_sweapon_close_callback)
			for item in self.weapons:
				if int(self.weapons[item]['rank']) <= int(pdata['rank'][str(pdata['class'])]) and int(self.weapons[item]['type']) == 2 and pteam == self.weapons[item]['team'] and int(pdata['class']) == self.weapons[item]['class']:
					menu.append(PagedOption('{}'.format(self.weapons[item]['name']), str(item), selectable=True))
			menu.send(player.index)
		except:
			msg('ERROR', 'could not send select sweapon menu to player')

	def menu_select_sweapon_callback(self, menu, pindex, option):
		try:
			player = Player(pindex)
			if player.team == 3:
				pteam = 'CT'
			else:
				pteam = 'T'
			pdata = self.get_player_data(player.userid)
			if pdata['loadout1']:
				loadout1 = json.loads(pdata['loadout1'])
			else:
				loadout1 = {}
			if pteam not in loadout1:
				loadout1[pteam] = {}
			if str(pdata['class']) not in loadout1[pteam]:
				loadout1[pteam][str(pdata['class'])] = {}
			if 'secondary' not in loadout1[pteam][str(pdata['class'])]:
				loadout1[pteam][str(pdata['class'])]['secondary'] = ''
			loadout1[pteam][str(pdata['class'])]['secondary'] = self.weapons[int(option.value)]['slug']
			self.update_player_data(player.userid, {
				'loadout1': json.dumps(loadout1)
			})
			self.player_give_weapon(player.userid)
		except:
			msg('ERROR', 'could not send select sweapon callback menu to player')

	def menu_select_sweapon_close_callback(self, menu, pindex):
		try:
			player = Player(pindex)
			self.menu_select_sweapon(player.userid)
		except:
			msg('ERROR', 'could not send select sweapon close callback menu to player')