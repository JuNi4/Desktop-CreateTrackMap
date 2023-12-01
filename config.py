import log, os, configparser, shutil

# get path to current
PATH = os.path.abspath(os.path.dirname(__file__))

# config file name
CONFIG_FILE_NAME = "config.ini"

# the config template
configfile = f"""
;  Offline Create Track Map Config
;   By JuNi (https://github.com/juni4)
; #-----------------------------------#

; Config for general stuff
[GENERAL]
    ; The title of the window
    ; Default: "Create Track Map"
title = Create Track Map
    ; The background image of the map, This will allow you to have an image of your minecraft map shown below the tracks
    ; Note: this is not propperly implemented yet
    ; Default: ""
background_img = 
    ; The color an error will appear in in the console
    ; Default: "{log.col_red}"
log_red = {log.col_red}
    ; The color a warning will appear in in the console
    ; Default: "{log.col_yellow}"
log_yellow = {log.col_yellow}
    ; The color an info will appear in in the console
    ; Default: "{log.col_blue}"
log_blue = {log.col_blue}
    ; The default font
    ; Default: "None"
font = None
    ; The default font size
    ; Default: 20
font_size = 20

; Config for the api
[API]
    ; The url to the create track map
    ; Default: "http://localhost:3876"
ctm = http://localhost:3876
    ; The level of detail, decides which content get stripped from the offline storage
    ; Example: "medium" will show everything except blocks, signals and trains while "off" will show nothing when the track map is unreachable
    ; Default: "medium", other options are "full", "low" and "off"
storage_lod = medium
    ; The path for the local storage for the api
    ; Can be used to have multiple worlds
    ; Default: "{PATH}/api"
storage = {PATH}/api
    ; The time inbetween each request in seconds, lower number means more updates
    ; WARNING: If the number is too low, it may cause the api to crash
    ; Default: "5"
poll_rate = 5
"""[1:] # [1:] ignores the first new line char

def config_create():
    # log creation of config file
    log.log(log.sys,"Creating config file")
    # write the config file
    with open(PATH+"/"+CONFIG_FILE_NAME, "w") as f:
        f.write(configfile)

# see if a config file exists
log.log(log.sys,"Checking for config file")
if not os.path.isfile(PATH+"/"+CONFIG_FILE_NAME):
    log.log(log.sys,"Config file not found, creating one",log.col_yellow)
    config_create()
    log.log(log.sys,"New Config file generated, don't forget to change the settings!",log.col_yellow)
    log.log(log.sys,"Exiting...",log.col_yellow)
    exit(0)

# log loading of config file
log.log(log.sys,"Loading config")
# load config file
config_file = configparser.ConfigParser()
config_file.read(PATH+"/"+CONFIG_FILE_NAME)

# get template config
config_template = configparser.ConfigParser()
config_good = True

# check if config file is good
for section in config_template.sections():
    # check if section exists
    if not section in config_file.sections():
        config_good = False
        break

    # check if all keys exist
    for key in config_template[section]:
        # check if key exists
        if not key in config_file[section]:
            config_good = False
            break

# check if a backup file exists
if os.path.isfile(PATH+"/"+CONFIG_FILE_NAME+".bak"):
    # print file contents
    log.log(log.sys,"The backup file will deleted now, here are its contents incase you need any:",log.col_yellow)
    print("'''")
    with open(PATH+"/"+CONFIG_FILE_NAME+".bak","r") as f:
        print(f.read())
    print("'''")
    # delete file
    os.remove(PATH+"/"+CONFIG_FILE_NAME+".bak")

# if the config is not good, create new
if not config_good:
    log.log(log.sys,"The config file was not up to date, updating. This will leave a copy of your old file",log.col_red)
    log.log(log.sys,"The backup file will be deleted after the next restart",log.col_yellow)
    shutil.copyfile(PATH+"/"+CONFIG_FILE_NAME, PATH+"/"+CONFIG_FILE_NAME+".bak")
    config_create()
    log.log(log.sys,"Exiting...",log.col_yellow)
    exit(0)

# get all settings necessary
config_api = config_file["API"]
config_general = config_file["GENERAL"]

# Get Variables from config #
# general
TITLE = config_general["title"]
log.col_red = config_general["log_red"]
log.col_yellow = config_general["log_yellow"]
log.col_blue = config_general["log_blue"]
# api
URL = config_api["ctm"]
API_OFFLINE_MODE = config_api["storage_lod"]
API_OFFLINE_PATH = config_api["storage"]