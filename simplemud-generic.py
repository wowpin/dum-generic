#!/usr/bin/python
# -*- coding: utf-8 -*-

from cmsg import cmsg

from functions import getFreeKey
from functions import log

import time

# import the database library
import pymysql

# import the MUD server class
from mudserver import MudServer

# import random generator library
from random import randint

# import the deepcopy library
from copy import deepcopy

# import config parser
import configparser

log("", "Server Boot")

log("Loading configuration file", "info")

# load the configuration file
Config = configparser.ConfigParser()
Config.read('config.ini')

# example of config file usage
# print(str(Config.get('Database', 'Hostname')))

# Load rooms
rooms = {
    '$rid=0$': {'description': 'You are in your private quarter aboard the Mariner spacecraft. Your room is dark, the only source of light being a wall screen displaying current time of day on Earth. You can hear a distant hum of ventilation equipment and a characteristic buzz of FTL engines, currently pushing you through a vast, unknown expand of space.',
                'exits': {'door': '$rid=1$', 'bathroom': '$rid=4$'},
                'name': 'Private Quarter'},
    '$rid=1$': {'description': 'You are standing in a wide corridor, which circles around the second level of the craft. Private quarters of other crew members are located on this level. A broken ceiling light flickers every few seconds. The air pumped through the vents is chilly and refreshing.',
                'exits': {'quarter door': '$rid=0$',
                'north': '$rid=2$', 'south': '$rid=3$'},
                'name': 'Corridor'},
    '$rid=2$': {'description': 'You are in a corridor. It ends here abruptly with a dead end.',
                'exits': {'south': '$rid=1$'},
                'name': 'Corridor'},
    '$rid=3$': {'description': "You are standing in the middle of a wide corridor. It's impossible to venture further south, a pile of rubble is blocking the way.",
                'exits': {'north': '$rid=1$'},
                'name': 'Corridor'},
    '$rid=4$': {'description': 'You are standing in a tiny bathroom, which is part of a private quarter aboard Mariner. Only bare essentials here, certainly nothing luxurious.',
                'exits': {'door': '$rid=0$'},
                'name': 'Small Bathroom'},
    '$rid=666$': {'description': 'Void. This is how you would describe your surroundings. You realise you cannot see your physical body and somehow it feels like you are not ACTUALLY there in a physical sense. It`s unbelievably bright here. You can see a slightly darker patch in a distance. It almost looks like an open rift, a tear in whatever fabric the environment is made of.',
                'exits': {'rift': '$rid=0$'},
                'name': 'Void'},
    }

log("Rooms loaded: " + str(len(rooms)), "info")

# Load NPCs
npcs = {}

# Declare NPCs master (template) tuple
npcsTemplate = {}

# Declare env tuple
env = {}

# Declare fights tuple
fights = {}

# Declare corpses tuple
corpses = {}

# Declare items tuple
itemsDB = {}

# Declare itemsInWorld tuple
itemsInWorld = {}

# Declare number of seconds to elapse between State Saves
# A State Save takes values held in memory and updates the database
# at set intervals to achieve player state persistence
stateSaveInterval = int(Config.get('World', 'StateSaveInterval'))
log("State Save interval: " + str(stateSaveInterval) + " seconds", "info")

# Set last state save to 'now' on server boot
lastStateSave = int(time.time())

# Database connection details
DBhost = Config.get('Database', 'Hostname')
DBport = int(Config.get('Database', 'Port'))
DBuser = Config.get('Database', 'User')
DBpasswd = Config.get('Database', 'Pass')
DBdatabase = Config.get('Database', 'DB')

log("Connecting to database", "info")
cnxn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, passwd=DBpasswd, db=DBdatabase)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM tbl_NPC")
dbResponse = cursor.fetchall()

for npc in dbResponse:
    npcs[npc[0]] = {
    'name': npc[1],
    'room': npc[2],
    'lvl': npc[3],
    'exp': npc[4],
    'str': npc[5],
    'per': npc[6],
    'endu': npc[7],
    'cha': npc[8],
    'inte': npc[9],
    'agi': npc[10],
    'luc': npc[11],
    'cred': npc[12],
    'inv': npc[13],
    'isAttackable': npc[14],
    'isStealable': npc[15],
    'isKillable': npc[16],
    'isAggressive': npc[17],
    'vocabulary': npc[18].split('|'),
    'talkDelay': npc[19],
    'lookDescription': npc[20],
    'timeTalked': int(time.time()),
    'clo_head': npc[21],
    'clo_larm': npc[22],
    'clo_rarm': npc[23],
    'clo_lhand': npc[24],
    'clo_rhand': npc[25],
    'clo_chest': npc[26],
    'clo_lleg': npc[27],
    'clo_rleg': npc[28],
    'clo_feet': npc[29],
    'imp_head': npc[30],
    'imp_larm': npc[31],
    'imp_rarm': npc[32],
    'imp_lhand': npc[33],
    'imp_rhand': npc[34],
    'imp_chest': npc[35],
    'imp_lleg': npc[36],
    'imp_rleg': npc[37],
    'imp_feet': npc[38],
    'hp': npc[39],
    'charge': npc[40],
    'isInCombat': 0,
    'lastCombatAction': int(time.time()),
    'lastRoom': None,
    'corpseTTL': 10,
    'respawn': npc[42],
    'whenDied': None
    }

log("NPCs loaded: " + str(len(npcs)), "info")
	
# Deepcopy npcs fetched from a database into a master template
npcsTemplate = deepcopy(npcs)

# List NPC dictionary for debigging purposes
# for x in npcs:
	# print (x)
	# for y in npcs[x]:
		# print (y,':',npcs[x][y])

# Fetch tbl_ENV and populate env[]
cursor.execute("SELECT * FROM tbl_ENV")
dbResponse = cursor.fetchall()

for en in dbResponse:
	env[en[0]] = {
	'name': en[1],
	'room': en[2],
	'vocabulary': en[3].split('|'),
	'talkDelay': en[4],
	'timeTalked': int(time.time()),
        'lastSaid': 0,
	}

log("Environment Actors loaded: " + str(len(env)), "info")
	# List ENV dictionary for debigging purposes
	# for x in env:
		# print (x)
		# for y in env[x]:
			# print (y,':',env[x][y])

# Fetch tbl_Items and populate itemsDB[]
cursor.execute("SELECT * FROM tbl_Items")
dbResponse = cursor.fetchall()

for item in dbResponse:
    itemsDB[item[0]] = {
        'name': item[1],
        'long_description': item[2],
        'short_description': item[3],
        'clo_head': item[4],
        'clo_larm': item[5],
        'clo_rarm': item[6],
        'clo_lhand': item[7],
        'clo_rhand': item[8],
        'clo_chest': item[9],
        'clo_lleg': item[10],
        'clo_rleg': item[11],
        'clo_feet': item[12],
        'imp_head': item[13],
        'imp_larm': item[14],
        'imp_rarm': item[15],
        'imp_lhand': item[16],
        'imp_rhand': item[17],
        'imp_chest': item[18],
        'imp_lleg': item[19],
        'imp_rleg': item[20],
        'imp_feet': item[21],
        'mod_str': item[22],
        'mod_per': item[23],
        'mod_endu': item[24],
        'mod_cha': item[25],
        'mod_inte': item[26],
        'mod_agi': item[27],
        'mod_luc': item[28],
        'weight': item[29],
        'article': item[30],
    }

log("Items loaded: " + str(len(itemsDB)), "info")
# List items DB for debugging purposes
# for x in itemsDB:
	# print (x)
	# for y in itemsDB[x]:
		# print(y,':',itemsDB[x][y])

# Put some items in the world for testing and debugging
itemsInWorld[getFreeKey(itemsInWorld)] = { 'id': 200001, 'room': '$rid=1$', 'whenDropped': 1533133523, 'lifespan': 90000000, 'owner': 1}
itemsInWorld[getFreeKey(itemsInWorld)] = { 'id': 200002, 'room': '$rid=1$', 'whenDropped': 1533133523, 'lifespan': 90002000, 'owner': 2}
itemsInWorld[getFreeKey(itemsInWorld)] = { 'id': 200001, 'room': '$rid=1$', 'whenDropped': 1533433523, 'lifespan': 90003000, 'owner': 1}

# List items in world for debugging purposes
# for x in itemsInWorld:
	# print (x)
	# for y in itemsInWorld[x]:
		# print(y,':',itemsInWorld[x][y])
		
# Close a database connection, all data has been fetched to memory
log("Closing database connection", "info")
cursor.close()
cnxn.close()

# Connect to the database
# cnxn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, passwd=DBpasswd, db=DBdatabase)

# stores the players in the game
players = {}

# start the server
mud = MudServer()

# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.1)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # Check if State Save is due and execute it if required
    now = int(time.time())
    if int(now >= lastStateSave + stateSaveInterval):
        # print("[info] Saving player state")
		
		# State Save logic Start
        cnxn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, passwd=DBpasswd, db=DBdatabase)
        cursor = cnxn.cursor()
        for (pid, pl) in list(players.items()):
            if players[pid]['authenticated'] is not None:
                # print('Saving' + players[pid]['name'])
                cursor.execute("UPDATE tbl_Players SET room = %s WHERE name = %s", [players[pid]["room"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET lvl = %s WHERE name = %s", [players[pid]["lvl"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET exp = %s WHERE name = %s", [players[pid]["exp"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET str = %s WHERE name = %s", [players[pid]["str"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET per = %s WHERE name = %s", [players[pid]["per"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET endu = %s WHERE name = %s", [players[pid]["endu"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET cha = %s WHERE name = %s", [players[pid]["cha"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET inte = %s WHERE name = %s", [players[pid]["int"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET agi = %s WHERE name = %s", [players[pid]["agi"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET luc = %s WHERE name = %s", [players[pid]["luc"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET cred = %s WHERE name = %s", [players[pid]["cred"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET inv = %s WHERE name = %s", [str(",".join(players[pid]["inv"])), players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_head = %s WHERE name = %s", [players[pid]["clo_head"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_larm = %s WHERE name = %s", [players[pid]["clo_larm"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_rarm = %s WHERE name = %s", [players[pid]["clo_rarm"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_lhand = %s WHERE name = %s", [players[pid]["clo_lhand"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_rhand = %s WHERE name = %s", [players[pid]["clo_rhand"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_chest = %s WHERE name = %s", [players[pid]["clo_chest"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_lleg = %s WHERE name = %s", [players[pid]["clo_lleg"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_rleg = %s WHERE name = %s", [players[pid]["clo_rleg"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET clo_feet = %s WHERE name = %s", [players[pid]["clo_feet"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_head = %s WHERE name = %s", [players[pid]["imp_head"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_larm = %s WHERE name = %s", [players[pid]["imp_larm"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_rarm = %s WHERE name = %s", [players[pid]["imp_rarm"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_lhand = %s WHERE name = %s", [players[pid]["imp_lhand"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_rhand = %s WHERE name = %s", [players[pid]["imp_rhand"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_chest = %s WHERE name = %s", [players[pid]["imp_chest"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_lleg = %s WHERE name = %s", [players[pid]["imp_lleg"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_rleg = %s WHERE name = %s", [players[pid]["imp_rleg"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET imp_feet = %s WHERE name = %s", [players[pid]["imp_feet"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET hp = %s WHERE name = %s", [players[pid]["hp"], players[pid]["name"]])
                cnxn.commit()
                cursor.execute("UPDATE tbl_Players SET charge = %s WHERE name = %s", [players[pid]["charge"], players[pid]["name"]])
                cnxn.commit()
        cnxn.close()
        # State Save logic End
        lastStateSave = now

    # Handle Player Deaths
    for (pid, pl) in list(players.items()):
        if players[pid]['authenticated'] == True:
            if players[pid]['hp'] <= 0:
                # Create player's corpse in the room
                corpses[len(corpses)] = { 'room': players[pid]['room'], 'name': str(players[pid]['name'] + '`s corpse'), 'inv': players[pid]['inv'], 'died': int(time.time()), 'TTL': players[pid]['corpseTTL'], 'owner': 1 }
                # Clear player's inventory, it stays on the corpse
                # This is bugged, causing errors when picking up things after death
                # players[pid]['inv'] = ''
                players[pid]['isInCombat'] = 0
                players[pid]['lastRoom'] = players[pid]['room']
                players[pid]['room'] = '$rid=666$'
                fightsCopy = deepcopy(fights)
                for (fight, pl) in fightsCopy.items():
                    if fightsCopy[fight]['s1id'] == pid or fightsCopy[fight]['s2id'] == pid:
                        del fights[fight]
                for (pid2, pl) in list(players.items()):
                    if players[pid2]['authenticated'] is not None \
                        and players[pid2]['room'] == players[pid]['lastRoom'] \
                        and players[pid2]['name'] != players[pid]['name']:
                        mud.send_message(pid2, '<u><f32>{}<r> <f124>has been killed.'.format(players[pid]['name']))
                players[pid]['lastRoom'] = None
                mud.send_message(pid, '<b88><f158>Oh dear! You have died!')
                players[pid]['hp'] = 4

    # Handle Fights
    for (fid, pl) in list(fights.items()):
        # PC -> PC
        if fights[fid]['s1type'] == 'pc' and fights[fid]['s2type'] == 'pc':
            if players[fights[fid]['s1id']]['room'] == players[fights[fid]['s2id']]['room']:
                if int(time.time()) >= players[fights[fid]['s1id']]['lastCombatAction'] + 10 - players[fights[fid]['s1id']]['agi']:
                    if players[fights[fid]['s2id']]['isAttackable'] == 1:
                        players[fights[fid]['s1id']]['isInCombat'] = 1
                        players[fights[fid]['s2id']]['isInCombat'] = 1
                        # Do damage to the PC here
                        if randint(0, 1) == 1:
                            modifier = randint(0, 10)
                            if players[fights[fid]['s1id']]['hp'] > 0:
                                players[fights[fid]['s2id']]['hp'] = players[fights[fid]['s2id']]['hp'] - (players[fights[fid]['s1id']]['str'] + modifier)
                                players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
                                mud.send_message(fights[fid]['s1id'], 'You manage to hit <f32><u>' + players[fights[fid]['s2id']]['name'] + '<r> for <f0><b2>' + str(players[fights[fid]['s1id']]['str'] + modifier) + '<r> points of damage.')
                                mud.send_message(fights[fid]['s2id'], '<f32>' + players[fights[fid]['s1id']]['name'] + '<r> has managed to hit you for <f15><b88>' + str(players[fights[fid]['s1id']]['str'] + modifier) + '<r> points of damage.')
                                # print('----------')
                                # print(players[fights[fid]['s1id']]['name'] + ': ' + str(players[fights[fid]['s1id']]['hp']))
                                # print(players[fights[fid]['s2id']]['name'] + ': ' + str(players[fights[fid]['s2id']]['hp']))
                        else:
                            players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
                            mud.send_message(fights[fid]['s1id'], 'You miss trying to hit <f32><u>' + players[fights[fid]['s2id']]['name'] + '')
                            mud.send_message(fights[fid]['s2id'], '<f32><u>' + players[fights[fid]['s1id']]['name'] + '<r> missed while trying to hit you!')
                    else:
                        mud.send_message(fights[fid]['s1id'], '<f225>Suddnely you stop. It wouldn`t be a good idea to attack <f32>' + players[fights[fid]['s2id']]['name'] + ' at this time.')
                        fightsCopy = deepcopy(fights)
                        for (fight, pl) in fightsCopy.items():
                            if fightsCopy[fight]['s1id'] == fights[fid]['s1id'] and fightsCopy[fight]['s2id'] == fights[fid]['s2id']:
                                del fights[fight]
        # PC -> NPC
        elif fights[fid]['s1type'] == 'pc' and fights[fid]['s2type'] == 'npc':
            if players[fights[fid]['s1id']]['room'] == npcs[fights[fid]['s2id']]['room']:
                if int(time.time()) >= players[fights[fid]['s1id']]['lastCombatAction'] + 10 - players[fights[fid]['s1id']]['agi']:
                    if npcs[fights[fid]['s2id']]['isAttackable'] == 1:
                        players[fights[fid]['s1id']]['isInCombat'] = 1
                        npcs[fights[fid]['s2id']]['isInCombat'] = 1
                        # Do damage to the NPC here
                        if randint(0, 1) == 1:
                            modifier = randint(0, 10)
                            if players[fights[fid]['s1id']]['hp'] > 0:
                                npcs[fights[fid]['s2id']]['hp'] = npcs[fights[fid]['s2id']]['hp'] - (players[fights[fid]['s1id']]['str'] + modifier)
                                players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
                                mud.send_message(fights[fid]['s1id'], 'You manage to hit <f21><u>' + npcs[fights[fid]['s2id']]['name'] + '<r> for <b2><f0>' + str(players[fights[fid]['s1id']]['str'] + modifier)  + '<r> points of damage')
                                # print(npcs[fights[fid]['s2id']]['hp'])
                        else:
                            players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
                            mud.send_message(fights[fid]['s1id'], 'You miss <u><f21>' + npcs[fights[fid]['s2id']]['name'] + '<r> completely!')
                    else:
                        mud.send_message(fights[fid]['s1id'], '<f225>Suddenly you stop. It wouldn`t be a good idea to attack <u><f21>' + npcs[fights[fid]['s2id']]['name'] + '<r> at this time.')
                        fightsCopy = deepcopy(fights)
                        for (fight, pl) in fightsCopy.items():
                            if fightsCopy[fight]['s1id'] == fights[fid]['s1id'] and fightsCopy[fight]['s2id'] == fights[fid]['s2id']:
                                del fights[fight]
        # NPC -> PC
        elif fights[fid]['s1type'] == 'npc' and fights[fid]['s2type'] == 'pc':
            if npcs[fights[fid]['s1id']]['room'] == players[fights[fid]['s2id']]['room']:
                if int(time.time()) >= npcs[fights[fid]['s1id']]['lastCombatAction'] + 10 - npcs[fights[fid]['s1id']]['agi']:
                    npcs[fights[fid]['s1id']]['isInCombat'] = 1
                    players[fights[fid]['s2id']]['isInCombat'] = 1
                    # Do the damage to PC here
                    if randint(0, 1) == 1:
                        modifier = randint(0, 10)
                        if npcs[fights[fid]['s1id']]['hp'] > 0:
                            players[fights[fid]['s2id']]['hp'] = players[fights[fid]['s2id']]['hp'] - (npcs[fights[fid]['s1id']]['str'] + modifier)
                            npcs[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
                            mud.send_message(fights[fid]['s2id'], '<f21><u>' + npcs[fights[fid]['s1id']]['name'] + '<r> has managed to hit you for <f15><b88>' + str(npcs[fights[fid]['s1id']]['str'] + modifier) + '<r> points of damage.')
                    else:
                        npcs[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
                        mud.send_message(fights[fid]['s2id'], '<f21><u>' + npcs[fights[fid]['s1id']]['name'] + '<r> has missed you completely!')
        elif fights[fid]['s1type'] == 'npc' and fights[fid]['s2type'] == 'npc':
            test = 1
            # NPC -> NPC
            

    # Iterate through NPCs, check if its time to talk, then check if anyone is attacking it
    for (nid, pl) in list(npcs.items()):
        # Check if any player is in the same room, then send a random message to them
        now = int(time.time())
        if now > npcs[nid]['timeTalked'] + npcs[nid]['talkDelay']:
            rnd = randint(0, len(npcs[nid]['vocabulary']) - 1)
            for (pid, pl) in list(players.items()):
                if npcs[nid]['room'] == players[pid]['room']:
                    if len(npcs[nid]['vocabulary']) > 1:
                        #mud.send_message(pid, npcs[nid]['vocabulary'][rnd])
                        msg = '<f21><u>' + npcs[nid]['name'] + '<r> says: <f86>' + npcs[nid]['vocabulary'][rnd]
                        mud.send_message(pid, msg)
                    else:
                        #mud.send_message(pid, npcs[nid]['vocabulary'][0])
                        msg = '<f21><u>' + npcs[nid]['name'] + '<r> says: <f86>' + npcs[nid]['vocabulary'][0]
                        mud.send_message(pid, msg)
            npcs[nid]['timeTalked'] =  now
        # Iterate through fights and see if anyone is attacking an NPC - if so, attack him too if not in combat (TODO: and isAggressive = true)
        for (fid, pl) in list(fights.items()):
            if fights[fid]['s2id'] == nid and npcs[fights[fid]['s2id']]['isInCombat'] == 1 and fights[fid]['s1type'] == 'pc' and fights[fid]['retaliated'] == 0:
                # print('player is attacking npc')
                # BETA: set las combat action to now when attacking a player
                npcs[fights[fid]['s2id']]['lastCombatAction'] = int(time.time())
                fights[fid]['retaliated'] = 1
                npcs[fights[fid]['s2id']]['isInCombat'] = 1
                fights[len(fights)] = { 's1': npcs[fights[fid]['s2id']]['name'], 's2': players[fights[fid]['s1id']]['name'], 's1id': nid, 's2id': fights[fid]['s1id'], 's1type': 'npc', 's2type': 'pc', 'retaliated': 1 }
            elif fights[fid]['s2id'] == nid and npcs[fights[fid]['s2id']]['isInCombat'] == 1 and fights[fid]['s1type'] == 'npc' and fights[fid]['retaliated'] == 0:
                # print('npc is attacking npc')
                # BETA: set las combat action to now when attacking a player
                npcs[fights[fid]['s2id']]['lastCombatAction'] = int(time.time())
                fights[fid]['retaliated'] = 1
                npcs[fights[fid]['s2id']]['isInCombat'] = 1
                fights[len(fights)] = { 's1': npcs[fights[fid]['s2id']]['name'], 's2': players[fights[fid]['s1id']]['name'], 's1id': nid, 's2id': fights[fid]['s1id'], 's1type': 'npc', 's2type': 'npc', 'retaliated': 1 }
        # Check if NPC is still alive, if not, remove from room and create a corpse, set isInCombat to 0, set whenDied to now and remove any fights NPC was involved in
        if npcs[nid]['hp'] <= 0:
            npcs[nid]['isInCombat'] = 0
            npcs[nid]['lastRoom'] = npcs[nid]['room']
            npcs[nid]['whenDied'] = int(time.time())
            fightsCopy = deepcopy(fights)
            for (fight, pl) in fightsCopy.items():
                if fightsCopy[fight]['s1id'] == nid or fightsCopy[fight]['s2id'] == nid:
                    del fights[fight]
            corpses[len(corpses)] = { 'room': npcs[nid]['room'], 'name': str(npcs[nid]['name'] + '`s corpse'), 'inv': npcs[nid]['inv'], 'died': int(time.time()), 'TTL': npcs[nid]['corpseTTL'], 'owner': 1 }
            for (pid, pl) in list(players.items()):
                if players[pid]['authenticated'] is not None:
                    if players[pid]['authenticated'] is not None and players[pid]['room'] == npcs[nid]['room']:
                        mud.send_message(pid, "<f32><u>{}<r> <f88>has been killed.".format(npcs[nid]['name']))
            npcs[nid]['room'] = None
            npcs[nid]['hp'] = npcsTemplate[nid]['hp']

    # Iterate through ENV elements and see if it's time to send a message to players in the same room as the ENV elements
    for (eid, pl) in list(env.items()):
        now = int(time.time())
        if now > env[eid]['timeTalked'] + env[eid]['talkDelay']:
            rnd = randint(0, len(env[eid]['vocabulary']) - 1)
            for (pid, pl) in list(players.items()):
                if env[eid]['room'] == players[pid]['room']:
                    if len(env[eid]['vocabulary']) > 1:
                        msg = '<f58>[' + env[eid]['name'] + ']: <f236>' + env[eid]['vocabulary'][rnd]
                        mud.send_message(pid, msg)
                    else:
                        msg = '<f58>[' + env[eid]['name'] + ']: <f236>' + env[eid]['vocabulary'][0]
                        mud.send_message(pid, msg)
            env[eid]['timeTalked'] =  now

    # Iterate through corpses and remove ones older than their TTL
    corpsesCopy = deepcopy(corpses)
    for (c, pl) in corpsesCopy.items():
        if int(time.time()) >= corpsesCopy[c]['died'] + corpsesCopy[c]['TTL']:
            # print("deleting " + corpses[corpse]['name'])
            del corpses[c]

    # Handle NPC respawns
    for (nid, pl) in list(npcs.items()):
        if npcs[nid]['whenDied'] is not None and int(time.time()) >= npcs[nid]['whenDied'] + npcs[nid]['respawn']:
            npcs[nid]['whenDied'] = None
            npcs[nid]['room'] = npcsTemplate[nid]['room']
            # print("respawning " + npcs[nid]['name'])

    # go through any newly connected players
    for id in mud.get_new_players():
        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. We set their room to
        # None initially until they have entered a name
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = {
            'name': None,
            'room': None,
            'lvl': None,
            'exp': None,
            'str': None,
            'per': None,
            'endu': None,
            'cha': None,
            'int': None,
            'agi': None,
            'luc': None,
            'cred': None,
            'inv': None,
            'authenticated': None,
            'clo_head': None,
            'clo_larm': None,
            'clo_rarm': None,
            'clo_lhand': None,
            'clo_rhand': None,
            'clo_chest': None,
            'clo_lleg': None,
            'clo_rleg': None,
            'clo_feet': None,
            'imp_head': None,
            'imp_larm': None,
            'imp_rarm': None,
            'imp_lhand': None,
            'imp_rhand': None,
            'imp_chest': None,
            'imp_lleg': None,
            'imp_rleg': None,
            'imp_feet': None,
            'hp': None,
            'charge': None,
            'isInCombat': None,
            'lastCombatAction': None,
            'isAttackable': None,
            'lastRoom': None,
            'corpseTTL': None,
            }

        # send the new player a prompt for their name
        # mud.send_message(id, 'Connected to server!')
        mud.send_message(id, "<f250><b25> ______            _______ ")
        mud.send_message(id, "<f250><b25>(  __  \ |\     /|(       )")
        mud.send_message(id, "<f250><b25>| (  \  )| )   ( || () () |")
        mud.send_message(id, "<f250><b25>| |   ) || |   | || || || |")
        mud.send_message(id, "<f250><b25>| |   | || |   | || |(_)| |")
        mud.send_message(id, "<f250><b25>| |   ) || |   | || |   | |")
        mud.send_message(id, "<f250><b25>| (__/  )| (___) || )   ( |")
        mud.send_message(id, "<f250><b25>(______/ (_______)|/     \|")
        mud.send_message(id, " ")
        mud.send_message(id, "<f250><b25> a modern MU* engine       ")
        mud.send_message(id, "<f15><b25>    dumengine.wikidot.com  ")
        mud.send_message(id, " ")
        mud.send_message(id, "<f250><b25> Development Server 1       ")
        mud.send_message(id, " ")
        mud.send_message(id, '<f15>What is your username?')
        log("Client ID: " + str(id) + " has connected", "info")

    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue
		
        log("Client ID:" + str(id) + " has disconnected (" + str(players[id]['name']) + ")", "info")
		
        # go through all the players in the game
        for (pid, pl) in list(players.items()):
            # send each player a message to tell them about the diconnected
            # player if they are in the same room
            if players[pid]['authenticated'] is not None:
                if players[pid]['authenticated'] is not None \
                    and players[pid]['room'] == players[id]['room'] \
                    and players[pid]['name'] != players[id]['name']:
                    mud.send_message(pid,
                            "<f32><u>{}<r>'s body has vanished.".format(players[id]['name']))

        # Code here to save player to the database after he's disconnected and before removing him from players dictionary
        if players[id]['authenticated'] is not None:
            cnxn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, passwd=DBpasswd, db=DBdatabase)
            cursor = cnxn.cursor()
            log("Player disconnected, saving state", "info")
            cursor.execute("UPDATE tbl_Players SET room = %s WHERE name = %s", [players[id]["room"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET lvl = %s WHERE name = %s", [players[id]["lvl"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET exp = %s WHERE name = %s", [players[id]["exp"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET str = %s WHERE name = %s", [players[id]["str"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET per = %s WHERE name = %s", [players[id]["per"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET endu = %s WHERE name = %s", [players[id]["endu"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET cha = %s WHERE name = %s", [players[id]["cha"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET inte = %s WHERE name = %s", [players[id]["int"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET agi = %s WHERE name = %s", [players[id]["agi"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET luc = %s WHERE name = %s", [players[id]["luc"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET cred = %s WHERE name = %s", [players[id]["cred"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET inv = %s WHERE name = %s", [str(",".join(players[id]["inv"])), players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_head = %s WHERE name = %s", [players[id]["clo_head"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_larm = %s WHERE name = %s", [players[id]["clo_larm"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_rarm = %s WHERE name = %s", [players[id]["clo_rarm"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_lhand = %s WHERE name = %s", [players[id]["clo_lhand"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_rhand = %s WHERE name = %s", [players[id]["clo_rhand"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_chest = %s WHERE name = %s", [players[id]["clo_chest"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_lleg = %s WHERE name = %s", [players[id]["clo_lleg"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_rleg = %s WHERE name = %s", [players[id]["clo_rleg"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET clo_feet = %s WHERE name = %s", [players[id]["clo_feet"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_head = %s WHERE name = %s", [players[id]["imp_head"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_larm = %s WHERE name = %s", [players[id]["imp_larm"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_rarm = %s WHERE name = %s", [players[id]["imp_rarm"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_lhand = %s WHERE name = %s", [players[id]["imp_lhand"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_rhand = %s WHERE name = %s", [players[id]["imp_rhand"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_chest = %s WHERE name = %s", [players[id]["imp_chest"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_lleg = %s WHERE name = %s", [players[id]["imp_lleg"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_rleg = %s WHERE name = %s", [players[id]["imp_rleg"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET imp_feet = %s WHERE name = %s", [players[id]["imp_feet"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET hp = %s WHERE name = %s", [players[id]["hp"], players[id]["name"]])
            cnxn.commit()
            cursor.execute("UPDATE tbl_Players SET charge = %s WHERE name = %s", [players[id]["charge"], players[id]["name"]])
            cnxn.commit()
            cnxn.close()
        
        # TODO: IDEA - Some sort of a timer to have the character remain in the game for some time after disconnection?

        # Create a deep copy of fights, iterate through it and remove fights disconnected player was taking part in
        fightsCopy = deepcopy(fights)
        for (fight, pl) in fightsCopy.items():
            if fightsCopy[fight]['s1'] == players[id]['name'] or fightsCopy[fight]['s2'] == players[id]['name']:
                del fights[fight]


        # remove the player's entry in the player dictionary
        del players[id]

    # go through any new commands sent from players
    for (id, command, params) in mud.get_commands():
        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # if the player hasn't given their name yet, use this first command as
        # their name and move them to the starting room.
        if players[id]['name'] is None:
            cnxn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, passwd=DBpasswd, db=DBdatabase)
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM tbl_Players WHERE name = '" + command + "'")
            dbResponse = cursor.fetchone()

            if dbResponse != None:
                players[id]['name'] = dbResponse[0]

                # Closing DB cursor, all required data has been extracted from the database
                cursor.close()
                cnxn.close()

                log("Client ID: " + str(id) + " has requested existing user (" + command + ")", "info")
                mud.send_message(id, 'Hi <u><f32>' + command + '<r>!')
                mud.send_message(id, '<f15>What is your password?')
            else:
                mud.send_message(id, '<f202>User <f32>' + command + '<r> was not found!')
                log("Client ID: " + str(id) + " has requested non existent user (" + command + ")", "info")
        elif players[id]['name'] is not None \
            and players[id]['authenticated'] is None:
            cnxn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, passwd=DBpasswd, db=DBdatabase)
            cursor = cnxn.cursor()
            cursor.execute("SELECT pwd FROM tbl_Players WHERE name = '" + players[id]['name'] + "'")
            dbPass = cursor.fetchone()
            cursor.close()
            cnxn.close()

            if dbPass[0] == command:
                players[id]['authenticated'] = True
                players[id]['room'] = dbResponse[1]
                players[id]['lvl'] = dbResponse[2]
                players[id]['exp'] = dbResponse[3]
                players[id]['str'] = dbResponse[4]
                players[id]['per'] = dbResponse[5]
                players[id]['endu'] = dbResponse[6]
                players[id]['cha'] = dbResponse[7]
                players[id]['int'] = dbResponse[8]
                players[id]['agi'] = dbResponse[9]
                players[id]['luc'] = dbResponse[10]
                players[id]['cred'] = dbResponse[11]
                players[id]['inv'] = dbResponse[12].split(',')
                # Example: item_list = [e for e in item_list if e not in ('item', 5)]
                players[id]['inv'] = [e for e in players[id]['inv'] if e not in ('', ' ')]
                players[id]['clo_head'] = dbResponse[14]
                players[id]['clo_larm'] = dbResponse[15]
                players[id]['clo_rarm'] = dbResponse[16]
                players[id]['clo_lhand'] = dbResponse[17]
                players[id]['clo_rhand'] = dbResponse[18]
                players[id]['clo_chest'] = dbResponse[19]
                players[id]['clo_lleg'] = dbResponse[20]
                players[id]['clo_rleg'] = dbResponse[21]
                players[id]['clo_feet'] = dbResponse[22]
                players[id]['imp_head'] = dbResponse[23]
                players[id]['imp_larm'] = dbResponse[24]
                players[id]['imp_rarm'] = dbResponse[25]
                players[id]['imp_lhand'] = dbResponse[26]
                players[id]['imp_rhand'] = dbResponse[27]
                players[id]['imp_chest'] = dbResponse[28]
                players[id]['imp_lleg'] = dbResponse[29]
                players[id]['imp_rleg'] = dbResponse[30]
                players[id]['imp_feet'] = dbResponse[31]
                players[id]['hp'] = dbResponse[32]
                players[id]['charge'] = dbResponse[33]
                players[id]['isInCombat'] = 0
                players[id]['lastCombatAction'] = int(time.time())
                players[id]['isAttackable'] = 1
                players[id]['corpseTTL'] = 60
				
                log("Client ID: " + str(id) + " has successfully authenticated user " + players[id]['name'], "info")
                
                # Debug - print data extracted from DB onto console
                #print('Loaded player ' + players[id]['name'] + 'room: ' \
                #    + players[id]['room'] + 'lvl: ' \
                #    + str(players[id]['lvl']) + 'exp: ' \
                #    + str(players[id]['exp']) + 'str: ' \
                #    + str(players[id]['str']) + 'per: ' \
                #    + str(players[id]['per']) + 'endu: ' \
                #    + str(players[id]['endu']) + 'cha: ' \
                #    + str(players[id]['cha']) + 'int: ' \
                #    + str(players[id]['int']) + 'agi: ' \
                #    + str(players[id]['agi']) + 'luc: ' \
                #    + str(players[id]['luc']) + 'cred: ' \
                #    + str(players[id]['cred']))

                # go through all the players in the game
                for (pid, pl) in list(players.items()):
                     # send each player a message to tell them about the new player
                     # print("player pid: " + players[pid]["room"] + ", player id: " + players[id]["room"])
                    if players[pid]['authenticated'] is not None \
                        and players[pid]['room'] == players[id]['room'] \
                        and players[pid]['name'] != players[id]['name']:
                        mud.send_message(pid, '{} has materialised out of thin air nearby.'.format(players[id]['name']))

                # send the new player a welcome message
                mud.send_message(id, '<f15>Welcome to the game, {}. '.format(players[id]['name']))
                mud.send_message(id, '<f15>-------------------------------------------------')
                mud.send_message(id, "<f15>Type 'help' for a list of commands. Have fun!")

                # send the new player the description of their current room
                # print('about to send room description...')
                # print('Description: ' + rooms[players[id]['room']]['description'])
                # mud.send_message(id, rooms[players[id]['room']]['description'])
            else:
                mud.send_message(id, '<f202>Password incorrect!')
                log("Client ID: " + str(id) + " has failed authentication", "info")

        elif command.lower() == 'help':
        # 'help' command
            # send the player back the list of possible commands
            mud.send_message(id, 'Commands:')
            mud.send_message(id, '  say <message>    - Says something out loud, '  + "e.g. 'say Hello'")
            mud.send_message(id, '  look             - Examines the ' + "surroundings, e.g. 'look'")
            mud.send_message(id, '  go <exit>        - Moves through the exit ' + "specified, e.g. 'go outside'")
            mud.send_message(id, '  attack <target>  - attack target ' + "specified, e.g. 'attack cleaning bot'")
            mud.send_message(id, '  check inventory  - check the contents of ' + "your inventory")
            mud.send_message(id, '  take <item>      - pick up an item lying ' + "on the floor")
            mud.send_message(id, '  drop <item>      - drop an item from your inventory ' + "on the floor")
            mud.send_message(id, '  colortest        - showcase client`s ability to display ' + "colorful text")
			
        elif command.lower() == 'say':
        # 'say' command
            # go through every player in the game
            for (pid, pl) in list(players.items()):
                # if they're in the same room as the player
                if players[pid]['room'] == players[id]['room']:
                    # send them a message telling them what the player said
                    mud.send_message(pid, '<f32>{}<r> says: <f159>{}'.format(players[id]['name'], params))
        elif command.lower() == 'look':
        # 'look' command
            # store the player's current room
            rm = rooms[players[id]['room']]

            # send the player back the description of their current room
            mud.send_message(id, "<f42>" + rm['description'])

            playershere = []

            itemshere = []

            # go through every player in the game
            for (pid, pl) in list(players.items()):
                # if they're in the same room as the player
                if players[pid]['room'] == players[id]['room']:
                    # ... and they have a name to be shown
                    if players[pid]['name'] is not None and players[pid]['name'] is not players[id]['name']:
                        # add their name to the list
                        playershere.append(players[pid]['name'])

            ##### Show corpses in the room
            for (corpse, pl) in list(corpses.items()):
                if corpses[corpse]['room'] == players[id]['room']:
                    playershere.append(corpses[corpse]['name'])
                                       
            ##### Show NPCs in the room #####
            for (nid, pl) in list(npcs.items()):
                if npcs[nid]['room'] == players[id]['room']:
                    playershere.append(npcs[nid]['name'])

            ##### Show items in the room
            for (item, pl) in list(itemsInWorld.items()):
                if itemsInWorld[item]['room'] == players[id]['room']:
                    itemshere.append(itemsDB[itemsInWorld[item]['id']]['article'] + ' ' + itemsDB[itemsInWorld[item]['id']]['name'])
            
            # send player a message containing the list of players in the room
            if len(playershere) > 0:
                mud.send_message(id, '<f42>You see: <f77>{}'.format(', '.join(playershere)))

            # send player a message containing the list of exits from this room
            mud.send_message(id, '<f42>Exits are: <f94>{}'.format(', '.join(rm['exits'])))

            # send player a message containing the list of items in the room
            if len(itemshere) > 0:
                mud.send_message(id, '<f42>You notice: <f222>{}'.format(', '.join(itemshere)))

        elif command.lower() == 'attack':
            # attack command
        
            isAlreadyAttacking = False
            target = params #.lower()
            targetFound = False

            for (fight, pl) in fights.items():
                if fights[fight]['s1'] == players[id]['name']:
                    isAlreadyAttacking = True
                    currentTarget = fights[fight]['s2']

            if isAlreadyAttacking == False:
                if players[id]['name'].lower() != target.lower():
                    for (pid, pl) in players.items():
                        if players[pid]['name'].lower() == target.lower():
                            targetFound = True
                            victimId = pid
                            attackerId = id
                            if players[pid]['room'] == players[id]['room']:
                                fights[len(fights)] = { 's1': players[id]['name'], 's2': target, 's1id': attackerId, 's2id': victimId, 's1type': 'pc', 's2type': 'pc', 'retaliated': 0 }
                                mud.send_message(id, '<f214>Attacking <r><u><f32>' + target + '!')
                            else:
                                targetFound = False

                    # mud.send_message(id, 'You cannot see ' + target + ' anywhere nearby.|')
                    if(targetFound == False):
                        for (nid, pl) in list(npcs.items()):
                            if npcs[nid]['name'].lower() == target.lower():
                                victimId = nid
                                attackerId = id
                                # print('found target npc')
                                if npcs[nid]['room'] == players[id]['room'] and targetFound == False:
                                    targetFound = True
                                    # print('target found!')
                                    if players[id]['room'] == npcs[nid]['room']:
                                        fights[len(fights)] = { 's1': players[id]['name'], 's2': nid, 's1id': attackerId, 's2id': victimId, 's1type': 'pc', 's2type': 'npc', 'retaliated': 0 }
                                        mud.send_message(id, 'Attacking <u><f21>' + npcs[nid]['name'] + '<r>!')
                                    else:
                                        pass

                    if targetFound == False:
                        mud.send_message(id, 'You cannot see ' + target + ' anywhere nearby.')
                else:
                    mud.send_message(id, 'You attempt hitting yourself and realise this might not be the most productive way of using your time.')
            else:
                if type(currentTarget) is not int:
                    mud.send_message(id, 'You are already attacking ' + currentTarget)
                else:
                    mud.send_message(id, 'You are already attacking ' + npcs[currentTarget]['name'])
            # List fights for debugging purposes
            # for x in fights:
                # print (x)
                # for y in fights[x]:
                    # print (y,':',fights[x][y])

        elif command.lower() == 'go':
        # 'go' command
            # store the exit name
            ex = params.lower()

            # store the player's current room
            rm = rooms[players[id]['room']]

            # if the specified exit is found in the room's exits list
            if ex in rm['exits']:
                # go through all the players in the game
                for (pid, pl) in list(players.items()):
                    # if player is in the same room and isn't the player
                    # sending the command
                    if players[pid]['room'] == players[id]['room'] \
                        and pid != id:
                        # send them a message telling them that the player
                        # left the room
                        mud.send_message(pid,
                                '<f32>{}<r> left via exit {}'.format(players[id]['name'], ex))

                # update the player's current room to the one the exit leads to
                players[id]['room'] = rm['exits'][ex]
                rm = rooms[players[id]['room']]

                # go through all the players in the game
                for (pid, pl) in list(players.items()):
                    # if player is in the same (new) room and isn't the player
                    # sending the command
                    if players[pid]['room'] == players[id]['room'] \
                        and pid != id:
                        # send them a message telling them that the player
                        # entered the room
                        # mud.send_message(pid, '{} arrived via exit {}|'.format(players[id]['name'], ex))
                        mud.send_message(pid, '<f32>{}<r> has arrived.'.format(players[id]['name'], ex))

                # send the player a message telling them where they are now
                #mud.send_message(id, 'You arrive at {}'.format(players[id]['room']))
                mud.send_message(id, 'You arrive at <f106>{}'.format(rooms[players[id]['room']]['name']))
            else:
            # the specified exit wasn't found in the current room
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit <f226>'{}''".format(ex))

        elif command.lower() == 'check':
        # 'check' command
            if params.lower() == 'inventory' or params.lower() == 'inv':
                mud.send_message(id, 'You check your inventory.')
                if len(list(players[id]['inv'])) > 0:
                    mud.send_message(id, 'You are currently in possession of: ')
                    for i in list(players[id]['inv']):
                        mud.send_message(id, '<b234>' + itemsDB[int(i)]['name'])
                else:
                    mud.send_message(id, 'You haven`t got any items on you.')
            elif params.lower() == 'stats':
                mud.send_message(id, 'You check your character sheet.')
            else:
                mud.send_message(id, 'Check what?')

        elif command.lower() == 'drop':
        # 'drop' command
            itemInDB = False
            inventoryNotEmpty = False
            itemInInventory = False
            itemID = None
            itemName = None
            
            for (iid, pl) in list(itemsDB.items()):
                if itemsDB[iid]['name'].lower() == str(params).lower():
                    # ID of the item to be dropped
                    itemID = iid
                    itemName = itemsDB[iid]['name']
                    itemInDB = True
                    break
                else:
                    itemInDB = False
                    itemName = None
                    itemID = None

            # Check if inventory is not empty
            if len(list(players[id]['inv'])) > 0:
                inventoryNotEmpty = True
            else:
                inventoryNotEmpty = False

            # Check if item is in player's inventory
            for item in players[id]['inv']:
                if int(item) == itemID:
                    itemInInventory = True
                    break
                else:
                    itemInInventory = False
            
            if itemInDB and inventoryNotEmpty and itemInInventory:
                inventoryCopy = deepcopy(players[id]['inv'])
                for i in inventoryCopy:
                    if int(i) == itemID:
                        # Remove first matching item from inventory
                        players[id]['inv'].remove(i)
                        break

                # Create item on the floor in the same room as the player
                itemsInWorld[getFreeKey(itemsInWorld)] = { 'id': itemID, 'room': players[id]['room'], 'whenDropped': int(time.time()), 'lifespan': 900000000, 'owner': id }
                
                # Print itemsInWorld to console for debugging purposes
                # for x in itemsInWorld:
                    # print (x)
                    # for y in itemsInWorld[x]:
                            # print(y,':',itemsInWorld[x][y])
                            
                mud.send_message(id, 'You drop ' + itemsDB[int(i)]['article'] + ' ' + itemsDB[int(i)]['name'] + ' on the floor.')
                
            else:
                mud.send_message(id, 'You don`t have that!')


        elif command.lower() == 'take':
        # take command
            itemInDB = None
            itemID = None
            itemName = None
            # itemInRoom = None

            for (iid, pl) in list(itemsDB.items()):
                if itemsDB[iid]['name'].lower() == str(params).lower():
                    # ID of the item to be picked up
                    itemID = iid
                    itemName = itemsDB[iid]['name']
                    itemInDB = True
                    break
                else:
                    itemInDB = False
                    itemName = None
                    itemID = None

            itemsInWorldCopy = deepcopy(itemsInWorld)

            for (iid, pl) in list(itemsInWorldCopy.items()):
                if itemsInWorldCopy[iid]['room'] == players[id]['room']:
                    # print(str(itemsDB[itemsInWorld[iid]['id']]['name'].lower()))
                    # print(str(params).lower())
                    if itemsDB[itemsInWorld[iid]['id']]['name'].lower() == str(params).lower():
                        players[id]['inv'].append(str(itemID))
                        del itemsInWorld[iid]
                        # mud.send_message(id, 'You pick up and place ' + itemsDB[itemID]['article'] + ' ' + itemsDB[itemID]['name'] + ' in your inventory.')
                        itemPickedUp = True
                        break
                    else:
                        # mud.send_message(id, 'You cannot see ' + str(params) + ' anywhere.')
                        itemPickedUp = False
                else:
                    # mud.send_message(id, 'You cannot see ' + str(params) + ' anywhere.')
                    itemPickedUp = False
                    # break

            if itemPickedUp == True:
                mud.send_message(id, 'You pick up and place ' + itemsDB[itemID]['article'] + ' ' + itemsDB[itemID]['name'] + ' in your inventory.')
                itemPickedUp = False
            else:
                mud.send_message(id, 'You cannot see ' + str(params) + ' anywhere.')
                itemPickedUp = False

        else:
        # some other, unrecognised command
            # send back an 'unknown command' message
            mud.send_message(id, "Unknown command '{}'".format(command))

