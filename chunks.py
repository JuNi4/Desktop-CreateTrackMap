import pygame
from vector import vec2

class Chunks:

    ## Chunks object constructor
    def __init__( s, ppc:int=500, clearColor:tuple=(0,0,0) ) -> None:
        # create buffer for storing the induvidual chunks
        s.buffer = []
        # lowest x,y values (chunk sized)
        min = 999999999999999999999999
        s.min = vec2(min,min)
        # number of pixels per chunk
        s.ppc = ppc

        # clear color for the chunks
        s.clearCol = clearColor

    # creates a blank chunk from chunk coordinates
    def _addChunk( s, cp:vec2 ):
        # get the index in the buffer
        # (pos - (xmin,ymin))
        p = cp - s.min

        # check if new regions have to be created ( bufferIndex < 0 )
        # do the min x chunks var
        if p.x < 0: s.min.x += p.x; p.x = 0
        # do the y chunks
        if p.y < 0:
            s.min.y += p.y
            # create new regions
            for i in range( abs(p.x + 1) ):
                s.buffer.insert( 0, [] )
            p.y = 0
        
        # create all the nessecary things
        for i in range( abs(p.x) - len( s.buffer[p.y] ) ):
            s.buffer[p.y].append( pygame.surface.Surface( (s.ppc,s.ppc) ) )
            s.buffer[p.y][i].fill(s.clearCol)

    def createChunks( s, p1:vec2, p2:vec2 ):
        r = (p2-p1).int()
        # create all chunks from p1 to p2
        for x in range( r.x ):
            for y in range( r.y ):
                s._addChunk( s.chunkPos( vec2(x,y) ) )

    def drawLine( s, color:vec2, p1:vec2, p2:vec2, size:int=1 ):
        # draw a line in all the chunks but offset
        for cy in range( len(s.buffer) ):
            for cx in range( len(s.buffer[cy]) ):
                ## calculate offsets
                # chunk starting pos)
                cp = ( vec2(cx,cy) + s.min ) * s.ppc
                
                # subtract the starting positions form the points
                p1 -= cp
                p2 -= cp

                # draw the line
                pygame.draw.line(s.buffer[cy][cx], color, p1.tuple(), p2.tuple(), size )

    # draw a chunk
    def drawChunk( s, screen:pygame.surface.Surface, cp:vec2, p:vec2, scale:int=1 ):
        # get the chunk
        cp = cp.int()
        chunk = s.buffer[cp.y][cp.x]

        # scale the chunk
        zoom = (s.ppc*scale,s.ppc*scale)
        scaled_chunk = pygame.surface.Surface(zoom)
        pygame.transform.scale(chunk,zoom,scaled_chunk)

        # draw the chunk
        screen.blit(scaled_chunk,p.tuple())

    # calculate where the track will be in which chunk
    # returns chunk x and y
    def chunkPos( s, p:vec2 ) -> vec2:
        
        cp = p // s.ppc

        return cp
        
    def posInChunk( s, x,y ):
        
        xinChunk = x % s.ppc
        yinChunk = y % s.ppc
        
        return ( xinChunk, yinChunk )