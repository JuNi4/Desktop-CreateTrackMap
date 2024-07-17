from numpy import Infinity
import pygame
from vector import vec2

class Chunks:

    # create buffer for storing the induvidual chunks
    buffer:dict = {}
    # lowest x,y values (chunk sized)
    min = vec2(999999999999999,999999999999999)

    ## Chunks object constructor
    def __init__( self, ppc:int=500, clearColor:tuple=(0,0,0) ) -> None:
        # number of pixels per chunk
        self.ppc = ppc

        # clear color for the chunks
        self.clearCol = clearColor

    # creat all chunks in a square from an area
    def createChunks(self, min:vec2, max:vec2) -> None:
        # get size of the rect
        size = max - min

        # loop over all chunks
        for x in range(int(size.x / self.ppc)):
            self.buffer[x] = {}
            for y in range(int(size.y / self.ppc)):
                self.buffer[x][y] = self.newChunk()

        self.min = min / self.ppc

    # create a single new chunk
    def newChunk(self):

        chunk = pygame.Surface((self.ppc, self.ppc))
        chunk.fill(self.clearCol)

        return chunk

    # draw a chunk
    def drawChunk( self, screen:pygame.surface.Surface, cp:vec2, p:vec2, scale:int=1 ):
        # get the chunk
        cp = cp.int()
        print(cp)
        if cp.x in self.buffer and cp.y in self.buffer[cp.x]:
            chunk = self.buffer[cp.x][cp.y]
        else: return

        # scale the chunk
        zoom = (self.ppc*scale,self.ppc*scale)
        scaled_chunk = pygame.surface.Surface(zoom)
        pygame.transform.scale(chunk,zoom,scaled_chunk)

        # draw the chunk
        screen.blit(scaled_chunk,p.tuple())

    def drawLine(self, color, p1, p2, size):
        # draw a line in all the chunks but offset
        for cx in self.buffer:
            for cy in self.buffer[cx]:
                ## calculate offsets
                # chunk starting pos)
                cp = ( vec2(cx,cy) + self.min ) * self.ppc

                # subtract the starting positions form the points
                p1 -= cp
                p2 -= cp

                # draw the line
                pygame.draw.line(self.buffer[cx][cy], color, p1.tuple(), p2.tuple(), size )

    # calculate where the track will be in which chunk
    # returns chunk x and y
    def chunkPos( self, p:vec2 ) -> vec2:

        cp = ( p / self.ppc ).int()

        return cp

    def posInChunk( self, x,y ):

        xinChunk = x % self.ppc
        yinChunk = y % self.ppc

        return ( xinChunk, yinChunk )
