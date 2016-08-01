# conquest-go
a battlefield series style conquest mod for counter-strike:global offensive

## introduction
conquest:go is an mod written in python3 (sourcepython.com) for playing a conquest like counter-strike as seen in the battlefield series. the goal is to have some great big maps with 6 or more conquest points where two teams of 16 players can conquer them.

## features
Here are some of the main features of the gamemode:

- completely configurable conquest flags
- skins for different kinds of players (e.G. V.I.P. or admin, ...)
- spawnprotection
- supports every map
- autodownload for skins or other stuff (like sounds, ...)
- create very own classes
- create own weapon list available for each class
- change, add or delete ranks (currently 60 ranks)

## installation
- install latest release of sourcepython (http://forums.sourcepython.com/)
- copy the "materials" and "models" folder to your csgo server directory into the existing folders (overwrite if neccessary)
- upload same files on your gameservers fastdownload (if any) and maybe it's a good idea to compress them to save bandwidth and disk space
- copy the "conquest" folder into the plugin directory of sourcepython and change connection details in "mysql.py"
- import the schema "database.sql" to your database server
- create a server.cfg file in the "cfg" directory of your csgo server and add the config entries below to it
- start the server (see command below)
- add bots for testing or just start playing with your friends

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
- Skin: CSGO Shadow Company (http://gamebanana.com/skins/144154) Made by Voikanaa, too (thanks again!)
- Skin: CSGO TF2 Heavy (http://gamebanana.com/skins/142003) Made by Kuristaja (thanks!)
- Skin: CSGO Nanosuit (http://gamebanana.com/skins/136977) Made by Kuristaja (thanks again!)
