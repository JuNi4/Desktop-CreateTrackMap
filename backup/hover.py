import pygame, numpy as np

# padding around the text
padding = 5

def hoverText(screen: pygame.surface.Surface, text:str, col:tuple, outline_col:tuple, pos:tuple, font:pygame.font.Font):
    # rendet text
    rtext = font.render(text,True,col)
    # draw outline around text
    w,h = np.add(rtext.get_size(),padding*2)

    # add padding to w,h and x,y
    x,y = np.subtract(pos,padding)

    # draw outline
    pygame.draw.rect(screen,outline_col,pygame.Rect(x,y,w,h))
    
    # draw text
    screen.blit(rtext,pos)