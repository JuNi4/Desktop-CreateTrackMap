import pygame, os, sys, time

class toolBar:

    def __init__(self, screen:pygame.Surface, font, background = (0,0,0), highlight = (100,100,100)):
        self.screen = screen

        self.buttons = []

        self.col_background = background
        self.col_highlight = highlight

        self.height = 24

        self.font = font

        self.__listeners = []

        # in use vars
        self.__engaged = False
        self.__open_menu = None
        self.__current_children = {}
        self.__child_max_width = 0

        self.__events = []

    ## Event stuff
    # add listnerers
    def addListener(self,func, id, parent):
        if func in self.__listeners: return
        self.__listeners.append((func,id,parent))

    # event reciever
    #@property
    def onButtonClick(self, id=None,parent=None):
        def wrapper(func):
            self.addListener(func,id,parent)
            return func
        return wrapper

    def __trigger(self,id):
        # find correct function
        for o in self.__listeners:
            func, fid, fparent = o

            if fid == id or fid == "any" or id.split(".")[0] == fparent:
                func(id)
    
    ## Others
    # hover check
    @staticmethod
    def __hover_over( pos, mouse ):
        mouseX, mouseY = mouse
        posX, posY, w, h = pos
        # Check if mouse position is in position of button
        return ( mouseX > posX and mouseY > posY ) and ( mouseX < posX+w and mouseY < posY+h )
    
    # add a button
    def addButton(self, id, name, children):
        data = {"id":id,"name":name,"children":children}
        self.buttons.append(data)

    def updateButton(self, id, name="", children=[]):
        # find correct button
        for i in range(len(self.buttons)):
            if self.buttons[i]["id"] == id:
                # if name was not set, keep original
                if name == "":
                    name = self.buttons[i]["name"]
                # if child was not set, keep original
                if children == []:
                    children = self.buttons[i]["children"]
                # update button data
                self.buttons[i] = {"id":id,"name":name,"children":children}

    def eventHandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # continue if button is lmb
            if event.button == 1:
                # check if clicked on any of the buttons children
                for o in self.__current_children:
                    # get child
                    text, pos, size, id = o
                    # check if hovering over child
                    x,y = pos
                    w,h = size
                    hover = self.__hover_over((x-4,y-4,self.__child_max_width+10,h+9),pygame.mouse.get_pos())

                    if hover:
                        # trigger an event for that child
                        self.__trigger(self.__open_menu+"."+id)

                # check if clicked on any of the buttons
                a = False
                for b in self.buttons:
                    size = b["size"]
                    pos = size["x"]-4, size["y"]-4, size["w"]+9, size["h"]+9
                    hover = self.__hover_over(pos,pygame.mouse.get_pos())

                    if hover:
                        self.__open_menu = b["id"]
                        a = True
                # if no button was clicked, close all menus
                if not a:
                    self.__open_menu = None
            # if right click was done, close all menus
            if event.button == 3:
                self.__open_menu = None

    def draw(self):
        # clear events
        self.__events = []

        # get screen size
        w,h = self.screen.get_size()

        # draw rectangle for bar
        pygame.draw.rect(self.screen, self.col_background, pygame.Rect(0, 0, w, self.height))

        buttons = self.buttons
        # x value
        x = 5
        # draw all buttons
        for i in range(len(buttons)):
            # get text
            text = self.font.render(buttons[i]["name"],True,(255,255,255))
            if not "size" in buttons[i]:
                # get size of text
                tw, th = text.get_size()
                y = self.height/2 - th/2
                # update button thing
                self.buttons[i]["size"] = {}
                self.buttons[i]["size"]["x"] = x
                self.buttons[i]["size"]["y"] = y
                self.buttons[i]["size"]["w"] = tw
                self.buttons[i]["size"]["h"] = th
                buttons = self.buttons
            # check if mous is over button or button is selected
            size = self.buttons[i]["size"]
            pos = size["x"]-4, size["y"]-4, size["w"]+9, size["h"]+9
            hover = self.__hover_over(pos,pygame.mouse.get_pos())
            if hover or self.__open_menu == buttons[i]["id"]:
                # draw highlight
                pygame.draw.rect(self.screen, self.col_highlight, pygame.Rect(x-4, buttons[i]["size"]["y"]-4, buttons[i]["size"]["w"]+9, buttons[i]["size"]["h"]+9), border_radius=4)

            if self.__open_menu == buttons[i]["id"]:
                self.__drawMenu(buttons[i]["id"])
            elif self.__open_menu == None:
                self.__current_children = []

            # mover open menu if hovering over current button while menu is open
            if hover and self.__open_menu != None:
                self.__open_menu = buttons[i]["id"]
            # draw text
            self.screen.blit(text,(buttons[i]["size"]["x"],buttons[i]["size"]["y"]))
            # increment x
            x += buttons[i]["size"]["w"] + 10

    def __drawMenu(self,id):
        index = -1
        # get index in buttons
        for i in range(len(self.buttons)):
            if self.buttons[i]["id"] == id:
                index = i

        button = self.buttons[index]
        # get position
        x = button["size"]["x"]
        y = button["size"]["y"]
        w = 10
        h = 10
        
        # get all children
        child_texts = []

        cx = x
        cy = y+h + 15

        totalW = 5
        totalH = 5

        for o in button["children"]:
            # create text
            text = self.font.render(o["name"],True,(255,255,255))


            # get width of text
            tw, th = text.get_size()

            if tw > totalW:
                totalW = tw

            totalH += th + 10

            child_texts.append((text,(cx,cy),(tw,th),o["id"]))

            # increment y
            cy += th + 10

        self.__child_max_width = totalW
        self.__current_children = child_texts

        # draw rectangle
        pygame.draw.rect(self.screen, self.col_background, pygame.Rect(x-4,self.height,totalW+10,totalH))
        # draw all children
        for o in child_texts:
            # get child
            text, pos, size,id = o
            # check if hovering over child
            x,y = pos
            w,h = size
            hover = self.__hover_over((x-4,y-4,totalW+10,h+9),pygame.mouse.get_pos())

            # if hover draw highlight
            if hover:
                pygame.draw.rect(self.screen, self.col_highlight, pygame.Rect(x-4, y-4, totalW+10, h+9, border_radius=4))
            # draw child on screen
            self.screen.blit(text, pos)