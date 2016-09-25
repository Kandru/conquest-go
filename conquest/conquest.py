# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from events import Event
from listeners import OnTick, OnPluginLoaded, OnPluginUnloaded
from players.entity import Player
from filters.entities import EntityIter
from entities.entity import Entity
from entities.helpers import edict_from_pointer
from entities.hooks import EntityCondition
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
from memory import make_object

from conquest.mysql import mysql
from conquest.flags import flags
from conquest.respawn import respawn
from conquest.rank import rank
from conquest.callbacks import callbacks
from conquest.downloads import downloads
from conquest.weapons import weapons
from conquest.sounds import sounds

class_mysql = None
class_flags = None
class_respawn = None
class_rank = None
class_weapons = None
class_sounds = None

_bump_player = None

@OnPluginLoaded
def pload(var):
	global class_mysql, class_flags, class_respawn, class_rank, class_weapons, class_sounds
	class_mysql = mysql()
	class_downloads = downloads(class_mysql)
	class_sounds = sounds(class_mysql, class_downloads)
	class_callbacks = callbacks()
	class_rank = rank(class_mysql, class_callbacks, class_downloads)
	class_flags = flags(class_mysql, class_rank, class_callbacks, class_sounds)
	class_respawn = respawn(class_callbacks)
	class_weapons = weapons(class_mysql, class_downloads, class_rank)

@OnPluginUnloaded
def punload(var):
	class_flags.reset_flags()

@OnTick
def tick_listener():
	global class_flags, class_weapons
	if class_flags is not None:
		class_flags.ontick()
	if class_weapons is not None:
		class_weapons.ontick()

@Event('round_start')
def round_start(event):
	global class_flags
	class_flags.reset_flags()
	class_flags.reset_tickets()
	class_flags.spawn_flags()
	# remove all hostages
	for item in EntityIter('hostage_entity'):
		item.remove()

@Event('round_end')
def round_end(event):
	global class_flags
	class_flags.reset_flags()

@Event('player_death')
def player_death(event):
	global class_respawn, class_flags, class_rank, class_weapons
	class_respawn.player_death(event['userid'])
	class_flags.player_death(event['userid'])
	class_rank.player_death(event['userid'], event['attacker'])
	class_weapons.player_death(event['userid'])

@Event('player_spawn')
def player_spawn(event):
	global class_respawn, class_flags, class_rank
	player = Player.from_userid(event['userid'])
	class_respawn.player_spawn(event['userid'], class_flags.flags)
	class_rank.player_spawn(event['userid'])

@Event('player_team')
def player_team(event):
	global class_respawn
	# only fire event if player is not disconnecting
	if event['disconnect'] == False:
		class_respawn.player_team(event['userid'], event['oldteam'], event['team'])

@Event('player_connect_full')
def player_connect_full(event):
	global class_rank
	class_rank.player_connect_full(event['userid'])

@Event('player_disconnect')
def player_disconnect(event):
	global class_weapons
	class_weapons.player_disconnect(event['userid'])

@Event('begin_new_match')
def begin_new_match(event):
	global class_rank
	class_rank.begin_new_match()
	
@Event('bomb_dropped')
def bomb_dropped(event):
	global class_weapons
	class_weapons.bomb_dropped(event['userid'], event['entindex'])

@Event('bomb_beep')
def bomb_beep(event):
	global class_weapons
	class_weapons.bomb_beep(event['entindex'])

@Event('player_say')
def player_say(event):
	global class_rank
	class_rank.player_say(event['userid'], event['text'])
	#player = Player.from_userid(event['userid'])
	
@EntityPreHook(EntityCondition.is_human_player, 'bump_weapon')
def _pre_bump_weapon(args):
	"""Switch the player's team if they are a CT picking up the bomb."""
	global _bump_player
	if edict_from_pointer(args[1]).classname != 'weapon_c4':
		return
	_bump_player = make_object(Player, args[0])
	if _bump_player.team == 3:
		Entity(_bump_player.index).team = 2
	else:
		_bump_player = None


@EntityPostHook(EntityCondition.is_human_player, 'bump_weapon')
def _post_bump_weapon(args, return_value):
	"""Switch the player's team back to CT if they just picked up the bomb."""
	global _bump_player
	if _bump_player is None:
		return
	Entity(_bump_player.index).team = 3
	_bump_player = None
