import pygame, numpy as np, bezier, time

def drawTracks(screen, tracks, layers, zoom, cam, style):
    # get all variables
    cam, cam_final, cam_offset, screen_size, dimension, mouse_move = cam
    track_free, line_thickness, fast = style

    # only continue if tracks are visible
    if not layers["tracks"]: return

    # draw tracks
    for o in tracks["tracks"]:
        # skip track if not in current dimension
        if o["dimension"] != dimension: continue
        # get path of track
        path = o["path"]

        # get window size
        screen.get_size()
        # check if track is on screen
        on_screen = False
        for o in path:
            pos = np.add(np.multiply((o["x"], o["z"]),zoom), np.add(cam_final,cam_offset))
            if np.greater(screen_size,pos).all() and np.greater(pos,(0,0)).all():
                on_screen = True

        if not on_screen: continue

        # color var
        col = track_free

        if len(path) > 2 and not mouse_move and not fast:
            pts = []
            # assemble point list
            for o in path:
                pos = np.add(np.multiply((o["x"], o["z"]),zoom), np.add(cam_final,cam_offset))
                pts.append(pos)
            # draw bezier curve
            bezier.bezier(screen, pts, col, int((line_thickness-1)*zoom + 1), 0.1)
        elif len(path) > 2:
            for l in range(len(path)-1):
                start_pos = np.add(np.multiply((path[l]["x"], path[l]["z"]),zoom), np.add(cam_final,cam_offset))
                end_pos = np.add(np.multiply((path[l+1]["x"], path[l+1]["z"]),zoom), np.add(cam_final,cam_offset))
                # make a line from a to b
                pygame.draw.line(screen, col, start_pos, end_pos, int((line_thickness-1)*zoom + 1) )
        else:
            start_pos = np.add(np.multiply((path[0]["x"], path[0]["z"]),zoom), np.add(cam_final,cam_offset))
            end_pos = np.add(np.multiply((path[1]["x"], path[1]["z"]),zoom), np.add(cam_final,cam_offset))
            # make a line from a to b
            pygame.draw.line(screen, col, start_pos, end_pos, int((line_thickness-1)*zoom + 1) )
