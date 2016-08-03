# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from events import Event
from listeners import OnTick
from listeners.tick import Delay
from players.entity import Player
from entities.entity import Entity
from engines.sound import Sound, StreamSound

from conquest.mysql import mysql
from conquest.flags import flags
from conquest.respawn import respawn
from conquest.rank import rank
from conquest.callbacks import callbacks
from conquest.downloads import downloads

class_mysql = None
class_flags = None
class_respawn = None
class_rank = None

player1 = None
player2 = None

@Event('load')
def load():
	global class_mysql, class_flags, class_respawn, class_rank
	class_mysql = mysql()
	class_downloads = downloads(class_mysql)
	class_callbacks = callbacks()
	class_rank = rank(class_mysql, class_callbacks, class_downloads)
	class_flags = flags(class_mysql, class_rank, class_callbacks)
	class_respawn = respawn(class_callbacks)

@Event('unload')
def unload():
	class_flags.reset_flags()

@OnTick
def tick_listener():
	global class_flags
	if class_flags is not None:
		class_flags.ontick()

@Event('round_start')
def round_start(event):
	global class_flags
	class_flags.reset_flags()
	class_flags.reset_tickets()
	class_flags.spawn_flags()

@Event('round_end')
def round_end(event):
	global class_flags
	class_flags.reset_flags()

@Event('player_death')
def player_death(event):
	global class_respawn, class_flags, class_rank
	class_respawn.player_death(event['userid'])
	class_flags.player_death(event['userid'])
	class_rank.player_death(event['userid'], event['attacker'])

@Event('player_spawn')
def player_spawn(event):
	global class_respawn, class_flags, class_rank
	player = Player.from_userid(event['userid'])
	class_respawn.player_spawn(event['userid'], class_flags.flags)
	class_rank.player_spawn(event['userid'])
	
@Event('player_connect_full')
def player_connect_full(event):
	global class_rank
	class_rank.player_connect_full(event['userid'])
	
@Event('begin_new_match')
def begin_new_match(event):
	global class_rank
	class_rank.begin_new_match()

@Event('player_say')
def player_say(event):
	global class_rank, class_flags, player1, player2, chicken_coord
	class_rank.player_say(event['userid'], event['text'])
	player = Player.from_userid(event['userid'])
	#player.give_named_item("weapon_hegrenade", 0, None, True)
	print(str(player.origin))
	#class_rank.player_add_cash(event['userid'],1000)
	#if event['text'] == '1':
	#	player1 = event['userid']
	#if event['text'] == '2':
	#	player2 = event['userid']
	#if player1 is not None and player2 is not None:
	#	tmp = Player.from_userid(player2)
	#	print(player.origin.get_distance(tmp.origin))
	#class_flags.spawn_flag_circle(player.origin, int(event['text']), 255, 255, 255)
	#test = StreamSound("music/conquest/3.mp3", download=True)
	#test.play([player.index])
	#class_flags.endround(7)
	#Sound('conquest/flags_v1/your_team_scores.wav', index=player.index, attenuation=Attenuation.STATIC).play()