import pygame, numpy as np, time
from ui import icon
from math import *

wagon = """{
    "layers": [
        {"type":"polygons","polygons":[
            {"p":[(.5*length,-.5),(.5*length,.5),(-.5,.5),(-.5,-.5)],"col":0}
        ]}
    ]
}"""

lead = {
    "layers": [
        {"type":"polygons","polygons": [
            {"p":[(.5,0),(.25,-.25),(.5,.5),(0,.5),(0,0)],"col":0}
        ]}
    ]
}
    
def drawTrains(screen,trains,layers, zoom, cam, style):
    # get all variables
    train_color, leading_train_color, train_size = style
    cam, cam_final, cam_offset, dimension = cam
    # only continue if trains are visible
    if not layers["trains"]: return
    # variable for returning a train when hovered over
    out = ({},0)
    # draw trains
    for o in trains["trains"]:
        # go through all the cars
        for car in o["cars"]:
            # check for correct dimension
            if not (car["leading"]["dimension"] == dimension or car["trailing"]["dimension"] == dimension): continue

            # get position of front
            fpos = car["leading"]["location"]
            fpos = np.add(np.multiply((fpos["x"], fpos["z"]),zoom), np.add(cam_final,cam_offset))

            bpos = car["trailing"]["location"]
            bpos = np.add(np.multiply((bpos["x"], bpos["z"]),zoom), np.add(cam_final,cam_offset))

            # get the length of the carriege
            fx,fy = fpos
            bx,by = bpos

            a = bx - fx
            b = by - fy

            hyp = sqrt(a**2 + b**2)
            
            length = 0

            if fx == bx: length = by - fy
            elif fy == by: length = bx - fx
            else: length = hyp

            # stretch the wagon
            tmp_wagon = eval(wagon)

            # get the angle of the car
            icon.drawIcon(screen,fpos,degrees(asin(b/hyp)),1*train_size*zoom,[train_color,leading_train_color],icon=tmp_wagon)

    return out