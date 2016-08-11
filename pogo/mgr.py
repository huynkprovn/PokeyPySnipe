#!/usr/bin/python
import argparse
import logging
import time
import sys
import json
import configparser
from POGOProtos.Enums import PokemonMove_pb2
from custom_exceptions import GeneralPogoException
import random
from api import PokeAuthSession
from location import Location

from pokedex import pokedex
from inventory import items
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from flask import jsonify
import thread
import subprocess
import os
import sys
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)

#this will execute the_task() every 30 seconds in the spooler



@app.route('/release')
def release():
    global released
    global sortBy
    inventory = session.getInventory()
    
    #id: 2436312686824190668
    #pokemon_id: EEVEE
    #cp: 46
    #stamina: 19
    #stamina_max: 19
    #move_1: TACKLE_FAST
    #move_2: DIG
    #height_m: 0.297532558441
    #weight_kg: 8.24643802643
    #individual_attack: 15
    #individual_defense: 12
    #individual_stamina: 9
    #cp_multiplier: 0.166397869587
    #pokeball: ITEM_POKE_BALL
    #captured_cell_id: 6108423709528162304
    #creation_time_ms: 1469364470778
    pokeID = request.args.get('pokeID', 0)
    action = request.args.get('action',0)
    sortBy = request.args.get('sortBy',0)
    
    
    
    for z in pokeID.split(","):
        
    
        for poke in range(0,len(inventory.party)-1):
            curPoke = inventory.party[poke]
            #logging.critical(str(curPoke.id) + "," + str(z))
            
            if str(curPoke.id) == str(z):
                iv = (round(inventory.party[poke].individual_attack + inventory.party[poke].individual_defense + inventory.party[poke].individual_stamina) / 45)
                
                #logging.critical(inventory.party[poke].individual_attack)
                #logging.critical(inventory.party[poke].individual_defense)
                #logging.critical(inventory.party[poke].individual_stamina)
                #logging.critical(iv)
                #logging.critical(iv*100)
                #logging.critical(int(iv*100))
                
                if action.find("Release") > -1:
                    logging.critical("Found pokemon. Transfer in progress...")
                    logging.critical(session.releasePokemon(inventory.party[poke]))
                    if len(pokeID.split(","))>1:
                        logging.critical("Rate limiting in effect, waiting before next action.")
                        time.sleep(int(config.get('CONFIG','releaseDelay')) + random.randint(1, 5))
                elif action.find("Evolve") > -1:
                    logging.critical("Found pokemon. Evolve in progress...")
                    logging.critical(session.evolvePokemon(inventory.party[poke]))
                    if len(pokeID.split(","))>1:
                        logging.critical("Rate limiting in effect, waiting before next action.")
                        time.sleep(int(config.get('CONFIG','evolveDelay')) + random.randint(1, 5))
                elif action.find("Rename") > -1:
                    logging.critical("Found pokemon. Renaming to " + str(pokedex[curPoke.pokemon_id]) + str(int(iv*100)))
                    logging.critical(session.nicknamePokemon(inventory.party[poke],str(pokedex[curPoke.pokemon_id]) + str(int(iv*100))))
                    if len(pokeID.split(","))>1:
                        logging.critical("Rate limiting in effect, waiting before next action.")
                        time.sleep(int(config.get('CONFIG','renameDelay')) + random.randint(1, 5))
                    #logging.critical(inventory.party)
                elif action.find("PowerUp") > -1:
                    logging.critical("Found pokemon. Upgrading.")
                    logging.critical(session.upgradePokemon(inventory.party[poke]))
                    if len(pokeID.split(","))>1:
                        logging.critical("Rate limiting in effect, waiting before next action.")
                        time.sleep(int(config.get('CONFIG','evolveDelay')) + random.randint(1, 5))
                    #logging.critical(inventory.party)
                    
    released = True                
    return render_template('inventoryTimeout.html')
    

@app.route('/inventory')
def inventory():
    global released
    inventory = session.getInventory()
    pokes = []
    #id: 2436312686824190668
    #pokemon_id: EEVEE
    #cp: 46
    #stamina: 19
    #stamina_max: 19
    #move_1: TACKLE_FAST
    #move_2: DIG
    #height_m: 0.297532558441
    #weight_kg: 8.24643802643
    #individual_attack: 15
    #individual_defense: 12
    #individual_stamina: 9
    #cp_multiplier: 0.166397869587
    #pokeball: ITEM_POKE_BALL
    #captured_cell_id: 6108423709528162304
    #creation_time_ms: 1469364470778
    
    
    for poke in range(0,len(inventory.party)):
        
    
        family = {'1': {1,2,3},'4': {4,5,6},'7': {7,8,9}, '10': {10,11,12}, '13': {13,14,15}, '16': {16,17,18}, '19': {19,20}, '21': {21,22}, '23': {23,24},'25': {25,26}, '27': {27,28}, '29': {29,30,31}, '32': {32,33,34}, '35': {35,36}, '37': {37,38}, '39': {39,40}, '41': {41,42}, '43': {43,44,45}, '46': {46,47}, '48': {48,49}, '50': {50,51}, '52': {52,53},'54': {54,55}, '56': {56,57}, '58': {58,59}, '60': {60,61,62}, '63': {63,64,65}, '66': {66,67,68},'69': {69,70,71}, '72': {72,73}, '74': {74,75,76}, '77': {77,78}, '79': {79,80}, '81': {81,82,83}, '84': {84,85}, '86': {86,87}, '88': {88,89}, '90': {90,91}, '92': {92,93,94}, '95': {95}, '96': {96,97}, '98': {98,99}, '100': {100,101}, '102': {102,103}, '104': {104,105}, '106': {106}, '107': {107},'108': {108}, '109': {109,110}, '111': {111,112}, '113': {113}, '114': {114}, '115': {115}, '116': {116,117}, '118': {118,119}, '120': {120,121},'122': {122}, '123': {123}, '124': {124}, '125': {125}, '126': {126}, '127': {127}, '128': {128}, '129': {129,130}, '131': {131}, '132': {132}, '133': {133,134,135,136},'137': {137}, '138': {138,139}, '140': {140,141},'142': {142}, '143': {143}, '144': {144}, '145': {145}, '146':{146}, '147': {147,148,149}, '150': {150}, '151': {151}}
        reqCandy = {'1':25,'2':100,'3':0,'4':25,'5':100,'6':0,'7':25,'8':100,'9':0,'10':12,'11':50,'12':0,'13':12,'14':50,'15':0,'16':12,'17':50,'18':0,'19':25,'20':0,'21':50,'22':0,'23':50,'24':0,'25':50,'26':0,'27':50,'28':0,'29':25,'30':100,'31':0,'32':25,'33':100,'34':0,'35':50,'36':0,'37':50,'38':0,'39':50,'40':0,'41':50,'42':0,'43':25,'44':100,'45':0,'46':50,'47':0,'48':50,'49':0,'50':50,'51':0,'52':50,'53':0,'54':50,'55':0,'56':50,'57':0,'58':50,'59':0,'60':25,'61':100,'62':0,'63':25,'64':100,'65':0,'66':25,'67':100,'68':0,'69':25,'70':100,'71':0,'72':50,'73':0,'74':25,'75':100,'76':0,'77':50,'78':0,'79':50,'80':0,'81':50,'82':0,'83':0,'84':50,'85':0,'86':50,'87':0,'88':50,'89':0,'90':50,'91':0,'92':25,'93':100,'94':0,'95':0,'96':50,'97':0,'98':50,'99':0,'100':50,'101':0,'102':50,'103':0,'104':50,'105':0,'106':0,'107':0,'108':0,'109':50,'110':0,'111':50,'112':0,'113':0,'114':0,'115':0,'116':50,'117':0,'118':50,'119':0,'120':50,'121':0,'122':0,'123':0,'124':0,'125':0,'126':0,'127':0,'128':0,'129':400,'130':0,'131':0,'132':0,'133':25,'134':0,'135':0,'136':0,'137':0,'138':50,'139':0,'140':50,'141':0,'142':0,'143':0,'144':0,'145':0,'146':0,'147':25,'148':100,'149':0,'150':0,'151':0}
        pokeMoves = {'13':['Wrap','Normal','25'],'14':['Hyper Beam','Normal','120'],'16':['Dark Pulse','Dark','45'],'18':['Sludge','Poison','30'],'20':['Vice Grip','Normal','25'],'21':['Flame Wheel','Fire','40'],'22':['Megahorn','Bug','80'],'24':['Flamethrower','Fire','55'],'26':['Dig','Ground','70'],'28':['Cross Chop','Fighting','60'],'30':['Psybeam','Psychic','40'],'31':['Earthquake','Ground','100'],'32':['Stone Edge','Rock','80'],'33':['Ice Punch','Ice','45'],'34':['Heart Stamp','Psychic','20'],'35':['Discharge','Electric','35'],'36':['Flash Cannon','Steel','60'],'38':['Drill Peck','Flying','40'],'39':['Ice Beam','Ice','65'],'40':['Blizzard','Ice','100'],'42':['Heat Wave','Fire','80'],'45':['Aerial Ace','Flying','30'],'46':['Drill Run','Ground','50'],'47':['Petal Blizzard','Grass','65'],'48':['Mega Drain','Grass','15'],'49':['Bug Buzz','Bug','75'],'50':['Poison Fang','Poison','25'],'51':['Night Slash','Dark','30'],'53':['Bubble Beam','Water','30'],'54':['Submission','Fighting','30'],'56':['Low Sweep','Fighting','30'],'57':['Aqua Jet','Water','25'],'58':['Aqua Tail','Water','45'],'59':['Seed Bomb','Grass','40'],'60':['Psyshock','Psychic','40'],'62':['Ancient Power','Rock','35'],'63':['Rock Tomb','Rock','30'],'64':['Rock Slide','Rock','50'],'65':['Power Gem','Rock','40'],'66':['Shadow Sneak','Ghost','15'],'67':['Shadow Punch','Ghost','20'],'69':['Ominous Wind','Ghost','30'],'70':['Shadow Ball','Ghost','45'],'72':['Magnet Bomb','Steel','30'],'74':['Iron Head','Steel','30'],'75':['Parabolic Charge','Electric','15'],'77':['Thunder Punch','Electric','40'],'78':['Thunder','Electric','100'],'79':['Thunderbolt','Electric','55'],'80':['Twister','Dragon','25'],'82':['Dragon Pulse','Dragon','65'],'83':['Dragon Claw','Dragon','35'],'84':['Disarming Voice','Fairy','25'],'85':['Draining Kiss','Fairy','25'],'86':['Dazzling Gleam','Fairy','55'],'87':['Moonblast','Fairy','85'],'88':['Play Rough','Fairy','55'],'89':['Cross Poison','Poison','25'],'90':['Sludge Bomb','Poison','55'],'91':['Sludge Wave','Poison','70'],'92':['Gunk Shot','Poison','65'],'94':['Bone Club','Ground','25'],'95':['Bulldoze','Ground','35'],'96':['Mud Bomb','Ground','30'],'99':['Signal Beam','Bug','45'],'100':['X-Scissor','Bug','35'],'101':['Flame Charge','Fire','25'],'102':['Flame Burst','Fire','30'],'103':['Fire Blast','Fire','100'],'104':['Brine','Water','25'],'105':['Water Pulse','Water','35'],'106':['Scald','Water','55'],'107':['Hydro Pump','Water','90'],'108':['Psychic','Psychic','55'],'109':['Psystrike','Psychic','70'],'111':['Icy Wind','Ice','25'],'114':['Giga Drain','Grass','35'],'115':['Fire Punch','Fire','40'],'116':['Solar Beam','Grass','120'],'117':['Leaf Blade','Grass','55'],'118':['Power Whip','Grass','70'],'121':['Air Cutter','Flying','30'],'122':['Hurricane','Flying','80'],'123':['Brick Break','Fighting','30'],'125':['Swift','Normal','30'],'126':['Horn Attack','Normal','25'],'127':['Stomp','Normal','30'],'129':['Hyper Fang','Normal','35'],'131':['Body Slam','Normal','40'],'132':['Rest','Normal','35'],'133':['Struggle','Normal','15'],'134':['Scald*','Water','35'],'135':['Hydro Pump*','Water','60'],'136':['Wrap*','Normal','15'],'137':['Wrap*','Normal','15'],'200':['Fury Cutter','Bug','3'],'201':['Bug Bite','Bug','5'],'202':['Bite','Dark','6'],'203':['Sucker Punch','Dark','7'],'204':['Dragon Breath','Dragon','6'],'205':['Thunder Shock','Electric','5'],'206':['Spark','Electric','7'],'207':['Low Kick','Fighting','5'],'208':['Karate Chop','Fighting','6'],'209':['Ember','Fire','10'],'210':['Wing Attack','Flying','9'],'211':['Peck','Flying','10'],'212':['Lick','Ghost','5'],'213':['Shadow Claw','Ghost','11'],'214':['Vine Whip','Grass','7'],'215':['Razor Leaf','Grass','15'],'216':['Mud Shot','Ground','6'],'217':['Ice Shard','Ice','15'],'218':['Frost Breath','Ice','9'],'219':['Quick Attack','Normal','10'],'220':['Scratch','Normal','6'],'221':['Tackle','Normal','12'],'222':['Pound','Normal','7'],'223':['Cut','Normal','12'],'224':['Poison Jab','Poison','12'],'225':['Acid','Poison','10'],'226':['Psycho Cut','Psychic','7'],'227':['Rock Throw','Rock','12'],'228':['Metal Claw','Steel','8'],'229':['Bullet Punch','Steel','10'],'230':['Water Gun','Water','6'],'231':['Splash','Water','0'],'232':['Water Gun*','Water','10'],'233':['Mud Slap','Ground','15'],'234':['Zen Headbutt','Psychic','12'],'235':['Confusion','Psychic','15'],'236':['Poison Sting','Poison','6'],'237':['Bubble','Water','25'],'238':['Feint Attack','Dark','12'],'239':['Steel Wing','Steel','15'],'240':['Fire Fang','Fire','10'],'241':['Rock Smash','Fighting','15']}
        
        curPoke = inventory.party[poke]   
        candies = 0
        nickName = None
        if released == True:
            timeStamp = int(round(time.time()))
            released = False
        else:
            timeStamp = 0
            
        if curPoke.nickname:
            nickName = curPoke.nickname
        else:
            nickName = pokedex[curPoke.pokemon_id]
            
        if str(curPoke.pokemon_id) not in family:
            
            for z in family:
                
                if curPoke.pokemon_id in family[z]:
                    #logging.critical(str(pokedex[curPoke.pokemon_id]) + " is in family " +str(z))
                    #logging.critical(inventory.candies)
                    candies = inventory.candies[int(z)]
                    candyFamily = pokedex[int(z)]
        else:
            #logging.critical(str(curPoke.pokemon_id) + " is a family!")
            candies = inventory.candies[curPoke.pokemon_id]
            candyFamily = pokedex[curPoke.pokemon_id]
        
        pokez = {
        'id': str(curPoke.id),
        'pokemon_id': curPoke.pokemon_id,
        'pokemon_name': nickName,
        'cp': curPoke.cp,
        'stamina': curPoke.stamina,
        'stamina_max': curPoke.stamina_max,
        'move_1': pokeMoves[str(curPoke.move_1)][0],
        'move_1_type': pokeMoves[str(curPoke.move_1)][1],
        'move_1_dmg': pokeMoves[str(curPoke.move_1)][2],
        'move_2': pokeMoves[str(curPoke.move_2)][0],
        'move_2_type': pokeMoves[str(curPoke.move_2)][1],
        'move_2_dmg': pokeMoves[str(curPoke.move_2)][2],
        'height_m': curPoke.height_m,
        'weight_kg': curPoke.weight_kg,
        'individual_attack': curPoke.individual_attack,
        'individual_defense': curPoke.individual_defense,
        'individual_stamina': curPoke.individual_stamina,
        'candies': candies,
        'reqCandies': reqCandy[str(curPoke.pokemon_id)],
        'candyFamily': candyFamily,
        'sortBy': sortBy,
        'timeStamp': timeStamp
        }
        pokes.append(pokez)
        
        
    
    
    
    json.dump(pokes, open('static/inventory.json', 'w'))
    
    return render_template('inventory.html')
    
@app.route('/')
def index():
    
    stats = session.getInventory().stats
    profileInfo = session.getProfile().player_data

        #level
        #experience: 2004695
        #prev_level_xp: 1650000
        #next_level_xp: 2500000
        #km_walked: 29.3902397156
        #pokemons_encountered: 4484
        #unique_pokedex_entries: 92
        #pokemons_captured: 4348
        #evolutions: 614
        #poke_stop_visits: 13337
        #pokeballs_thrown: 4819
        #eggs_hatched: 7
    
    
    if profileInfo.team:
        
        team = profileInfo.team
    else:
        team = 'noteam'
               
    statz = {
    'level': str(stats.level),
    'experience': str(stats.experience),
    'next_level_xp': str(stats.next_level_xp),
    'km_walked': str(stats.km_walked),
    'pokemons_encountered': str(stats.pokemons_encountered),
    'pokemons_captured': str(stats.pokemons_captured),
    'username': str(profileInfo.username),
    'max_pokemon_storage': str(profileInfo.max_pokemon_storage),
    'max_item_storage': str(profileInfo.max_item_storage),
    'team': team
     }

    json.dump(statz, open('static/stats.json', 'w'))
    

    return render_template('dashboard.html')
    


@app.errorhandler(500)
def page_not_found(e):
    return render_template('result.html'), 404

    
def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('Line %(lineno)d,%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)



# Get profile
def getProfile(session):
        logging.info("Printing Profile:")
        profile = session.getProfile()
        logging.info(profile)



# Do Inventory stuff
def getInventory(session):
    logging.info("Get Inventory:")
    logging.info(session.getInventory())

def hb():
   hb = session.getMapObjects()
    
    
    
    
    
    

if __name__ == '__main__':
    global sortBy
    sortBy = 'cp'
    global released
    released = False
    data = [{'status':'Server startup. Nothing to report.'}]
    json.dump(data, open('static/catch_data.json', 'w'))
    time.sleep(1)
    setupLogger()
    logging.debug('Logger set up')

    	
	#parse in configuration from config.ini
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    #config.get('AUTH','type')
    #config.get('AUTH','username')
    #config.get('AUTH','password')
    #config.get('CONFIG','startLoc')
    
    
    # Check service
    
    if config.get('AUTH','type') not in ['ptc', 'google']:
        logging.error('Invalid auth service {}'.format(config.get('AUTH','type')))
        sys.exit(-1)

    # Create PokoAuthObject
    poko_session = PokeAuthSession(
        config.get('AUTH','username'),
        config.get('AUTH','password'),
        config.get('AUTH','type'),
        ''.join(['encrypt/',config.get('CONFIG', 'encryptFile')]),
        geo_key=""
    )

    # Authenticate with a given location
    # Location is not inherent in authentication
    # But is important to session
    if config.get('CONFIG','startLoc'):
        session = poko_session.authenticate(locationLookup=config.get('CONFIG','startLoc'))
    else:
        session = poko_session.authenticate()

    
    logging.info("Successfuly logged in to Pokemon Go! Starting web server on port 5100.")
    
    ###Setting up HB:
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
    func=hb,
    trigger=IntervalTrigger(seconds=30),
    id='printing_job',
    name='Periodic call to getMapObjects to keep connection alive',
    replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    
    app.run(host='0.0.0.0', port=5100)
    url_for('static', filename='catch_data.json')
    
    	
    
	
