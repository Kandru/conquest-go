# CONQUEST:GO
# https://github.com/Kandru/conquest-go
# author: Karl-Martin Minkner
# website: https://gameshare.community

import time

from core import echo_console

def msg(type, msg):
	echo_console('[CONQUEST][{}][{}] {}'.format(time.strftime("%d.%m.%Y - %H:%M:%S"),type,msg))