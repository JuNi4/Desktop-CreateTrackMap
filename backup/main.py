import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, time, numpy as np, copy, toolBar, ptd, configparser, shutil, log, webbrowser, hover
from map import CreateTrackMapApi
import map.tracks as map_tracks, map.signals as map_signals, map.trains as map_trains, map.stations  as map_stations, map.portals as map_portals

# TODO: implement hover and click for stations, trains and portals
# TODO: ( WIP ) Make blocked segments show

# TODO: Make Coords show

# TODO: improve icon draw programm
# TODO: (Maybe) Create icon creator

# TODO: Improve performance

# TODO: Make trains look proper (Done for now, might be worth improving later)

# a list of all color aliases
colors = {
    "white": "#ffffff",
    "black": "#000000",

    "red": "#ff0000",
    "yellow": "#ffff00",
    "green": "#00ff00",
    "cyan": "#00FFFF",
    "blue": "#0000ff",
    "magenta": "#ff00ff",

    "purple": "#800080",
    "pink": "#FFC0CB",
    "plum": "#C2938D"
}

def hexToRGB(hexCode):
    # replace semicolon with nothing
    hexCode = hexCode.replace(";","")

    # if hexCode is a color alias, convert it
    if hexCode in colors:
        hexCode = colors[hexCode]

    # try convert hex to rgb
    try:
        return tuple(int(hexCode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    except Exception as e:
        log.log(log.sys,e,log.col_red)
        return (0,0,0)

def assembleTrainStationChildren(tracks, trains):
    global bar
    # list for children
    train_list = []
    station_list = []

    # add all trains
    for o in trains["trains"]:
        train_list.append(o)

    # add all stations
    for o in tracks["stations"]:
        station_list.append(o)

    # update toolbar things
    bar.updateButton("trains",children=train_list)
    bar.updateButton("stations",children=station_list)

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

; Config for the api
[API]
    ; The api for the create track map
    ; Default: "http://localhost:3876"
ctm = http://localhost:3876
    ; The level of detail, decides what contents get stripped from the offline storage
    ; Example: "medium" will show everything except blocked signals and trains while "off" will show nothing
    ; Default: "medium", other options are "full", "low" and "off"
storage_lod = medium
    ; The path for the local storage for the api
    ; Default: "{PATH}/api"
storage = {PATH}/api
    ; The time inbetween each request, lower number means more updates. WARNING: If it's too low, it might cause the api to crash
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

try:
    API_POLL_RATE = float(config_api["poll_rate"])
except:
    log.log(log.api, "[FATAL ERROR] Poll intervall is not a valid number!", log.col_red)

log.log(log.sys,"Setting up API")
log.log(log.api,f"Setting offline path to '{PATH}/api'")
## Seutp API
log.log(log.api,f"URL set to {URL}")
api = CreateTrackMapApi.mapAPI(URL,API_OFFLINE_PATH,API_OFFLINE_MODE)

# get config
config = api.getConfig()
if config == {}:
    log.log(log.api,"[FATAL ERROR] API could not be reached. Please make sure the correct url is set in the config and you have a working internet connection",log.col_red)
    exit()
# get cam position
cam = config["view"]["initial_position"]
cam = cam["x"], cam["z"]
dimension = config["view"]["initial_dimension"]
# get style sheet
style = api.getStyleAsJson()
# get all colors
background = hexToRGB(style["map-background"])
track_occupied = hexToRGB(style["track-occupied"])
track_reserved = hexToRGB(style["track-reserved"])
track_free = hexToRGB(style["track-free"])
signal_green = hexToRGB(style["signal-green"])
signal_yellow = hexToRGB(style["signal-yellow"])
signal_red = hexToRGB(style["signal-red"])
signal_outline = hexToRGB(style["signal-outline"])
portal_color = hexToRGB(style["portal-color"])
portal_outline = hexToRGB(style["portal-outline"])
station_color = hexToRGB(style["station-color"])
station_outline = hexToRGB(style["station-outline"])
train_color = hexToRGB(style["train-color"])
lead_car_color = hexToRGB(style["lead-car-color"])

line_thickness = 2

signal_size = 3
signal_border_size = 0.5

train_size = 4

station_size = 3
station_line_thickness = 1

# get all network data
tracks = api.getTracks()
blocks = api.getBlocks()
signals = api.getSignals()
trains = api.getTrains()

#with open("config.json","w") as f:
#    import json
#    json.dump(config,f,indent=4)

fast = False # disables bezier curves

log.log(log.sys,"Launching Create Track Map")
## Pygame Seutp
pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([500, 500], pygame.RESIZABLE)
# set title
pygame.display.set_caption(TITLE)
# exit variable
done = False

# create font
# create font
FONT = pygame.font.SysFont(None, 20)

# how often the api will be called
callInterval = API_POLL_RATE # seconds
last = time.time()

# delta time
deltaTime = 0
start = time.time()

# cam movement
cam_v = [0,0]
v = 200

cam_final = cam

w, h = screen.get_size()
cam_offset = (w/2,h/2)
#cam_offset = (0,0)

# zoom variables
zoom = 1
zoom_v = 0.1

# mouse to cam movement variables
Mstart_position = (0,0)
mouse_move = False
old_cam = cam

# create toolbar
bar = toolBar.toolBar(screen, FONT)

## add all buttons
# layer backup for later
layer_backup = {}
# add all layers
child = []
tmp_layers = config["layers"]
layers = {}
for o in tmp_layers:
    layers[o] = o != "blocks"
    if layers[o]:
        name = "x "+tmp_layers[o]["label"]
    else:
        name = "  "+tmp_layers[o]["label"]
    child.append({"id":o,"name":name})
bar.addButton("view","View",child)

bar.addButton("trains","Trains",[])
bar.addButton("stations","Stations",[])
# add all stations and trains
assembleTrainStationChildren(tracks, trains)

# add all dimensions
dims = [{"id":"reset","name":"Reset View"}]
for o in config["dimensions"]:
    dims.append({"id":o,"name":config["dimensions"][o]["label"]})
# navigation button for going to other dimensions
bar.addButton("nav","Navigation",dims)
# about menu
bar.addButton("about","About",[{"id":"browser","name":"Open in Browser"},{"id":"about","name":"About"},{"id":"help","name":"Help"}])

# update layers when corrosponding view button was clicked
@bar.onButtonClick(parent="view")
def updateView(id):
    # get all layers
    global layers
    # get subid of button
    subid = id.split(".")[1]
    # toggle thing
    layers[subid] = not layers[subid]
    log.log(log.view,f"Toggled {id} to {str(layers[subid])}")
    # find correct button in children
    for i in range(len(child)):
        if child[i]["id"] == subid:
            if layers[subid]:
                child[i]["name"] = "x"+child[i]["name"][1:]
            else:
                child[i]["name"] = " "+child[i]["name"][1:]
    # udate title
    bar.updateButton(id, "View",child)

# if a train was clicked, move camera to it
@bar.onButtonClick(parent="trains")
def gotoTrain(id):
    # get global vars
    global cam
    # get subid
    subid = id.split(".")[1]
    # get train data
    for o in trains["trains"]:
        # see if trains has the same id
        if o["id"] == subid:
            break

    log.log(log.nav,"Jumped to train "+o["name"])
    
    # get car position
    pos = o["cars"][0]["leading"]["location"]
    pos = -pos["x"], -pos["z"]

    cam = pos
        
# if a station was clicked, move camera to it
@bar.onButtonClick(parent="stations")
def gotoTrain(id):
    # get global vars
    global cam
    # get subid
    subid = id.split(".")[1]
    # get train data
    for o in tracks["stations"]:
        # see if trains has the same id
        if o["id"] == subid:
            break

    log.log(log.nav,"Jumped to station "+o["name"])
    # get car position
    pos = o["location"]
    pos = -pos["x"], -pos["z"]

    cam = pos

# if about is clicked, show about screen
@bar.onButtonClick(id="about.about")
def show_about(id):
    # print status
    log.log(log.scene,"Going to about screen")
    # get variables
    global SCENE
    global S_ABOUT
    global layers
    global layer_backup

    # make deep copy of layers
    layer_backup = copy.deepcopy(layers)

    # set all layers to off
    for o in layers:
        layers[o] = False

    # set SCENE to about
    SCENE = S_ABOUT

# if the open in browser button was pressed
@bar.onButtonClick("about.browser")
def openInBrowser(id):
    log.log(log.sys,f"Opening Website for Create Track Map (at {URL})")
    # open the website
    webbrowser.open(URL, new=0, autoraise=True)

# reset the camera view
@bar.onButtonClick("nav.reset")
def resetView(id):
    global cam
    global zoom
    global dimension
    # get inital position
    pos = config["view"]["initial_position"]
    # set cam to it
    cam = pos["x"], pos["z"]
    # reset zoom
    zoom = 1
    # reset dimension
    dimension = config["view"]["initial_dimension"]

    # print action
    log.log(log.nav,"Resetted view")

# move to a new dimension
@bar.onButtonClick(parent="nav")
def navigation(id):
    if id == "nav.reset": return
    # get subid
    subid = id.split(".")[1]
    # dimension variable
    global dimension

    dimension = subid

    # print action
    log.log(log.nav,"Switched to dimension " + subid)

## scene setup
# scene selector, possible ["MAP","ABOUT"]
SCENE = "MAP"
S_ABOUT = "ABOUT"
S_MAP = "MAP"

## about screen details
about_msg = "Create Track Map\nby JuNi (https://github.com/juni4)\n\nBased on the Create Track Map mod for Minecraft Forge\nby littlechasiu (https://modrinth.com/mod/create-track-map)\n\nA Map schowing the track layed in a minecraft world (Create Mod Tracks). It can also show all of the network activity on said tracks."
about_msg = ptd.text(screen,about_msg,FONT,(5,5),0)

## Layers
layer_track = None


try:
    ## main loop ##
    while not done:
        # calculate deltatime
        deltaTime = time.time() - start
        start = time.time()
        # event handler
        for event in pygame.event.get():
            # if quit event
            if event.type == pygame.QUIT:
                # quit
                log.log(log.sys,"Exiting...",log.col_yellow)
                done = True
                break
            # map events
            if SCENE == S_MAP:
                # tool bar event handler
                bar.eventHandler(event)
                # w,a,s,d down for cam controlls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        cam_v[1] += v
                    elif event.key == pygame.K_s:
                        cam_v[1] -= v
                    elif event.key == pygame.K_a:
                        cam_v[0] += v
                    elif event.key == pygame.K_d:
                        cam_v[0] -= v
                # w,a,s,d up for cam controlls
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        cam_v[1] -= v
                    elif event.key == pygame.K_s:
                        cam_v[1] += v
                    elif event.key == pygame.K_a:
                        cam_v[0] -= v
                    elif event.key == pygame.K_d:
                        cam_v[0] += v
                # mouse wheel for zoom
                elif event.type == pygame.MOUSEWHEEL:
                    #print(event.x, event.y)
                    zoom += event.y * zoom_v
                    if zoom < 0: zoom = 0
                # mouse down for moving map
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_move = True
                        Mstart_position = pygame.mouse.get_pos()
                        old_cam = copy.deepcopy(cam)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_move = False

            # about screen evetns
            elif SCENE == S_ABOUT:
                if event.type == pygame.KEYDOWN:
                    # if escape was pressed
                    if event.key == pygame.K_ESCAPE:
                        # return to map
                        SCENE = S_MAP
                        layers = layer_backup
                        log.log(log.scene,"Going to map screen")
                        # reset mouse movement
                        mouse_move = False

        ## set beckground color
        screen.fill(background)

        ## display things ##
        if SCENE == S_MAP:
            # move camera to mouse difference
            if mouse_move:
                delta = np.divide(np.subtract(pygame.mouse.get_pos(),Mstart_position),zoom)
                cam = np.add(old_cam,delta)
                pygame.mouse.set_cursor(6)
            else:
                pygame.mouse.set_cursor(11)

            # recalucalte cams
            cam = np.add(cam, np.multiply(cam_v,deltaTime))
            # recalculate cam offset
            screen_size = screen.get_size()
            cam_offset = np.divide(screen_size,2)
            # final camera values for further math
            cam_final = np.multiply(cam,zoom)

            # if callInterval seconds have past, call api
            if time.time() - last >= callInterval:
                #print("Calling API")
                tracks = api.getTracks()
                blocks = api.getBlocks()
                signals = api.getSignals()
                trains = api.getTrains()
                last = time.time()
                # add all stations and trains to toolbar
                assembleTrainStationChildren(tracks, trains)

            ## MAP
            # draw tracks
            if layer_track == None:
                tmp_cam = cam, cam_final, cam_offset, screen_size, dimension, mouse_move
                tmp_style = track_free, line_thickness, fast
                map_tracks.drawTracks(screen, tracks, layers, zoom, tmp_cam, tmp_style)

            # draw signals (WIP)
            tmp_style = signal_green, signal_yellow, signal_red, signal_outline, signal_size, signal_border_size
            tmp_cam = cam, cam_final, cam_offset, screen_size, dimension
            map_signals.drawSignals(screen, signals, layers, zoom, tmp_cam, tmp_style)

            # draw stations (WIP)
            tmp_cam = cam, cam_final, cam_offset, screen_size, dimension
            tmp_style = station_outline,station_color,station_size, station_line_thickness
            map_stations.drawStations(screen, tracks, layers, zoom, tmp_cam, tmp_style)

            # draw trains
            tmp_style = train_color, lead_car_color, train_size
            tmp_cam = cam, cam_final, cam_offset, dimension
            car = map_trains.drawTrains(screen,trains,layers, zoom, tmp_cam, tmp_style)

            # draw portals (WIP)
            tmp_style = portal_color, portal_outline, line_thickness
            tmp_cam = cam, cam_final, cam_offset, dimension
            map_portals.drawPortals(screen,tracks,layers,zoom,tmp_cam,tmp_style)
            

            # draw options bar
            bar.draw()

            train, id = car
            if train != {}:
                # draw name of station / portal
                hover.hoverText(screen, train["name"] + f" [{str(id)}]",(255,255,255),(0,0,0),np.add(pygame.mouse.get_pos(),(20,0)),FONT)

        # abbout screen
        elif SCENE == S_ABOUT:
            # get screen width
            w,h = screen_size
            # limit width of text
            about_msg.maxWidth = w-10
            about_msg.draw()

        ## Update Display
        pygame.display.update()

    # Quit pygame
    pygame.quit()
except KeyboardInterrupt:
    log.log(" "+log.sys,"Exiting...",log.col_yellow)