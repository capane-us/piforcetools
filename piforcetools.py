#!/usr/bin/python2

import os, collections, signal, sys, subprocess, socket, copy, operator, time
import triforcetools
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Define a signal handler to turn off LCD before shutting down
def handler(signum = None, frame = None):
    lcd = Adafruit_CharLCDPlate()
    lcd.clear()
    lcd.stop()
    sys.exit(0)
signal.signal(signal.SIGTERM , handler)

# Determine hardware revision and initialize LCD
revision = "unknown"
cpuinfo = open("/proc/cpuinfo", "r")
for line in cpuinfo:
    item = line.split(':', 1)
    if item[0].strip() == "Revision":
        revision = item[1].strip()
if revision.startswith('a'):
    lcd = Adafruit_CharLCDPlate(busnum = 1)
else:
    lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.noCursor()
lcd.noBlink()

# Importing configuration file & labels
try:
    from labels import *
    from config import *
except (SyntaxError, ImportError) as e:
    lcd.clear()
    print str(e)
    lcd.message("Error reading \nconfig files")
    sys.exit(1)

# DO NOT MODIFY THIS
HEART = [0B00000, 0B00000, 0B01010, 0B11111, 0B11111, 0B01110, 0B00100, 0B00000]
DOT = [0B00000, 0B00000, 0B00000, 0B00000, 0B00000, 0B00000, 0B00000, 0B10101]

# Try to import game list script, if it fails, signal error on LCD
try:
    from gamelist import GAME_LIST
except (SyntaxError, ImportError) as e:
    lcd.clear()
    lcd.message(LABELS[LANGUAGE][NO_GAME_LIST_ERROR])
    sleep(5)
    GAME_LIST = {}

# Backup used for the orphan roms. Only used there
GAME_LIST_BACKUP = copy.deepcopy(GAME_LIST)
SYSTEMS_FOR_UPLOAD_BACKUP = copy.deepcopy(SYSTEMS_FOR_UPLOAD)

# Try to import the views. If it fails, load the default one
try:
    from views import *
except (SyntaxError, ImportError) as e:
    VIEWS = [VIEW_BY_SYSTEMS, VIEW_BY_TYPES, FAVORITES, VIEW_ALL_GAMES, CHOOSE_SYSTEM_TO_PING, UNKNOWN_ROMS]
    GAMES_TYPES = [FIGHTING, ACTION, SPORT, HORI_SHOOTEMUP, VERT_SHOOTEMUP, PUZZLE, VARIOUS, RACING, SHOOTER]
    GAMES_SYSTEMS = [NAOMI1, NAOMI2, ATOMISWAVE, CHIHIRO, TRIFORCE]

# Creates the lists for each systems
def create_system_dict(dictionary, system):
    if GAME_LIST[system].has_key(GAMES):
        for key, value in GAME_LIST[system][GAMES].iteritems():
            for key2, value2 in GAME_LIST[system][GAMES][key].iteritems():
                if dictionary.has_key(GAMES) == False:
                    dictionary[GAMES] = {key2: {FILENAME: copy.deepcopy(GAME_LIST[system][GAMES][key][key2]), SYSTEMS: copy.deepcopy(GAME_LIST[system][SYSTEMS])}}
                else:
                    dictionary[GAMES].update({key2: {FILENAME: copy.deepcopy(GAME_LIST[system][GAMES][key][key2]), SYSTEMS: copy.deepcopy(GAME_LIST[system][SYSTEMS])}})
        dictionary[CATEGORY_NAME] = LABELS[LANGUAGE][system]

# Return the IP adress of a system
def get_ip_for_system(system):
    for j in range(len(SYSTEMS_FOR_UPLOAD)):
        if SYSTEMS_FOR_UPLOAD[j][0] == system:
            return SYSTEMS_FOR_UPLOAD[j][1]

# Creates the list of each game types
def create_game_type_dict(dictionary, game_type):
    systems_to_search = [ATOMISWAVE, NAOMI1, NAOMI2, CHIHIRO, TRIFORCE]
    
    for i in range(len(systems_to_search)):
        if GAME_LIST[systems_to_search[i]].has_key(GAMES):
            if GAME_LIST[systems_to_search[i]][GAMES].has_key(game_type):
                for key, value in GAME_LIST[systems_to_search[i]][GAMES][game_type].iteritems():
                    if dictionary.has_key(GAMES) == False:
                        dictionary[GAMES] = {key: {FILENAME: copy.deepcopy(GAME_LIST[systems_to_search[i]][GAMES][game_type][key]), SYSTEMS: copy.deepcopy(GAME_LIST[systems_to_search[i]][SYSTEMS])}}
                    else:
                        dictionary[GAMES].update({key: {FILENAME: copy.deepcopy(GAME_LIST[systems_to_search[i]][GAMES][game_type][key]), SYSTEMS: copy.deepcopy(GAME_LIST[systems_to_search[i]][SYSTEMS])}})

    dictionary[CATEGORY_NAME] = LABELS[LANGUAGE][game_type]

# Transform the games as a sorted list    
def sort_game_list(dictionary):
    if dictionary.has_key(GAMES):
        sorted_list = sorted(dictionary[GAMES].items(), key=lambda t: t[0])
        dictionary[GAMES] = sorted_list

# Return the inputs
last_time_long_pressed = time.time()
def read_buttons(input_signal):
    global last_time_long_pressed
    if input_signal.buttonPressed(input_signal.LEFT):
        pressed_time = time.time()
        while input_signal.buttonPressed(input_signal.LEFT) and time.time() - pressed_time < TIME_FOR_LONG_PRESS:
            pass
        # Long press
        if time.time() - pressed_time >= TIME_FOR_LONG_PRESS:
            sleep(SLEEP_AFTER_LONG_PRESS)
            last_time_long_pressed = time.time()
            return LONG_LEFT
        else:
            # Ignore a short press just after a long press
            if time.time() - last_time_long_pressed >= TIME_FOR_LONG_PRESS:
                sleep(SLEEP_AFTER_SHORT_PRESS)
                return SHORT_LEFT
    elif input_signal.buttonPressed(input_signal.RIGHT):
        pressed_time = time.time()
        while input_signal.buttonPressed(input_signal.RIGHT) and time.time() - pressed_time < TIME_FOR_LONG_PRESS:
            pass
        # Long press
        if time.time() - pressed_time >= TIME_FOR_LONG_PRESS:
            sleep(SLEEP_AFTER_LONG_PRESS)
            last_time_long_pressed = time.time()
            return LONG_RIGHT
        else:
            # Ignore a short press just after a long press
            if time.time() - last_time_long_pressed >= TIME_FOR_LONG_PRESS:
                sleep(SLEEP_AFTER_SHORT_PRESS)
                return SHORT_RIGHT
    elif lcd.buttonPressed(input_signal.UP):
        pressed_time = time.time()
        while input_signal.buttonPressed(input_signal.UP) and time.time() - pressed_time < TIME_FOR_LONG_PRESS:
            pass
        # Long press
        if time.time() - pressed_time >= TIME_FOR_LONG_PRESS:
            sleep(SLEEP_AFTER_LONG_PRESS)
            last_time_long_pressed = time.time()
            return LONG_UP
        else:
            # Ignore a short press just after a long press
            if time.time() - last_time_long_pressed >= TIME_FOR_LONG_PRESS:
                sleep(SLEEP_AFTER_SHORT_PRESS)
                return SHORT_UP
    elif input_signal.buttonPressed(input_signal.DOWN):
        pressed_time = time.time()
        while input_signal.buttonPressed(input_signal.DOWN) and time.time() - pressed_time < TIME_FOR_LONG_PRESS:
            pass
        # Long press
        if time.time() - pressed_time >= TIME_FOR_LONG_PRESS:
            sleep(SLEEP_AFTER_LONG_PRESS)
            last_time_long_pressed = time.time()
            return LONG_DOWN
        else:
            # Ignore a short press just after a long press
            if time.time() - last_time_long_pressed >= TIME_FOR_LONG_PRESS:
                sleep(SLEEP_AFTER_SHORT_PRESS)
                return SHORT_DOWN
    elif input_signal.buttonPressed(input_signal.SELECT):
        pressed_time = time.time()
        while input_signal.buttonPressed(input_signal.SELECT) and time.time() - pressed_time < TIME_FOR_LONG_PRESS:
            pass
        # Long press
        if time.time() - pressed_time >= TIME_FOR_LONG_PRESS:
            sleep(SLEEP_AFTER_LONG_PRESS)
            last_time_long_pressed = time.time()
            return LONG_SELECT
        else:
            # Ignore a short press just after a long press
            if time.time() - last_time_long_pressed >= TIME_FOR_LONG_PRESS:
                sleep(SLEEP_AFTER_SHORT_PRESS)
                return SHORT_SELECT
    return NONE

# Contains the history of navigation 
history = []

# Adds a new element in history but keeps it <= 10
def add_element_to_history(mode):    
    global history
    
    if len(history) > 10:
        del history[0]
    
    history.insert(len(history), mode)

# Allows to go back in time :)
def go_back_to_history():
    global history
    
    last_mode = history[len(history) - 2]
    del history[len(history) - 1]
    
    return last_mode


# Opens the files containing the rom file names and then creates a list
def read_favorites(dictionary):
    favorites_read_from_file = []
    
    try:
        with open(FAVORITES_FILE) as file:
            for line in file:
                line = line.strip()
                favorites_read_from_file.append(line)
        file.close()
        
        systems_to_search = [ATOMISWAVE, NAOMI1, NAOMI2, CHIHIRO, TRIFORCE]
        game_types = [RACING, ACTION, SHOOTER, SPORT, FIGHTING, HORI_SHOOTEMUP, VERT_SHOOTEMUP, VARIOUS, PUZZLE]
    
        for i in range(len(systems_to_search)):
            for j in range(len(game_types)):
                if GAME_LIST[systems_to_search[i]].has_key(GAMES):
                    if GAME_LIST[systems_to_search[i]][GAMES].has_key(game_types[j]):
                        for key, value in GAME_LIST[systems_to_search[i]][GAMES][game_types[j]].iteritems():
                            if GAME_LIST[systems_to_search[i]][GAMES][game_types[j]][key] in favorites_read_from_file:
                                if dictionary.has_key(GAMES) == False:
                                    dictionary[GAMES] = {key: {FILENAME: copy.deepcopy(GAME_LIST[systems_to_search[i]][GAMES][game_types[j]][key]), SYSTEMS: copy.deepcopy(GAME_LIST[systems_to_search[i]][SYSTEMS])}}
                                else:
                                    dictionary[GAMES].update({key: {FILENAME: copy.deepcopy(GAME_LIST[systems_to_search[i]][GAMES][game_types[j]][key]), SYSTEMS: copy.deepcopy(GAME_LIST[systems_to_search[i]][SYSTEMS])}})

        dictionary[CATEGORY_NAME] = LABELS[LANGUAGE][FAVORITES]
    except:
        pass
    
    return dictionary

# Allows you to add a game to your favorites list and file
def add_favorite(game_to_add):
    global list_favorites
    list_favorites = {}
    read_favorites(list_favorites)
    if list_favorites.has_key(GAMES) == False:
        list_favorites[GAMES] = {copy.deepcopy(game_to_add[0]): {FILENAME: copy.deepcopy(game_to_add[1][FILENAME]), SYSTEMS: game_to_add[1][SYSTEMS]}}
    else:
        list_favorites[GAMES].update({copy.deepcopy(game_to_add[0]): {FILENAME: copy.deepcopy(game_to_add[1][FILENAME]), SYSTEMS: game_to_add[1][SYSTEMS]}})
    sort_game_list(list_favorites)
    
    if os.path.isfile(FAVORITES_FILE) == True:
        os.remove(FAVORITES_FILE)
    file = open(FAVORITES_FILE, "w")
    for key, value in list_favorites[GAMES]:
        file.write(value[FILENAME] + "\n")
    file.close()
    
    list_favorites = {}
    read_favorites(list_favorites)
    sort_game_list(list_favorites)
    
# Remove a game from the favorites list and then recreates the file to keep it up to date
def remove_favorite(game_to_remove):
    global list_favorites
    if os.path.isfile(FAVORITES_FILE) == True:
        os.remove(FAVORITES_FILE)
    file = open(FAVORITES_FILE, "w")
    for key, value in list_favorites[GAMES]:
        if value[FILENAME] != game_to_remove[1][FILENAME]:
            file.write(value[FILENAME] + "\n")
    file.close()
    
    list_favorites = {}
    read_favorites(list_favorites)
    sort_game_list(list_favorites)
    

# Allows you to know wether a game in one of your favorite or not
def is_favorite_game(game_file):
    if list_favorites.has_key(GAMES) == True:
        for key, value in list_favorites[GAMES]:
            if value[FILENAME] == game_file:
                return True
    return False

# Show on the lcd the game (adding the heart if it's one of your favorites)
def show_game(game):
    lcd.createChar(1, DOT)
    lcd.createChar(2, HEART)
    game_to_show = game[0]
    
    if is_favorite_game(game[1][FILENAME]):
        if game_to_show.count("\n") > 0:
            if len(game_to_show.split("\n")[1]) > 13:
                game_to_show = game_to_show.split("\n")[0] + "\n" + game_to_show.split("\n")[1][:-3] + "\x01 \x02"
            else:
                while len(game_to_show.split("\n")[1]) < 15:
                    game_to_show += " "
                game_to_show += "\x02"
        else:
            game_to_show += "\n               \x02"
                
    lcd.message(game_to_show) 

def get_string_for_display(filename):
    if len(filename) > 16:
        temp_filename = filename[0:14] + "\n" + filename[14:]
        filename = temp_filename
    return filename
    
def create_unknown_roms(list_unknown_roms):
    systems_to_search = [ATOMISWAVE, NAOMI1, NAOMI2, CHIHIRO, TRIFORCE]

    roms = [ f for f in os.listdir(ROM_DIR) if os.path.isfile(ROM_DIR + f) ]
    for rom in roms:
        found = False
        for i in range(len(systems_to_search)):
            for key, value in GAME_LIST[systems_to_search[i]][GAMES].iteritems():
                for key2, value2 in GAME_LIST[systems_to_search[i]][GAMES][key].iteritems():
                    if value2 == rom:
                        found = True
        if found == False:
            list_unknown_roms.append(rom)
    list_unknown_roms = sorted(list_unknown_roms, key=lambda t: t[0])

def get_game_rom_file(game_name):
    systems_to_search = [ATOMISWAVE, NAOMI1, NAOMI2, CHIHIRO, TRIFORCE]
        
    for i in range(len(systems_to_search)):
        for key, value in GAME_LIST_BACKUP[systems_to_search[i]][GAMES].iteritems():
            for key2, value2 in GAME_LIST_BACKUP[systems_to_search[i]][GAMES][key].iteritems():
                if key2 == game_name:
                    return value2
    
def rename_rom(UNKNOWN_ROMS_idx, UNKNOWN_ROMS_CHOOSE_GAME_idx):
    real_filename = get_game_rom_file(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx])
    try:
        os.rename(ROM_DIR + list_unknown_roms[UNKNOWN_ROMS_idx], ROM_DIR + real_filename)
        return True
    except:
        return False



# Defines all the lists
list_by_system_atomiswave = {}
list_by_system_naomi1 = {}
list_by_system_naomi2 = {}
list_by_system_chihiro = {}
list_by_system_triforce = {}
list_by_game_type_racing = {}
list_by_game_type_shooter = {}
list_by_game_type_action = {}
list_by_game_type_sport = {}
list_by_game_type_fighting = {}
list_by_game_type_hori_shootemup = {}
list_by_game_type_vert_shootemup = {}
list_by_game_type_various = {}
list_by_game_type_puzzle = {}
list_all_games = {}
list_favorites = {}
list_unknown_roms = []
game_without_rom = []


def create_lists():
    global GAME_LIST
    global game_without_rom
    global list_by_system_atomiswave
    global list_by_system_naomi1
    global list_by_system_naomi2
    global list_by_system_chihiro
    global list_by_system_triforce
    global list_by_game_type_racing 
    global list_by_game_type_shooter
    global list_by_game_type_action
    global list_by_game_type_sport
    global list_by_game_type_fighting
    global list_by_game_type_hori_shootemup
    global list_by_game_type_vert_shootemup
    global list_by_game_type_various
    global list_by_game_type_puzzle
    global list_all_games
    global list_favorites
    global list_unknown_roms
    global game_without_rom
    global SYSTEMS_FOR_UPLOAD
    
    list_by_system_atomiswave = {}
    list_by_system_naomi1 = {}
    list_by_system_naomi2 = {}
    list_by_system_chihiro = {}
    list_by_system_triforce = {}
    list_by_game_type_racing = {}
    list_by_game_type_shooter = {}
    list_by_game_type_action = {}
    list_by_game_type_sport = {}
    list_by_game_type_fighting = {}
    list_by_game_type_hori_shootemup = {}
    list_by_game_type_vert_shootemup = {}
    list_by_game_type_various = {}
    list_by_game_type_puzzle = {}
    list_all_games = {}
    list_favorites = {}
    list_unknown_roms = []
    game_without_rom = []
    
    GAME_LIST = copy.deepcopy(GAME_LIST_BACKUP)
    SYSTEMS_FOR_UPLOAD = copy.deepcopy(SYSTEMS_FOR_UPLOAD_BACKUP)
    
    create_unknown_roms(list_unknown_roms)
    if PURGE_SYSTEMS:
        # We simply remove the systems of GAME_LIST that couldn't be found in SYSTEMS_FOR_UPLOAD
        dictionary_temp = copy.deepcopy(GAME_LIST)
        for cat_key, cat_value in GAME_LIST.iteritems():
            nb_system_removed = 0
            for i in range(len(cat_value[SYSTEMS])):
                if SYSTEMS_FOR_UPLOAD.get(cat_value[SYSTEMS][i]) == None:
                    dictionary_temp[cat_key][SYSTEMS].pop(i - nb_system_removed)
                    nb_system_removed = nb_system_removed + 1
        GAME_LIST = copy.deepcopy(dictionary_temp)  
        
    # Purge game dictionary of game files that cannot be found
    if PURGE_GAMES:
        dictionary_temp = copy.deepcopy(GAME_LIST)
        for systems_key, systems_value in GAME_LIST.iteritems():
            for types_key, types_value in GAME_LIST[systems_key][GAMES].iteritems():
                for games_key, games_value in GAME_LIST[systems_key][GAMES][types_key].iteritems():
                    if not os.path.isfile(ROM_DIR + GAME_LIST[systems_key][GAMES][types_key][games_key]):
                        game_without_rom.append(games_key)
                        if dictionary_temp[systems_key][GAMES].has_key(types_key):
                            del dictionary_temp[systems_key][GAMES][types_key][games_key]
        GAME_LIST = copy.deepcopy(dictionary_temp)
        for systems_key, systems_value in GAME_LIST.iteritems():
            for types_key, types_value in GAME_LIST[systems_key][GAMES].iteritems():
                if len(GAME_LIST[systems_key][GAMES][types_key]) == 0:
                    del dictionary_temp[systems_key][GAMES][types_key]
        GAME_LIST = copy.deepcopy(dictionary_temp)
        for systems_key, systems_value in GAME_LIST.iteritems():
            if len(GAME_LIST[systems_key][GAMES]) == 0:
                del dictionary_temp[systems_key][GAMES]
        GAME_LIST = copy.deepcopy(dictionary_temp)
        game_without_rom = sorted(game_without_rom, key=lambda t: t[0])

    
    # We add games to all the lists and sorts them
    create_system_dict(list_by_system_atomiswave, ATOMISWAVE)
    sort_game_list(list_by_system_atomiswave)
    create_system_dict(list_by_system_naomi1, NAOMI1)
    sort_game_list(list_by_system_naomi1)
    create_system_dict(list_by_system_naomi2, NAOMI2)
    sort_game_list(list_by_system_naomi2)
    create_system_dict(list_by_system_chihiro, CHIHIRO)
    sort_game_list(list_by_system_chihiro)
    create_system_dict(list_by_system_triforce, TRIFORCE)
    sort_game_list(list_by_system_triforce)
    create_game_type_dict(list_by_game_type_racing, RACING)
    sort_game_list(list_by_game_type_racing)
    create_game_type_dict(list_by_game_type_shooter, SHOOTER)
    sort_game_list(list_by_game_type_shooter)
    create_game_type_dict(list_by_game_type_action, ACTION)
    sort_game_list(list_by_game_type_action)
    create_game_type_dict(list_by_game_type_sport, SPORT)
    sort_game_list(list_by_game_type_sport)
    create_game_type_dict(list_by_game_type_fighting, FIGHTING)
    sort_game_list(list_by_game_type_fighting)
    create_game_type_dict(list_by_game_type_hori_shootemup, HORI_SHOOTEMUP)
    sort_game_list(list_by_game_type_hori_shootemup)
    create_game_type_dict(list_by_game_type_vert_shootemup, VERT_SHOOTEMUP)
    sort_game_list(list_by_game_type_vert_shootemup)
    create_game_type_dict(list_by_game_type_various, VARIOUS)
    sort_game_list(list_by_game_type_various)
    create_game_type_dict(list_by_game_type_puzzle, PUZZLE)
    sort_game_list(list_by_game_type_puzzle)
    # all games types, for the "all game" menu
    create_game_type_dict(list_all_games, RACING)
    create_game_type_dict(list_all_games, SHOOTER)
    create_game_type_dict(list_all_games, ACTION)
    create_game_type_dict(list_all_games, SPORT)
    create_game_type_dict(list_all_games, FIGHTING)
    create_game_type_dict(list_all_games, HORI_SHOOTEMUP)
    create_game_type_dict(list_all_games, VERT_SHOOTEMUP)
    create_game_type_dict(list_all_games, VARIOUS)
    create_game_type_dict(list_all_games, PUZZLE)
    sort_game_list(list_all_games)
    list_all_games[CATEGORY_NAME] = None
    read_favorites(list_favorites)
    sort_game_list(list_favorites)


    # Purge the menus : if the game list of a menu is empty, no need to show it
    if list_by_system_atomiswave.has_key(GAMES) == False or len(list_by_system_atomiswave[GAMES]) == 0:
        if GAMES_SYSTEMS.count(ATOMISWAVE) > 0:
            GAMES_SYSTEMS.pop(GAMES_SYSTEMS.index(ATOMISWAVE))
    if list_by_system_naomi1.has_key(GAMES) == False or len(list_by_system_naomi1[GAMES]) == 0:
        if GAMES_SYSTEMS.count(NAOMI1) > 0:
            GAMES_SYSTEMS.pop(GAMES_SYSTEMS.index(NAOMI1))
    if list_by_system_naomi2.has_key(GAMES) == False or len(list_by_system_naomi2[GAMES]) == 0:
        if GAMES_SYSTEMS.count(NAOMI2) > 0:
            GAMES_SYSTEMS.pop(GAMES_SYSTEMS.index(NAOMI2))
    if list_by_system_chihiro.has_key(GAMES) == False or len(list_by_system_chihiro[GAMES]) == 0:
        if GAMES_SYSTEMS.count(CHIHIRO) > 0:
            GAMES_SYSTEMS.pop(GAMES_SYSTEMS.index(CHIHIRO))
    if list_by_system_triforce.has_key(GAMES) == False or len(list_by_system_triforce[GAMES]) == 0:
        if GAMES_SYSTEMS.count(TRIFORCE) > 0:
            GAMES_SYSTEMS.pop(GAMES_SYSTEMS.index(TRIFORCE))  
    if list_by_game_type_racing.has_key(GAMES) == False or len(list_by_game_type_racing[GAMES]) == 0:
        if GAMES_TYPES.count(RACING) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(RACING))
    if list_by_game_type_shooter.has_key(GAMES) == False or len(list_by_game_type_shooter[GAMES]) == 0:
        if GAMES_TYPES.count(SHOOTER) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(SHOOTER))
    if list_by_game_type_action.has_key(GAMES) == False or len(list_by_game_type_action[GAMES]) == 0:
        if GAMES_TYPES.count(ACTION) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(ACTION))
    if list_by_game_type_sport.has_key(GAMES) == False or len(list_by_game_type_sport[GAMES]) == 0:
        if GAMES_TYPES.count(SPORT) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(SPORT))
    if list_by_game_type_fighting.has_key(GAMES) == False or len(list_by_game_type_fighting[GAMES]) == 0:
        if GAMES_TYPES.count(FIGHTING) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(FIGHTING))
    if list_by_game_type_hori_shootemup.has_key(GAMES) == False or len(list_by_game_type_hori_shootemup[GAMES]) == 0:
        if GAMES_TYPES.count(HORI_SHOOTEMUP) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(HORI_SHOOTEMUP))
    if list_by_game_type_vert_shootemup.has_key(GAMES) == False or len(list_by_game_type_vert_shootemup[GAMES]) == 0:
        if GAMES_TYPES.count(VERT_SHOOTEMUP) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(VERT_SHOOTEMUP))
    if list_by_game_type_various.has_key(GAMES) == False or len(list_by_game_type_various[GAMES]) == 0:
        if GAMES_TYPES.count(VARIOUS) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(VARIOUS))
    if list_by_game_type_puzzle.has_key(GAMES) == False or len(list_by_game_type_puzzle[GAMES]) == 0:
        if GAMES_TYPES.count(PUZZLE) > 0:
            GAMES_TYPES.pop(GAMES_TYPES.index(PUZZLE))


    if list_all_games.has_key(GAMES) == False or len(list_all_games[GAMES]) == 0:
        VIEWS.pop(VIEWS.index(VIEW_ALL_GAMES))
    if len(GAMES_TYPES) == 0 and VIEWS.count(VIEW_BY_TYPES) > 0:
        VIEWS.pop(VIEWS.index(VIEW_BY_TYPES))
    if len(GAMES_SYSTEMS) == 0 and VIEWS.count(VIEW_BY_SYSTEMS) > 0:
        VIEWS.pop(VIEWS.index(VIEW_BY_SYSTEMS))
    if len(list_unknown_roms) == 0 and VIEWS.count(UNKNOWN_ROMS) > 0:
        VIEWS.pop(VIEWS.index(UNKNOWN_ROMS))

    # No games found message if there are none to show
    if VIEWS.count(VIEW_BY_SYSTEMS) < 1 and VIEWS.count(VIEW_BY_TYPES) < 1 and VIEWS.count(VIEW_ALL_GAMES) < 1 and VIEWS.count(FAVORITES) < 1:
        VIEWS.insert(0, LABELS[LANGUAGE][NO_GAMES_FOUND])

# Some initialisations    
TOP_VIEW_idx = 0
SUB_CATEGORIES_idx = 0
SHOW_GAMES_idx = 0
SYSTEM_TO_PING_idx = 0
SYSTEM_TO_UPLOAD_idx = 0
UNKNOWN_ROMS_idx = 0
UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
mode = None
nb_game_cat_in_top_view = 0

create_lists()

# Let's sort the different systems for easy finding
SYSTEMS_FOR_UPLOAD = sorted(SYSTEMS_FOR_UPLOAD.items(), key=lambda t: t[0])

# Welcome message ?
if SHOW_WELCOME_MESSAGE:
    lcd.message(LABELS[LANGUAGE][WELCOME_MESSAGE])
    sleep(SLEEP_AFTER_MESSAGE)
    lcd.clear()

# Let's count what we have to show in the top view
if VIEW_BY_SYSTEMS in VIEWS:
    nb_game_cat_in_top_view += 1
if VIEW_BY_TYPES in VIEWS:
    nb_game_cat_in_top_view += 1
if VIEW_ALL_GAMES in VIEWS:
    nb_game_cat_in_top_view += 1
if FAVORITES in VIEWS:
    nb_game_cat_in_top_view += 1

# Do we really have to show a top view ? It depends on the user settings...
if nb_game_cat_in_top_view == 0 and CHOOSE_SYSTEM_TO_PING in VIEWS:
    lcd.message(LABELS[LANGUAGE][NO_CATEGORY_TO_SHOW])
    sleep(SLEEP_AFTER_MESSAGE)
    lcd.clear()
    lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
    mode = TOP_VIEW
    add_element_to_history(TOP_VIEW)
elif nb_game_cat_in_top_view == 0:
    lcd.message(LABELS[LANGUAGE][NOTHING_TO_SHOW])
elif nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS:
    lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
    mode = TOP_VIEW
    add_element_to_history(TOP_VIEW)
elif nb_game_cat_in_top_view == 1:
    if VIEW_BY_SYSTEMS in VIEWS:
        lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
        mode = VIEW_BY_SYSTEMS
        add_element_to_history(VIEW_BY_SYSTEMS)
    elif VIEW_BY_TYPES in VIEWS:
        lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
        mode = VIEW_BY_TYPES
        add_element_to_history(VIEW_BY_TYPES)
    elif VIEW_ALL_GAMES in VIEWS:
        current_game_list = list_all_games[GAMES]
        show_game(current_game_list[SHOW_GAMES_idx])
        mode = VIEW_ALL_GAMES  
        add_element_to_history(VIEW_ALL_GAMES)
    elif FAVORITES in VIEWS:
        if list_favorites.get(GAMES) == None:
            lcd.message(LABELS[LANGUAGE][NOTHING_TO_SHOW])
        else:
            current_game_list = list_favorites[GAMES]
            show_game(current_game_list[SHOW_GAMES_idx])
            mode = FAVORITES  
            add_element_to_history(FAVORITES)
elif nb_game_cat_in_top_view > 1:
    lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
    mode = TOP_VIEW
    add_element_to_history(TOP_VIEW)

# Never stops !    
while True:
    button = read_buttons(lcd)
    # We're on the top view !
    if mode == TOP_VIEW:
        if button == TOP_VIEW_NEXT_ITEM:
            if TOP_VIEW_idx == len(VIEWS) - 1:
                TOP_VIEW_idx = 0
            else:
                TOP_VIEW_idx += 1
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
        elif button == TOP_VIEW_PREVIOUS_ITEM:
            if TOP_VIEW_idx == 0:
                TOP_VIEW_idx = len(VIEWS) - 1
            else:
                TOP_VIEW_idx -= 1
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
        elif button == TOP_VIEW_SELECT:
            add_element_to_history(VIEWS[TOP_VIEW_idx])
            mode = VIEWS[TOP_VIEW_idx] 
            lcd.clear()
            # Depends on the selection
            if VIEWS[TOP_VIEW_idx] == VIEW_BY_SYSTEMS:
                lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
            elif VIEWS[TOP_VIEW_idx] == VIEW_BY_TYPES:
                lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
            elif VIEWS[TOP_VIEW_idx] == VIEW_ALL_GAMES:
                current_game_list = list_all_games[GAMES]
                show_game(current_game_list[SHOW_GAMES_idx])
            elif VIEWS[TOP_VIEW_idx] == UNKNOWN_ROMS:
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
            elif VIEWS[TOP_VIEW_idx] == FAVORITES:
                # No fav to show
                if list_favorites.has_key(GAMES) == False or len(list_favorites[GAMES]) == 0:
                    lcd.clear()
                    lcd.message(LABELS[LANGUAGE][NO_FAVORITES_DEFINED])
                    sleep(SLEEP_AFTER_MESSAGE)
                    lcd.clear()
                    lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                    mode = TOP_VIEW
                    add_element_to_history(TOP_VIEW)
                else:
                    current_game_list = list_favorites[GAMES]
                    show_game(current_game_list[SHOW_GAMES_idx])
            elif VIEWS[TOP_VIEW_idx] == CHOOSE_SYSTEM_TO_PING:
                # Do we have some systems to choose ?
                if len(SYSTEMS_FOR_UPLOAD) > 0:
                    SYSTEM_TO_PING_idx = 0
                    lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
                else:
                    lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                    sleep(SLEEP_AFTER_MESSAGE)
                    lcd.clear()
                    lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
        elif button == PING_SHORTCUT:
            lcd.clear()
            # Do we have some systems to ping ?
            if len(SYSTEMS_FOR_UPLOAD) > 0:
                TOP_VIEW_idx = 0
                add_element_to_history(CHOOSE_SYSTEM_TO_PING)
                mode = CHOOSE_SYSTEM_TO_PING
                SYSTEM_TO_PING_idx = 0
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
        elif button == TOP_VIEW_RETURN_TOP_VIEW:
            # If we need a top view, we show it 
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                TOP_VIEW_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
    elif mode == VIEW_BY_SYSTEMS or mode == VIEW_BY_TYPES:
        if mode == VIEW_BY_SYSTEMS:
            sub_category_list = GAMES_SYSTEMS
        elif mode == VIEW_BY_TYPES:
            sub_category_list = GAMES_TYPES
        if button == SUB_VIEW_NEXT_ITEM:
            if SUB_CATEGORIES_idx == len(sub_category_list) - 1:
                SUB_CATEGORIES_idx = 0
            else:
                SUB_CATEGORIES_idx += 1
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][sub_category_list[SUB_CATEGORIES_idx]])
        elif button == SUB_VIEW_PREVIOUS_ITEM:
            if SUB_CATEGORIES_idx == 0:
                SUB_CATEGORIES_idx = len(sub_category_list) - 1
            else:
                SUB_CATEGORIES_idx -= 1
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][sub_category_list[SUB_CATEGORIES_idx]])
        elif button == SUB_VIEW_SELECT:
            lcd.clear()
            if mode == VIEW_BY_SYSTEMS:
                if sub_category_list[SUB_CATEGORIES_idx] == ATOMISWAVE:
                    current_game_list = list_by_system_atomiswave[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == NAOMI1:
                    current_game_list = list_by_system_naomi1[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == NAOMI2:
                    current_game_list = list_by_system_naomi2[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == CHIHIRO:
                    current_game_list = list_by_system_chihiro[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == TRIFORCE:
                    current_game_list = list_by_system_triforce[GAMES]
            elif mode == VIEW_BY_TYPES:
                if sub_category_list[SUB_CATEGORIES_idx] == RACING:
                    current_game_list = list_by_game_type_racing[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == SHOOTER:
                    current_game_list = list_by_game_type_shooter[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == ACTION:
                    current_game_list = list_by_game_type_action[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == SPORT:
                    current_game_list = list_by_game_type_sport[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == FIGHTING:
                    current_game_list = list_by_game_type_fighting[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == HORI_SHOOTEMUP:
                    current_game_list = list_by_game_type_hori_shootemup[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == VERT_SHOOTEMUP:
                    current_game_list = list_by_game_type_vert_shootemup[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == VARIOUS:
                    current_game_list = list_by_game_type_various[GAMES]
                elif sub_category_list[SUB_CATEGORIES_idx] == PUZZLE:
                    current_game_list = list_by_game_type_puzzle[GAMES]
            SHOW_GAMES_idx = 0
            show_game(current_game_list[SHOW_GAMES_idx])
            add_element_to_history(SHOW_GAMES)
            mode = SHOW_GAMES
        # Always the same code block for sub view return... 
        elif button == SUB_VIEW_RETURN:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                SUB_CATEGORIES_idx = 0
                mode = go_back_to_history()
                if mode == TOP_VIEW:
                    lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                elif mode == VIEW_BY_SYSTEMS:
                    lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
                elif mode == VIEW_BY_TYPES:
                    lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
                elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
                    show_game(current_game_list[SHOW_GAMES_idx])
                elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
                    lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
                elif mode == CHOOSE_SYSTEM_TO_PING:
                    lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
                elif mode == UNKNOWN_ROMS:
                    lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == SUB_VIEW_RETURN_TOP_VIEW:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                TOP_VIEW_idx = 0
                SUB_CATEGORIES_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_UPLOAD_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                UNKNOWN_ROMS_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
        elif button == PING_SHORTCUT:
            lcd.clear()
            if len(SYSTEMS_FOR_UPLOAD) > 0:
                SUB_CATEGORIES_idx = 0
                TOP_VIEW_idx = 0
                mode = CHOOSE_SYSTEM_TO_PING
                add_element_to_history(CHOOSE_SYSTEM_TO_PING)
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(LABELS[LANGUAGE][sub_category_list[SUB_CATEGORIES_idx]])
    elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
        if button == SHOW_GAMES_NEXT_GAME:
            if SHOW_GAMES_idx == len(current_game_list) - 1:
                SHOW_GAMES_idx = 0
            else:
                SHOW_GAMES_idx += 1
            lcd.clear()
            show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_PREVIOUS_GAME:
            if SHOW_GAMES_idx == 0:
                SHOW_GAMES_idx = len(current_game_list) - 1
            else:
                SHOW_GAMES_idx -= 1
            lcd.clear()
            show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_NEXT_LETTER:
            if SHOW_GAMES_idx == 0:
                old_SHOW_GAMES_idx = len(current_game_list) - 1
            else:
                old_SHOW_GAMES_idx = SHOW_GAMES_idx - 1
            
            notFound = True
            while(notFound):
                currentFirstLetter = current_game_list[SHOW_GAMES_idx][0][0].upper()
                if SHOW_GAMES_idx < len(current_game_list) - 1:
                    nextFirstLetter = current_game_list[SHOW_GAMES_idx + 1][0][0].upper()
                else:
                    nextFirstLetter = current_game_list[0][0][0].upper() 
                        
                if(currentFirstLetter != nextFirstLetter or old_SHOW_GAMES_idx == SHOW_GAMES_idx):
                    notFound = False
                
                if (old_SHOW_GAMES_idx != SHOW_GAMES_idx):
                    if SHOW_GAMES_idx == len(current_game_list) - 1:
                        SHOW_GAMES_idx = 0
                    else:
                        SHOW_GAMES_idx += 1  
            lcd.clear()
            show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_PREVIOUS_LETTER:
            if SHOW_GAMES_idx == len(current_game_list) - 1:
                old_SHOW_GAMES_idx = 0
            else:
                old_SHOW_GAMES_idx = SHOW_GAMES_idx + 1

            notFound = True
            cptLetterChange = 0
            while(notFound):
                currentFirstLetter = current_game_list[SHOW_GAMES_idx][0][0].upper()
                if SHOW_GAMES_idx > 0 :
                    nextFirstLetter = current_game_list[SHOW_GAMES_idx - 1][0][0].upper()
                else:
                    nextFirstLetter = current_game_list[len(current_game_list) - 1][0][0].upper()

                if(currentFirstLetter != nextFirstLetter):
                    if (cptLetterChange >= 2):
                        notFound = False
                    cptLetterChange += 1
                if(old_SHOW_GAMES_idx == SHOW_GAMES_idx):
                    notFound = False
                elif(cptLetterChange < 2):
                    if SHOW_GAMES_idx == 0:
                        SHOW_GAMES_idx = len(current_game_list) - 1
                    else:
                        SHOW_GAMES_idx -= 1
            lcd.clear()
            show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_UPLOAD_DEFAULT:
            lcd.clear()
            if len(current_game_list[SHOW_GAMES_idx][1][SYSTEMS]) > 0:
                lcd.message(LABELS[LANGUAGE][CONNECTING])
                try:
                    triforcetools.connect(get_ip_for_system(current_game_list[SHOW_GAMES_idx][1][SYSTEMS][0]), 10703)
                except:
                    lcd.clear()
                    lcd.message(LABELS[LANGUAGE][CONNECT_FAILED])
                    sleep(SLEEP_AFTER_MESSAGE)
                    lcd.clear()
                    show_game(current_game_list[SHOW_GAMES_idx])
                    continue
                lcd.clear()
                lcd.message(LABELS[LANGUAGE][SENDING])
                lcd.setCursor(10, 0)
                lcd.ToggleBlink()
                triforcetools.HOST_SetMode(0, 1)
                triforcetools.SECURITY_SetKeycode("\x00" * 8)
                triforcetools.DIMM_UploadFile(ROM_DIR + current_game_list[SHOW_GAMES_idx][1][FILENAME])
                triforcetools.HOST_Restart()
                triforcetools.TIME_SetLimit(10*60*1000)
                triforcetools.disconnect()
                lcd.ToggleBlink()
                lcd.clear()
                lcd.message(LABELS[LANGUAGE][TRANSFER_COMPLETE])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                show_game(current_game_list[SHOW_GAMES_idx])
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_CHOOSE_SYSTEM_TO_UPLOAD:
            lcd.clear()
            if len(current_game_list[SHOW_GAMES_idx][1][SYSTEMS]) > 0:
                mode = CHOOSE_SYSTEM_TO_UPLOAD
                add_element_to_history(CHOOSE_SYSTEM_TO_UPLOAD)
                systems_for_the_game = current_game_list[SHOW_GAMES_idx][1][SYSTEMS]
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_RETURN:
            SHOW_GAMES_idx = 0
            SYSTEM_TO_UPLOAD_idx = 0
            lcd.clear()
            mode = go_back_to_history()
            if mode == TOP_VIEW:
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
            elif mode == VIEW_BY_SYSTEMS:
                lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
            elif mode == VIEW_BY_TYPES:
                lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
            elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
                show_game(current_game_list[SHOW_GAMES_idx])
            elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
            elif mode == CHOOSE_SYSTEM_TO_PING:
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            elif mode == UNKNOWN_ROMS:
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == SHOW_GAMES_RETURN_TOP_VIEW:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                TOP_VIEW_idx = 0
                SUB_CATEGORIES_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_UPLOAD_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                UNKNOWN_ROMS_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
        elif button == PING_SHORTCUT:
            lcd.clear()
            if len(SYSTEMS_FOR_UPLOAD) > 0:
                SUB_CATEGORIES_idx = 0
                TOP_VIEW_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_UPLOAD_idx = 0
                add_element_to_history(CHOOSE_SYSTEM_TO_PING)
                mode = CHOOSE_SYSTEM_TO_PING
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                show_game(current_game_list[SHOW_GAMES_idx])
        elif button == SHOW_GAMES_ADD_REMOVE_FAVORITES:
            if is_favorite_game(current_game_list[SHOW_GAMES_idx][1][FILENAME]):
                remove_favorite(current_game_list[SHOW_GAMES_idx])
                if mode == FAVORITES:
                    current_game_list = list_favorites
                    if current_game_list.get(GAMES) == None:
                        lcd.clear()
                        TOP_VIEW_idx = 0
                        SUB_CATEGORIES_idx = 0
                        SHOW_GAMES_idx = 0
                        SYSTEM_TO_UPLOAD_idx = 0
                        if nb_game_cat_in_top_view == 1:
                            lcd.message(LABELS[LANGUAGE][NOTHING_TO_SHOW])
                        else:
                            lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                            add_element_to_history(TOP_VIEW)
                            mode = TOP_VIEW
                    else:
                        current_game_list = list_favorites[GAMES]
                        if SHOW_GAMES_idx > 0:
                            SHOW_GAMES_idx -= 1
                        lcd.clear()
                        show_game(current_game_list[SHOW_GAMES_idx])
                else:
                    lcd.clear()
                    show_game(current_game_list[SHOW_GAMES_idx])
            else:
                add_favorite(current_game_list[SHOW_GAMES_idx])
                lcd.clear()
                show_game(current_game_list[SHOW_GAMES_idx])
    elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
        if button == CHOOSE_SYSTEM_TO_UPLOAD_NEXT_ITEM:
            if SYSTEM_TO_UPLOAD_idx == len(systems_for_the_game) - 1:
                SYSTEM_TO_UPLOAD_idx = 0
            else:
                SYSTEM_TO_UPLOAD_idx += 1
            lcd.clear()
            lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
        elif button == CHOOSE_SYSTEM_TO_UPLOAD_PREVIOUS_ITEM:
            if SYSTEM_TO_UPLOAD_idx == 0:
                SYSTEM_TO_UPLOAD_idx = len(systems_for_the_game) - 1
            else:
                SYSTEM_TO_UPLOAD_idx -= 1
            lcd.clear()
            lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
        elif button == CHOOSE_SYSTEM_TO_UPLOAD_SELECT:
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][CONNECTING])
            try:
                triforcetools.connect(get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]), 10703)
            except:
                lcd.clear()
                lcd.message(LABELS[LANGUAGE][CONNECT_FAILED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
                continue
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][SENDING])
            lcd.setCursor(10, 0)
            lcd.ToggleBlink()
            triforcetools.HOST_SetMode(0, 1)
            triforcetools.SECURITY_SetKeycode("\x00" * 8)
            triforcetools.DIMM_UploadFile(ROM_DIR + current_game_list[SHOW_GAMES_idx][1][FILENAME])
            triforcetools.HOST_Restart()
            triforcetools.TIME_SetLimit(10*60*1000)
            triforcetools.disconnect()
            lcd.ToggleBlink()
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][TRANSFER_COMPLETE])
            sleep(SLEEP_AFTER_MESSAGE)
            lcd.clear()
            lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
        elif button == CHOOSE_SYSTEM_TO_UPLOAD_RETURN:
            SYSTEM_TO_UPLOAD_idx = 0
            lcd.clear()
            mode = go_back_to_history()
            if mode == TOP_VIEW:
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
            elif mode == VIEW_BY_SYSTEMS:
                lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
            elif mode == VIEW_BY_TYPES:
                lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
            elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
                show_game(current_game_list[SHOW_GAMES_idx])
            elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
            elif mode == CHOOSE_SYSTEM_TO_PING:
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            elif mode == UNKNOWN_ROMS:
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx])) 
        elif button == CHOOSE_SYSTEM_TO_UPLOAD_RETURN_TOP_VIEW:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                TOP_VIEW_idx = 0
                SUB_CATEGORIES_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_UPLOAD_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                UNKNOWN_ROMS_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
        elif button == PING_SHORTCUT:
            lcd.clear()
            if len(SYSTEMS_FOR_UPLOAD) > 0:
                add_element_to_history(CHOOSE_SYSTEM_TO_PING)
                mode = CHOOSE_SYSTEM_TO_PING
                SYSTEM_TO_PING_idx = 0
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
    elif mode == CHOOSE_SYSTEM_TO_PING:
        if button == PING_NEXT_ITEM:
            lcd.clear()
            if SYSTEM_TO_PING_idx == len(SYSTEMS_FOR_UPLOAD) - 1:
                SYSTEM_TO_PING_idx = 0
            else:
                SYSTEM_TO_PING_idx += 1
            lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
        elif button == PING_PREVIOUS_ITEM:
            lcd.clear()
            if SYSTEM_TO_PING_idx == 0:
                SYSTEM_TO_PING_idx = len(SYSTEMS_FOR_UPLOAD) - 1
            else:
                SYSTEM_TO_PING_idx -= 1
            lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
        elif button == PING_SELECT:
            lcd.clear()
            lcd.message(LABELS[LANGUAGE][PINGING] + "\n" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0])
            sleep(SLEEP_AFTER_MESSAGE)
            response = os.system("ping -c 1 " + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1])
            lcd.clear()
            if response == 0:
                lcd.message(LABELS[LANGUAGE][PING_SUCCESS])
            else:
                lcd.message(LABELS[LANGUAGE][PING_FAILED])
            sleep(SLEEP_AFTER_MESSAGE)
            lcd.clear()
            lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
        elif button == PING_RETURN:
            SYSTEM_TO_PING_idx = 0
            lcd.clear()
            mode = go_back_to_history()
            if mode == TOP_VIEW:
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
            elif mode == VIEW_BY_SYSTEMS:
                lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
            elif mode == VIEW_BY_TYPES:
                lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
            elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
                show_game(current_game_list[SHOW_GAMES_idx])
            elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
            elif mode == CHOOSE_SYSTEM_TO_PING:
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            elif mode == UNKNOWN_ROMS:
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == PING_RETURN_TOP_VIEW:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                TOP_VIEW_idx = 0
                SUB_CATEGORIES_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_PING_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
        elif button == PING_SHORTCUT:
            lcd.clear()
            # No need for test here :)
            mode = CHOOSE_SYSTEM_TO_PING
            SYSTEM_TO_PING_idx = 0
            lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
    elif mode == UNKNOWN_ROMS:
        if button == UNKNOWN_ROMS_NEXT_ITEM:
            lcd.clear()
            if UNKNOWN_ROMS_idx == len(list_unknown_roms) - 1:
                UNKNOWN_ROMS_idx = 0
            else:
                UNKNOWN_ROMS_idx += 1
            lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == UNKNOWN_ROMS_PREVIOUS_ITEM:
            lcd.clear()
            if UNKNOWN_ROMS_idx == 0:
                UNKNOWN_ROMS_idx = len(list_unknown_roms) - 1
            else:
                UNKNOWN_ROMS_idx -= 1
            lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == UNKNOWN_ROMS_SELECT:
            lcd.clear()
            if len(game_without_rom) > 0:
                add_element_to_history(UNKNOWN_ROMS_CHOOSE_GAME)
                mode = UNKNOWN_ROMS_CHOOSE_GAME
                lcd.message(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx])
            else:
                lcd.message(LABELS[LANGUAGE][NO_ORPHAN_GAMES])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == UNKNOWN_ROMS_RETURN:
            UNKNOWN_ROMS_idx = 0
            lcd.clear()
            mode = go_back_to_history()
            if mode == TOP_VIEW:
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
            elif mode == VIEW_BY_SYSTEMS:
                lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
            elif mode == VIEW_BY_TYPES:
                lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
            elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
                show_game(current_game_list[SHOW_GAMES_idx])
            elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
            elif mode == CHOOSE_SYSTEM_TO_PING:
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            elif mode == UNKNOWN_ROMS:
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == UNKNOWN_ROMS_RETURN_TOP_VIEW:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                UNKNOWN_ROMS_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                TOP_VIEW_idx = 0
                SUB_CATEGORIES_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_PING_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
        elif button == PING_SHORTCUT:
            if len(SYSTEMS_FOR_UPLOAD) > 0:
                add_element_to_history(CHOOSE_SYSTEM_TO_PING)
                mode = CHOOSE_SYSTEM_TO_PING
                SYSTEM_TO_PING_idx = 0
                UNKNOWN_ROMS_idx = 0
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
    elif mode == UNKNOWN_ROMS_CHOOSE_GAME:
        if button == UNKNOWN_ROMS_CHOOSE_GAME_NEXT_GAME:
            if UNKNOWN_ROMS_CHOOSE_GAME_idx == len(game_without_rom) - 1:
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
            else:
                UNKNOWN_ROMS_CHOOSE_GAME_idx += 1
            lcd.clear()
            lcd.message(get_string_for_display(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx]))
        elif button == UNKNOWN_ROMS_CHOOSE_GAME_PREVIOUS_GAME:
            if UNKNOWN_ROMS_CHOOSE_GAME_idx == 0:
                UNKNOWN_ROMS_CHOOSE_GAME_idx = len(game_without_rom) - 1
            else:
                UNKNOWN_ROMS_CHOOSE_GAME_idx -= 1
            lcd.clear()
            lcd.message(get_string_for_display(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx]))
        elif button == UNKNOWN_ROMS_CHOOSE_GAME_NEXT_LETTER:
            if UNKNOWN_ROMS_CHOOSE_GAME_idx == 0:
                old_UNKNOWN_ROMS_CHOOSE_GAME_idx = len(game_without_rom) - 1
            else:
                old_UNKNOWN_ROMS_CHOOSE_GAME_idx = UNKNOWN_ROMS_CHOOSE_GAME_idx - 1
            
            notFound = True
            while(notFound):
                currentFirstLetter = game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx][0].upper()
                if UNKNOWN_ROMS_CHOOSE_GAME_idx < len(game_without_rom) - 1:
                    nextFirstLetter = game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx + 1][0].upper()
                else:
                    nextFirstLetter = game_without_rom[0][0].upper() 
                        
                if(currentFirstLetter != nextFirstLetter or old_UNKNOWN_ROMS_CHOOSE_GAME_idx == UNKNOWN_ROMS_CHOOSE_GAME_idx):
                    notFound = False
                
                if (old_UNKNOWN_ROMS_CHOOSE_GAME_idx != UNKNOWN_ROMS_CHOOSE_GAME_idx):
                    if (UNKNOWN_ROMS_CHOOSE_GAME_idx == len(game_without_rom) - 1):
                        UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                    else:
                        UNKNOWN_ROMS_CHOOSE_GAME_idx += 1  
            lcd.clear()
            lcd.message(get_string_for_display(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx]))
        elif button == UNKNOWN_ROMS_CHOOSE_GAME_PREVIOUS_LETTER:
            if UNKNOWN_ROMS_CHOOSE_GAME_idx == len(game_without_rom) - 1:
                old_UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
            else:
                old_UNKNOWN_ROMS_CHOOSE_GAME_idx = UNKNOWN_ROMS_CHOOSE_GAME_idx + 1
            
            notFound = True
            cptLetterChange = 0
            while(notFound or forceExitLoop):
                currentFirstLetter = game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx][0].upper()
                if UNKNOWN_ROMS_CHOOSE_GAME_idx > 0 :
                    nextFirstLetter = game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx - 1][0].upper()
                else:
                    nextFirstLetter = game_without_rom[len(game_without_rom) - 1][0].upper() 
                        
                if(currentFirstLetter != nextFirstLetter):
                    if (cptLetterChange >= 2):
                        notFound = False
                    cptLetterChange += 1
                if (old_UNKNOWN_ROMS_CHOOSE_GAME_idx == UNKNOWN_ROMS_CHOOSE_GAME_idx):
                    notFound = False
                elif (cptLetterChange < 2):
                    if UNKNOWN_ROMS_CHOOSE_GAME_idx == 0:
                        UNKNOWN_ROMS_CHOOSE_GAME_idx = len(game_without_rom) - 1
                    else:
                        UNKNOWN_ROMS_CHOOSE_GAME_idx -= 1          
            lcd.clear()
            lcd.message(get_string_for_display(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx]))
        elif button == UNKNOWN_ROMS_CHOOSE_GAME_SELECT_GAME:
            lcd.clear()
            rename_rom(UNKNOWN_ROMS_idx, UNKNOWN_ROMS_CHOOSE_GAME_idx)
            list_unknown_roms.pop(UNKNOWN_ROMS_idx)
            game_without_rom.pop(UNKNOWN_ROMS_CHOOSE_GAME_idx)
            lcd.message(LABELS[LANGUAGE][ROM_RENAMED])
            TOP_VIEW_idx = 0
            SUB_CATEGORIES_idx = 0
            SHOW_GAMES_idx = 0
            SYSTEM_TO_UPLOAD_idx = 0
            create_lists()
            sleep(SLEEP_AFTER_MESSAGE)
            lcd.clear()
            if len(list_unknown_roms) > 0:
                if UNKNOWN_ROMS_idx > 0:
                    UNKNOWN_ROMS_idx -= 1
                mode = UNKNOWN_ROMS
                add_element_to_history(UNKNOWN_ROMS)
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
            else:
                TOP_VIEW_idx = 0
                mode = TOP_VIEW
                add_element_to_history(TOP_VIEW)
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                UNKNOWN_ROMS_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
        elif button == UNKNOWN_ROMS_CHOOSE_GAME_RETURN:
            UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
            lcd.clear()
            mode = go_back_to_history()
            if mode == TOP_VIEW:
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
            elif mode == VIEW_BY_SYSTEMS:
                lcd.message(LABELS[LANGUAGE][GAMES_SYSTEMS[SUB_CATEGORIES_idx]])
            elif mode == VIEW_BY_TYPES:
                lcd.message(LABELS[LANGUAGE][GAMES_TYPES[SUB_CATEGORIES_idx]])
            elif mode == VIEW_ALL_GAMES or mode == SHOW_GAMES or mode == FAVORITES:
                show_game(current_game_list[SHOW_GAMES_idx])
            elif mode == CHOOSE_SYSTEM_TO_UPLOAD:
                lcd.message(systems_for_the_game[SYSTEM_TO_UPLOAD_idx] + "\n(" + get_ip_for_system(systems_for_the_game[SYSTEM_TO_UPLOAD_idx]) + ")")
            elif mode == CHOOSE_SYSTEM_TO_PING:
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            elif mode == UNKNOWN_ROMS:
                lcd.message(get_string_for_display(list_unknown_roms[UNKNOWN_ROMS_idx]))
        elif button == UNKNOWN_ROMS_CHOOSE_GAME_RETURN_TOP_VIEW:
            if (nb_game_cat_in_top_view == 1 and CHOOSE_SYSTEM_TO_PING in VIEWS) or (nb_game_cat_in_top_view > 1):
                lcd.clear()
                TOP_VIEW_idx = 0
                SUB_CATEGORIES_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_UPLOAD_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                UNKNOWN_ROMS_idx = 0
                lcd.message(LABELS[LANGUAGE][VIEWS[TOP_VIEW_idx]])
                add_element_to_history(TOP_VIEW)
                mode = TOP_VIEW
        elif button == PING_SHORTCUT:
            lcd.clear()
            if len(SYSTEMS_FOR_UPLOAD) > 0:
                SUB_CATEGORIES_idx = 0
                TOP_VIEW_idx = 0
                SHOW_GAMES_idx = 0
                SYSTEM_TO_UPLOAD_idx = 0
                UNKNOWN_ROMS_idx = 0
                UNKNOWN_ROMS_CHOOSE_GAME_idx = 0
                add_element_to_history(CHOOSE_SYSTEM_TO_PING)
                mode = CHOOSE_SYSTEM_TO_PING
                lcd.message(SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][0] + "\n(" + SYSTEMS_FOR_UPLOAD[SYSTEM_TO_PING_idx][1] + ")")
            else:
                lcd.message(LABELS[LANGUAGE][NO_SYSTEM_DEFINED])
                sleep(SLEEP_AFTER_MESSAGE)
                lcd.clear()
                lcd.message(get_string_for_display(game_without_rom[UNKNOWN_ROMS_CHOOSE_GAME_idx]))

