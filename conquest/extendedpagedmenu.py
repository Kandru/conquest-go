# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

from menus.radio import BUTTON_CLOSE
from menus import PagedMenu

class ExtendedPagedMenu(PagedMenu):
	def __init__(self, *args, on_close_menu=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.on_close_menu = on_close_menu

	def _select(self, player_index, choice_index):
		if choice_index == BUTTON_CLOSE and self.on_close_menu is not None:
			return self.on_close_menu(self, player_index)
		return super()._select(player_index, choice_index)


	def on_close_menu(menu, player_index):
		pass