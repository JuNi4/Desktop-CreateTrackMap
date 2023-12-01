#import pygame, numpy as np, time
from ui import bezier
from chunks import Chunks
from vector import vec2,tuple2vec2 as t2v2

# calculate where the track will be in which chunk
def chunkPos(x,y):

    # how many blocks per chunk
    scale = 500

    chunkX = x // scale
    chunkY = y // scale

    xinChunk = x % scale
    yinChunk = y % scale

    return xinChunk,yinChunk,chunkX,chunkY

def drawTracks(tracks, layers, dimension, style) -> Chunks:

    track_free, line_thickness, bg = style
    # create chunk storage
    chunks = Chunks(clearColor=bg)
    # create all chunks nessecary
    min = vec2()
    max = vec2()
    for o in tracks["tracks"]:
        if o["dimension"] != dimension: continue
        path = o["path"]
        for o in path:
            # check if point is more ore less than max or min
            p = vec2(o["x"], o["y"])
            if p > max: max = p
            elif p < min: min = p
        
    chunks.createChunks(min,max)

    # draw tracks
    for o in tracks["tracks"]:
        # skip track if not in current dimension
        if o["dimension"] != dimension: continue
        # get path of track
        path = o["path"]

        # color var
        col = track_free

        if len(path) > 2:# and not mouse_move and not fast:
            pts = []
            # assemble point list
            for o in path:
                pos = (o["x"], o["z"])
                pts.append(pos)
            # draw bezier curve
            bezier.bezier(chunks, pts, col, line_thickness, 0.1)
        elif len(path) < 2:
            for l in range(len(path)-1):
                start_pos = vec2(path[l]["x"], path[l]["z"])
                end_pos = vec2(path[l+1]["x"], path[l+1]["z"])
                # make a line from a to b
                chunks.drawLine(col, start_pos, end_pos, line_thickness )
        else:
            start_pos = vec2(path[0]["x"], path[0]["z"])
            end_pos = vec2(path[1]["x"], path[1]["z"])
            # make a line from a to b
            chunks.drawLine(col, start_pos, end_pos, line_thickness )

    return chunks