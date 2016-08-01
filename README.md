# conquest-go
a battlefield series style conquest mod for counter-strike:global offensive

## introduction
conquest:go is an mod written in python3 (sourcepython.com) for playing a conquest like counter-strike as seen in the battlefield series. the goal is to have some great big maps with 6 or more conquest points where two teams of 16 players can conquer them.

## installation
just copy the "conquest" folder into the plugin directory of sourcepython and change the "mysql.py" to your actual mysql database. import the sql schemata "database.sql" and load my default test map "cs_office". just add one or more bots to your game (to actually start the game) and have fun testing.

### server config file
you should set some csgo server variables at least and make sure they don't get overwritten since we definately need them ;)
```
mp_ignore_round_win_conditions 1
mp_freezetime "0"
mp_afterroundmoney "0"
mp_timelimit "0"
mp_buytime "0"
mp_win_panel_display_time "7"
mp_free_armor "0"
sv_tags "conquest:go"
```

## start gameserver
it's useful to use classic casual as gamemode because otherwise you couldn't join a running game. start the server with the following command:
```
./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 0 +mapgroup mg_bomb +map de_cbble
```
## credits
- http://forums.sourcepython.com/ - all users and project leaders that helped me :)
- http://battlefront-cantina.de/ - Jack who helped me testing and provided me a list of all weapons for every class and many more!
- n0rt3-X - helped me testing :)
- Taskiii - helped me testing and provided the idea, too :)
- Skin: CSGO Rayman (http://gamebanana.com/skins/143904) Made by Voikanaa (thanks!)
