# Pygame Text Display
import pygame

class text:

    def __init__(self, screen:pygame.surface.Surface, text:str, font:pygame.font.Font, pos:tuple, maxWidth = -1):
        self.screen = screen

        self.text = text
        self.font = font
        self.pos = pos
        self.maxWidth = maxWidth

    def draw(self):
        # split the text
        text = self.text.split(" ")
        # position counters
        sx,sy = self.pos
        x, y = sx,sy

        padding = 5

        # reposition limit limits the amount of time a word can go to a new line
        reposition_limit = 2

        # go through all text elements and draw them
        for o in text:
            word = o.split("\n")
            for i in range(len(word)):
                # create text
                text = self.font.render(word[i],True,(255,255,255))
                # get text size
                tw,th = text.get_size()
                for i2 in range(reposition_limit):
                    # check if text exceeds max width
                    if x-sx + tw > self.maxWidth:
                        y += th + padding
                        x = sx
                        continue
                    
                    # if spot is free, place text
                    self.screen.blit(text,(x,y))

                    # increment x var
                    x += tw + padding

                    # if there is an element after the current, do a linebreak
                    if i < len(word)-1 > 0:
                        y += th + padding
                        x = sx
                    # go to next word
                    break