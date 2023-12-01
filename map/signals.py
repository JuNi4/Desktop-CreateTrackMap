import numpy as np
from ui import icon

entry_signal_icon = {
    "layers": [
        {"type":"paths","paths": [
            {"from":(.5,0),"to":(1.5,0),"col":0},
            {"from":(1,0),"to":(1,.5),"col":0}
        ]},
        {"type":"circles","circles":[
            {"p":(1,.8),"r":.6,"w":0,"col":0},
            {"p":(1,.8),"r":.5,"w":0,"col":1}
        ]}
    ]
}

cross_signal_icon = {
    "layers": [
        {"type":"paths","paths": [
            {"from":(.5,0),"to":(1.5,0),"col":0},
            {"from":(1,0),"to":(1,.5),"col":0}
        ]},
        {"type":"polygons","polygons":[
            {"p":[(.5,.5),(1.5,.5),(1,1.5)],"col":0},
            {"p":[(.65,.65),(1.35,.65),(1,1.35)],"col":1},
        ]}
    ]
}

def drawSignals(screen, signals, layers, zoom, cam, style):
    # get all variables
    signal_green, signal_yellow, signal_red, signal_outline, signal_size, signal_border_size = style
    cam, cam_final, cam_offset, screen_size, dimension = cam

    # only continue if signals are visible
    if not layers["signals"]: return

    # draw all signals
    for o in signals["signals"]:
            # get position
            pos = o["location"]
            pos = np.add(np.multiply((pos["x"], pos["z"]),zoom), np.add(cam_final,cam_offset))
            # check for correct dimension
            if o["dimension"] != dimension: continue
            # check if signal is on screen
            if not (np.greater(screen_size,pos).all() and np.greater(pos,(0,0)).all()):
                continue
            
            # empty color
            col = (0,0,0)
            # signal type
            entry_signal = True
            # rotation of the signal
            rot = 0
            # get color of signal
            if o["reverse"] != None:
                #print(o["reverse"]["state"])
                if o["reverse"]["state"] == "GREEN": col = signal_green
                if o["reverse"]["state"] == "YELLOW": col = signal_yellow
                if o["reverse"]["state"] == "RED": col = signal_red
                entry_signal = o["reverse"]["type"] == "ENTRY_SIGNAL"
                # set rotation
                rot = o["reverse"]["angle"]
            elif o["forward"] != None:
                #print(o["forward"]["state"])
                if o["forward"]["state"] == "GREEN": col = signal_green
                if o["forward"]["state"] == "YELLOW": col = signal_yellow
                if o["forward"]["state"] == "RED": col = signal_red
                entry_signal = o["forward"]["type"] == "ENTRY_SIGNAL"
                # set rotation
                rot = o["forward"]["angle"]
            # if signal is not working
            else:
                continue
            if entry_signal:
                # draw entry signal
                icon.drawIcon(screen,pos,rot,signal_size*zoom,[signal_outline,col],signal_border_size*zoom,entry_signal_icon)
            else:
                # draw cross signal
                icon.drawIcon(screen,pos,rot,signal_size*zoom,[signal_outline,col],signal_border_size*zoom,cross_signal_icon)