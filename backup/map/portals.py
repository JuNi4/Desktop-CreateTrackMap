import pygame, numpy as np

def drawPortals(screen, tracks, layers, zoom, cam, style):
    # get all variables
    cam, cam_final, cam_offset, dimension = cam
    portal_color, portal_outline, line_thickness = style
    
    screen_size = screen.get_size()

    # only continue if tracks are visible
    if not layers["portals"]: return
    
    # draw tracks
    for o in tracks["portals"]:
        # skip station if not in current dimension
        if o["from"]["dimension"] != dimension: continue
        # get position of station
        location = o["from"]["location"]
        pos = location["x"], location["z"]

        # get window size
        screen.get_size()
        # check if track is on screen
        on_screen = False
        pos = np.add(np.multiply(pos,zoom), np.add(cam_final,cam_offset))
        if not (np.greater(screen_size,pos).all() and np.greater(pos,(0,0)).all()):
            continue

        x,y = pos

        w,h = 6,6
        
        ## draw code
        #draw outline
        pygame.draw.rect(screen, portal_outline, pygame.Rect((x,y-h/2*zoom,w*zoom,h*zoom)), border_radius=2)
        # draw purply bits
        pos = ( x + 1*zoom, y + 1*zoom - h/2 * zoom, (w-2) * zoom, (h-2) * zoom )
        pygame.draw.rect(screen, portal_color, pygame.Rect(pos), border_radius=2)