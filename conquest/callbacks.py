# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from listeners.tick import GameThread

class callbacks:
	def __init__(self):
		self.callbacks = {}

	def register(self, callback, key, function):
		if not callback in self.callbacks:
			self.callbacks[callback] = {}
		self.callbacks[callback][key] = function

	def execute(self, callback, values):
		if callback in self.callbacks:
			for key, func in self.callbacks[callback].items():
				t = GameThread(target=func, args=(values,))
				t.daemon = True
				t.start()

### list of available callbacks
## player_is_spawned
# When a player is definately read to spawn (e.G. after choosing class, weapon, ... and is ready to play) needed for make sure that a player choose a weapon and class before starts to play / getting attacked