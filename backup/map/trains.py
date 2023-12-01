import pygame, numpy as np, time

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

            # draw a line between the points
            pygame.draw.line(screen,train_color,fpos,bpos,int((train_size-1)*zoom+1))

            # get width and height
            x,y = fpos
            w,h = np.subtract(bpos,fpos)
            # clamp width and height
            if not w < 0:
                if w < train_size: w = train_size*zoom #not w < 0 and
            else:
                if w > -train_size: w = -train_size*zoom
                x += w
                w = abs(w)
            #elif w > -train_size: w = -train_size*zoom
            if not h < 0:
                if h < train_size: h = train_size*zoom
            else:
                if h > -train_size: h = -train_size*zoom
                y += h
                h = abs(h)
            #elif h > -train_size: h = -train_size*zoom

            # compensate for the coordinates being centered vertically
            if h == 4:
                #print(o["name"],time.time())
                y -= h/2
            else:
                x -= w/2

            #pygame.draw.rect(screen,(0,0,255),pygame.Rect(x,y,w,h))
            # get mouse position
            mx,my = pygame.mouse.get_pos()
            # check if mouse is over card
            if w+x > mx > x and h+y > my > y:
                out = o,car["id"]

    return out