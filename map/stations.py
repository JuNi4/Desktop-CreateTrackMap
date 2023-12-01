import numpy as np
from ui import icon

station = {
    "layers": [
        {"type":"polygons","polygons":[
            {"p":[(1,1),(1,-1),(-1,-1),(-1,1)],"col":1},
        ]},
        {"type":"paths","paths": [
            {"from":(1,1),"to":(-1,1),"col":0},
            {"from":(-1,1),"to":(-1,-1),"col":0},
            {"from":(-1,-1),"to":(1,-1),"col":0},
            {"from":(1,-1),"to":(1,1),"col":0}
        ]},
        {"type":"paths","paths": [
            {"from":(0,.6),"to":(0,-.6),"col":0},
            {"from":(.6,.6),"to":(-.6,.6),"col":0},
            {"from":(0,.6),"to":(.6,0),"col":0},
            {"from":(0,.6),"to":(-.6,0),"col":0}
        ]}
    ]
}

def drawStations(screen, tracks, layers, zoom, cam, style):
    # get all variables
    cam, cam_final, cam_offset, screen_size, dimension = cam
    station_outline,station_color,station_size,line_thickness = style
    
    # only continue if tracks are visible
    if not layers["stations"]: return
    
    # draw tracks
    for o in tracks["stations"]:
        # skip station if not in current dimension
        if o["dimension"] != dimension: continue
        # get position of station
        location = o["location"]
        pos = location["x"], location["z"]

        # get window size
        screen.get_size()
        # check if track is on screen
        on_screen = False
        pos = np.add(np.multiply(pos,zoom), np.add(cam_final,cam_offset))
        if not (np.greater(screen_size,pos).all() and np.greater(pos,(0,0)).all()):
            continue
        
        # draw code
        icon.drawIcon(screen,pos,o["angle"],station_size*zoom,[station_outline,station_color],(line_thickness-1)*zoom + 1,station)