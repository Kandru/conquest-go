# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from stringtables.downloads import Downloadables
from conquest.debug import msg

class downloads:
	def __init__(self, db):
		self.db = db
		self.downloads = Downloadables()

	def add(self, file):
		self.downloads.add(file)
		msg('INFO', 'added download {}'.format(file))

### list of available callbacks
## player_is_spawned
# When a player is definately read to spawn (e.G. after choosing class, weapon, ... and is ready to play) needed for make sure that a player choose a weapon and class before starts to play / getting attacked