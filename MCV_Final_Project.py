'''
A Visual Representation of Euler's Method
Victor Lelikov, Bernie Chen, and Jason Kim
MCV4U0 Culminating
'''

'''
Imports:
pygame - enables use of simpler, more intuitive I/O
matplotlib(.pyplot) - enables plotting and graphing
numpy - enables features necessary for plotting, including numpy arrays
math - enables use of basic math features, such as sqrt() and pi
PIL(.ImageFont) - enables the calculation of the size of font on a screen
sys - enables interfacing with the operating system
'''
import pygame as pg
import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import ImageFont
import sys

#Initializing pygame
pg.init()

'''
Window and low-level program constants

WIDTH - Stores the width of the window 
HEIGHT - Stores the height of the window
FRAMERATE - Stores the program framerate
screen - Stores the program window
clock - Used to regulate framerate
'''
WIDTH=640
HEIGHT=480
FRAMERATE = 30
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

'''
Game state variables

isRunning - Stores whether the program is running
screenOn - Stores the screen the program is on.
    main_menu -> The main menu
    enter_info -> A screen right before the program where information is entered
    program -> The main program
    info -> An explanation screen
'''
isRunning = True
screenOn = "main_menu"

'''
Colour Variables
'''
WHITE = (255,255,255)
BLACK = (0,0,0)
CYAN = (1,200,200)
LIME_GREEN = (50,205,50)
BLUE = (0,0,255)
RED = (255,0,0)
CREAM = (254,251,234)
SILVER = (192,192,192)
DARK_GRAY = (100,100,100)
LIGHT_GRAY = (230,230,230)
LIGHT_BLUE = (200,200,255)
LIGHT_RED = (255,150,150)
LIGHT_GREEN = (150,255,150)

'''
Font variables
'''
fontTitle = pg.font.SysFont('arial.ttf', 80)
fontSubtitle24 = pg.font.SysFont('arial.ttf', 24)
fontSubtitle30 = pg.font.SysFont('arialblack.ttf', 30)
fontSubtitle40 = pg.font.SysFont('arial.ttf', 40)
fontSubtitle50 = pg.font.SysFont('arial.ttf', 50)
fontSubtitle60 = pg.font.SysFont('arial.ttf', 60)
fontUtil120 = pg.font.SysFont('arial.ttf', 120)

'''
Button State variables per screen
'''
mainMenuButtons = {'continue':False, 'info':False, 'quit':False}
expButtons = {'menu':False, 'continue':False}
enterButtons = {'1':False}
mainPgmButtons = {'menu':False, 'openGraph':False}

'''
Program Info Variables
Used for calculations and plotting

coords - stores the coordinates calculated using Euler's method
xBound - stores the starting x value
yBound - stores the starting y value
hVal - stores the dX (or h) value
fX - stores the function as a string using TeX syntax, 
    with the exception that ^ is substituted with **
yAtX - stores the desired x value to be approximated

showPlot - stores whether the plot is to be shown. 
    Can be controlled in the main program
'''
coords = []
xBound = None
yBound = None
hVal = None
fX = None
yAtX = None
showPlot = False

'''
Math Constants
pi = 3.14159265...
e = 2.7182818...
sqrt = square root function
'''
pi = math.pi
e = math.e
sqrt = lambda a : math.sqrt(a)

#Changing the caption of the program screen
pg.display.set_caption("Euler's Method")

def getFontSize(text, fontSize, fontName):
    '''
    Getting the pixel dimensions of provided text

    :param text: (str) A string storing the text being checked
    :param fontSize: (int) The size of the text being checked
    :param fontName: (str) The name of the font being checked
    :return: A tuple of the text size (width, height)
    '''
    font = ImageFont.truetype(fontName, fontSize)
    size = font.getsize(text)
    return size

class MovingPoint():
    '''
    A class representing a point that moves across the screen on an elliptical trajectory
    '''
    def __init__(self, centerX, centerY, w, h, size, col, startAngle, speed):
        '''
        Constructor

        :param centerX: (int) The center-X of the ellipse representing the trajectory
        :param centerY: (int) The center-Y of the ellipse representing the trajectory
        :param w: (int) The width of the ellipse representing the trajectory
        :param h: (int) The height of the ellipse representing the trajectory
        :param size: (int) The size of the drawn point itself
        :param col: ((int, int, int))) The colour of the drawn point
        :param startAngle: (int) The initial angle between the line from the center of
            the circle to the exact bottom of the circle and the line from the center of
            the circle to the point.
        :param speed: (int) The speed at which the point travels along the elliptical path
        '''
        self.pathPosition = (centerX, centerY, w, h)
        self.x = centerX
        self.y = centerY
        self.size = size
        self.col = col
        self.degree = startAngle
        self.initAngle = startAngle
        self.speed = speed
        self.dir = 'f'

    def constrainCircle(self, xMin, xMax):
        '''
        Used to constrain the point to follow the elliptical path within the specified boundaries

        :param xMin: (int) The left boundary
        :param xMax: (int) The right boundary
        '''
        if (self.x >= xMax):
            self.dir='r'
        elif (self.x <= xMin):
            self.dir='f'

    def moveCircle(self):
        '''
        Used to move the point along the elliptical path
        '''
        if (self.dir == 'f'):
            self.degree = (self.degree + self.speed) % 360
        else:
            self.degree = (self.degree - self.speed) % 360
        self.x = int(math.cos(self.degree * 2 * math.pi / 360) * int(self.pathPosition[2] / 2) + self.pathPosition[0])
        self.y = int(math.sin(self.degree * 2 * math.pi / 360) * int(self.pathPosition[3] / 2) + self.pathPosition[1])

    def draw(self):
        '''
        Used to draw the point
        '''
        pg.draw.circle(surface=screen, color=self.col, center=(self.x,self.y),radius=self.size)

class Button():
    '''
    A class representing a pressable button
    '''
    def __init__(self, x, y, w, h, col, text, fontSize):
        '''
        Constructor

        :param x: (int) The X of the top left point
        :param y: (int) The Y of the top left point
        :param w: (int) The width of the button
        :param h: (int) The height of the button
        :param col: ((int, int, int)) The colour of the button when it isn't pressed
        :param text: (str) The text on the button
        :param fontSize: (int) The size of the text on the button
        '''
        self.rect = pg.Rect(x,y,w,h)
        self.col = col
        self.text = text
        self.fontSize = fontSize
        self.font = pg.font.SysFont('arial.ttf', self.fontSize)
        self.pressed = False

    def getPressed(self):
        '''
        Checks if the button is pressed at the moment of calling.
        Sets self.pressed to store that state

        :return: (boolean) Whether the button is pressed or not
        '''
        mouseX, mouseY = pg.mouse.get_pos()
        mouseL, mouseM, mouseR = pg.mouse.get_pressed()

        #collidepoint() checks if the mouse coordinates are within the boundaries of the rectangle
        self.pressed = self.rect.collidepoint((mouseX, mouseY)) and mouseL

        return self.pressed

    def draw(self):
        '''
        Used to draw the button and text on it
        Called when the button is in a released state
        '''
        pg.draw.rect(surface=screen, color=self.col, rect=self.rect, width=0, border_radius=int(self.rect[2] / 10))
        buttonFont = self.font.render(self.text, False, BLACK, self.col)
        textSize = getFontSize(text=self.text, fontSize=self.fontSize-10, fontName="arial.ttf")
        screen.blit(buttonFont, (self.rect[0] + int((self.rect[2] - textSize[0]) / 2), self.rect[1] + int((self.rect[3] - textSize[1]) / 2)))

    def drawPressed(self):
        '''
        Used to draw the button and text on it
        Called when the button is in a pressed state
        '''
        #Getting a slightly darker version of the original colour to use
        pressCol = (max(0, self.col[0] - 30), max(0, self.col[1] - 30), max(0, self.col[2] - 30))

        #Drawing the button
        pg.draw.rect(surface=screen, color=pressCol, rect=self.rect, width=0, border_radius=int(self.rect[2] / 10))
        #Rendering, positioning, and drawing the text
        buttonFont = self.font.render(self.text, False, BLACK, pressCol)
        textSize = getFontSize(text=self.text, fontSize=self.fontSize-10, fontName="arial.ttf")
        screen.blit(buttonFont, (self.rect[0] + int((self.rect[2] - textSize[0]) / 2), self.rect[1] + int((self.rect[3] - textSize[1]) / 2)))

class TextBox():
    '''
    A class used to represent a textbox that can be interacted with
    '''
    def __init__(self, x, y, w, h, thickness, col):
        '''
        Constructor

        :param x: (int) stores the x position of the top right corner of the button
        :param y: (int) stores the y position of the top right corner of the button
        :param w: (int) stores the width of the button
        :param h: (int) stores the height of the button
        :param thickness: (int) stores the thickness of the button's walls
        :param col: (int,int,int) stores the RGB values of the button's nominal colour (not pressed or invalid)
        '''
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.thickness = thickness
        self.col = col
        self.validEntry = True
        self.text = ""
        self.selected = False
        self.lastToggled = 0

    def draw(self):
        '''
        Method used to draw the button

        The colours change depending on 2 things:
        If the button's entry isn't considered 'valid' and the button is NOT selected,
        the button draws itself red

        If the button's entry isn't considered 'valid' and the button IS selected,
        the button draws itself slightly lighter than the typical red

        If the button's entry is empty or 'valid' and the button is NOT selected,
        the button draws itself in its nominal colour

        If the button's entry is empty or 'valid' and the button IS selected,
        the button draws itself slightly darker than its nominal colour
        '''
        if(self.validEntry == True and self.selected == False):
            innerCol = (210,210,210)
            outerCol = self.col
        elif(self.validEntry == True and self.selected == True):
            innerCol = WHITE
            outerCol = self.col
        elif(self.validEntry == False and self.selected == False):
            innerCol = (255, 150, 150)
            outerCol = (255,0,0)
        elif(self.validEntry == False and self.selected == True):
            innerCol = (255, 200, 200)
            outerCol = (255,0,0)

        # Drawing the 2 button rectangles - outer and inner
        pg.draw.rect(surface=screen, color=outerCol, rect=(self.x,self.y,self.w,self.h),width=self.thickness, border_radius=self.thickness)
        pg.draw.rect(surface=screen, color=innerCol, rect=(self.x+self.thickness, self.y+self.thickness, self.w-2*self.thickness, self.h-2*self.thickness), border_radius=self.thickness)

        # Drawing the text on the button
        textLen = 0
        letter = 0
        #Enabling scrolling of the text if it's longer than what the textbox fits
        while(textLen < self.w-3*self.thickness and letter < len(self.text)):
            letter+=1
            textLen = getFontSize(text=self.text[len(self.text)-letter:], fontSize=40, fontName="arial.ttf")[0]

        text = self.text[len(self.text) - letter:]
        screen.blit(fontSubtitle40.render(text, True, BLACK), (self.x+2*self.thickness, self.y+2*self.thickness))

    def checkClick(self):
        '''
        Method used to check if the button is clicked
        '''
        #Getting the X,Y position of the mouse
        mX, mY = pg.mouse.get_pos()
        #Getting the pressed state of the 3 buttons of the mouse (lClick, mClick, rClick)
        mL, mM, mR = pg.mouse.get_pressed()

        # If the mouse is clicked (mL == True) and over the textbox (collidepoint() is true),
        # the textbox checks if it's state was toggled within a range. If it was, this is ignored.
        # If not, the state is toggled. This is done to avoid toggles every frame.
        if (mL == True):
            if (pg.Rect(self.x, self.y, self.w, self.h).collidepoint(mX, mY) == True):
                if (self.selected == False):
                    if (self.lastToggled > FRAMERATE*0.1):
                        self.lastToggled = 0
                        self.selected = True
                if (self.selected == True):
                    if (self.lastToggled > FRAMERATE * 0.1):
                        self.lastToggled = 0
                        self.selected = False
            else:
                self.lastToggled = 0
                self.selected = False

        self.lastToggled += 1

    def enterText(self,events):
        '''
        Method used to enter text into the textbox

        :param events: pygame events (including key and mousepresses, mouse moves, etc.)
        '''
        #If the button is selected,
        if (self.selected == True):
            for event in events:
                #If the event is a keypress
                if event.type == 768:
                    #and the event is not a backspace
                    if (event.key != pg.K_BACKSPACE):
                        #Entering keys (a-z, 0-9, math symbols), event.mod is for capitalization
                        if ((event.key >= pg.K_a and event.key <= pg.K_z) or (event.key >= pg.K_0 and event.key <= pg.K_9) or event.key == pg.K_MINUS or event.key == pg.K_SLASH or event.key == pg.K_EQUALS or event.key == pg.K_PERIOD):
                            if (event.key == pg.K_EQUALS and event.mod == 32769):
                                self.text += "+"
                            elif (event.key == pg.K_EQUALS and event.mod == 1):
                                self.text += "+"
                            elif(event.key == pg.K_8 and event.mod == 32769):
                                self.text += "*"
                            elif(event.key == pg.K_8 and event.mod == 1):
                                self.text += "*"
                            elif(event.key == pg.K_9 and event.mod == 32769):
                                self.text += "("
                            elif(event.key == pg.K_9 and event.mod == 1):
                                self.text += "("
                            elif(event.key == pg.K_0 and event.mod == 32769):
                                self.text += ")"
                            elif(event.key == pg.K_0 and event.mod == 1):
                                self.text += ")"
                            else:
                                self.text += pg.key.name(event.key)
                    #If the event is a backspace, the last character is removed
                    else:
                        if (len(self.text) > 0):
                            self.text = self.text[:-1]

#Creating an instance of MovingPoint for the main menu
mainMenuPt = MovingPoint(centerX=120,centerY=0,w=800,h=600,size=15,col=LIME_GREEN,startAngle=90,speed=-1)

def mainMenu():
    global screenOn, isRunning

    '''
    Used to draw the elements of the main menu. Called when screenOn is 'main_menu'

    :return None: Exits the program when the 'quit' button is pressed or the window is closed
    :return None: Changes the game state to 'program' when the 'continue' button is pressed
    '''
    #Quitting if the red 'x' on the window bar is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

    #Creating the three buttons
    ContinueBtn = Button(30,414,180,50,CYAN,"CONTINUE!",30)
    InfoBtn = Button(230,414, 180, 50, CYAN, "INFO", 30)
    QuitBtn = Button(430,414,180,50,CYAN,"QUIT",30)

    #Updating the position of the moving point
    mainMenuPt.moveCircle()
    mainMenuPt.constrainCircle(xMin=mainMenuPt.pathPosition[0], xMax=int(mainMenuPt.pathPosition[0] + mainMenuPt.pathPosition[2] / 2))

    #Drawing
    screen.fill(LIGHT_GRAY)

    #Drawing notebook background
    for l in range(40):
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(l*(16),0), end_pos=(l*16,480))
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(0,l*12), end_pos=(640,l*12))

    #Drawing red margin line
    pg.draw.line(surface=screen, color=LIGHT_RED, start_pos=(20,0), end_pos=(20,480), width=3)

    # Drawing the graph
    # Euler Algo Lines
    lines = [((120, 300), (220, 300)), ((220, 300), (320, 281)), ((320, 281), (420, 237)), ((420, 237), (520, 152))]
    for line in lines:
        pg.draw.line(surface=screen, color=LIME_GREEN, start_pos=line[0], end_pos=line[1], width=5)

    # Vertical lines
    lines = [((120, 300), (120, 350)), ((220, 300), (220, 350)), ((320, 281), (320, 350)), ((420, 237), (420, 350)),
             ((520, 152), (520, 350))]
    for line in lines:
        pg.draw.line(surface=screen, color=LIME_GREEN, start_pos=line[0], end_pos=line[1], width=5)

    # Short dark grey vertical bars
    for x in range(120, 521, 100):
        pg.draw.line(surface=screen, color=DARK_GRAY, start_pos=(x, 350), end_pos=(x, 365), width=7)

    # Horizontal line
    pg.draw.line(surface=screen, color=DARK_GRAY, start_pos=(120, 355), end_pos=(520, 355), width=5)

    # Drawing the 'h'
    screen.blit(fontSubtitle40.render("h", True, DARK_GRAY), (162, 385))

    # Drawing the sideways '{' for the 'h'
    curly = fontUtil120.render("{", True, DARK_GRAY)
    curlyRot = pg.transform.rotate(curly, 90)
    curlyRot = pg.transform.scale(curlyRot, (120, 25))
    screen.blit(curlyRot, (107, 362))

    #Drawing the arc representing the path of the moving point along a function
    arcWidth = mainMenuPt.pathPosition[2]
    arcHeight = mainMenuPt.pathPosition[3]
    pg.draw.arc(surface=screen, color=BLUE, rect=(120-int(arcWidth/2),0-int(arcHeight/2),arcWidth+int(mainMenuPt.size/3),arcHeight+int(mainMenuPt.size/3)),start_angle=3*math.pi/2,stop_angle=2*math.pi,width=10)
    pg.draw.circle(surface=screen, color=BLUE, center=(120,300),radius=5)

    #Drawing the moving point
    mainMenuPt.draw()

    #Drawing the title and subtitle
    titleText = [fontTitle.render("Showcasing", True, BLACK),
    fontTitle.render("Euler's", True, BLACK),
    fontTitle.render("Method", True, BLACK)]
    for text in range(len(titleText)):
        screen.blit(titleText[text], (75, int(HEIGHT * ((50 + text*55) / 480))))

    subTitleText = [fontSubtitle30.render("Bernie Chen, Jason Kim", True, DARK_GRAY),
                    fontSubtitle30.render("Victor Lelikov", True, DARK_GRAY)]

    for text in range(len(subTitleText)):
        screen.blit(subTitleText[text], (80, 220+text*30))

    '''
    Checking the 'quit' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (mainMenuButtons['quit'] == True):                               #Pressed on prev. frame
        if (QuitBtn.getPressed() == True):                              #Pressed on current frame, no change!
            QuitBtn.drawPressed()
        else:                                                           #Not pressed on current frame, change!
            QuitBtn.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (QuitBtn.rect.collidepoint(mouseX,mouseY)):
                isRunning = False
            else:
                pass
    else:                                                               #Not pressed on previous frame
        QuitBtn.draw()

    '''
    Checking the 'continue' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (mainMenuButtons['continue'] == True):
        if (ContinueBtn.getPressed() == True):
            ContinueBtn.drawPressed()
        else:
            ContinueBtn.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (ContinueBtn.rect.collidepoint(mouseX,mouseY)):
                screenOn = "enter_info"
            else:
                pass
    else:
        ContinueBtn.draw()

    '''
    Checking the 'info' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (mainMenuButtons['info'] == True):
        if (InfoBtn.getPressed() == True):
            InfoBtn.drawPressed()
        else:
            InfoBtn.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (InfoBtn.rect.collidepoint(mouseX,mouseY)):
                screenOn = "info"
            else:
                pass
    else:
        InfoBtn.draw()

    #Updating the button state variables, allowing the states this frame to be used
    #in the next frame's comparison
    mainMenuButtons['quit'] = QuitBtn.getPressed()
    mainMenuButtons['continue'] =  ContinueBtn.getPressed()
    mainMenuButtons['info'] = InfoBtn.getPressed()

    #flip() is used to update the screen
    #tick() is used to regulate the framerate
    pg.display.flip()
    clock.tick(FRAMERATE)

expScreenOn = 1
def explanationMenu():
    global expScreenOn, isRunning

    '''
    Function used to differentiate between the 3 different 
    explanation/definition screens
    '''

    while (screenOn == "info" and isRunning == True):
        # Quitting if the red 'x' on the window bar is pressed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                isRunning = False

        if (expScreenOn == 1):
            definitionScreen()
        elif (expScreenOn == 2):
            explanationScreen()
        elif (expScreenOn == 3):
            explanationScreen2()

    expScreenOn = 1

#Buttons that are common to the 3 screens
expMenuButton = Button(40,420,100,40,LIGHT_BLUE,"< MENU",24)
expNextButton = Button(480,418,110,44,LIGHT_GREEN,"NEXT >",26)

def definitionScreen():
    '''
    Used to explain the definition and usages of Euler's method. Called when screenOn is 'info'

    '''
    global isRunning, screenOn, expScreenOn

    #Quitting if the red 'x' on the window bar is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

        # Drawing
    screen.fill(LIGHT_GRAY)

    #Drawing notebook background
    for l in range(40):
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(l*(16),0), end_pos=(l*16,480))
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(0,l*12), end_pos=(640,l*12))

    pg.draw.line(surface=screen, color=LIGHT_RED, start_pos=(20,0), end_pos=(20,480), width=3)

    '''
    Checking the 'continue' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (expButtons['menu'] == True):
        if (expMenuButton.getPressed() == True):
            expMenuButton.drawPressed()
        else:
            expMenuButton.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (expMenuButton.rect.collidepoint(mouseX,mouseY)):
                expNextButton.draw()
                screenOn = 'main_menu'
            else:
                pass
    else:
        expMenuButton.draw()

    '''
    Checking the 'mmenu' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (expButtons['continue'] == True):
        if (expNextButton.getPressed() == True):
            expNextButton.drawPressed()
        else:
            expNextButton.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (expNextButton.rect.collidepoint(mouseX,mouseY)):
                # Updating the button state variables, allowing the states this frame to be used
                # in the next frame's comparison
                expButtons['continue'] = expNextButton.getPressed()
                expButtons['menu'] = expMenuButton.getPressed()

                expNextButton.draw()
                expScreenOn=2
            else:
                pass
    else:
        expNextButton.draw()

    #Updating the button state variables, allowing the states this frame to be used
    #in the next frame's comparison
    expButtons['continue'] = expNextButton.getPressed()
    expButtons['menu'] =  expMenuButton.getPressed()

    subtitleText = fontTitle.render("Info: Definition", True, BLACK)
    screen.blit(subtitleText, (120, 20))

    subtitleText = fontSubtitle24.render("Welcome to the Euler's Method Demonstration Program! After reading this", True, BLACK)
    screen.blit(subtitleText, (40, 90))

    subtitleText = fontSubtitle24.render("info page, you will be able to use this program more accurately than what", True, BLACK)
    screen.blit(subtitleText, (40, 110))

    subtitleText = fontSubtitle24.render("Euler's method could ever compute :)", True, BLACK)
    screen.blit(subtitleText, (40, 130))

    subtitleText = fontSubtitle24.render("Euler's method, named after mathmatician Leonhard Euler, is a step by step", True, BLACK)
    screen.blit(subtitleText, (40, 170))

    subtitleText = fontSubtitle24.render("procedure that is used to analyze a first order differential equation. ", True, BLACK)
    screen.blit(subtitleText, (40, 190))

    subtitleText = fontSubtitle24.render("The idea of this method is to approximate solution curve using line ", True, BLACK)
    screen.blit(subtitleText, (40, 230))

    subtitleText = fontSubtitle24.render("segments, in which the approximated solution from the curve starts from a", True, BLACK)
    screen.blit(subtitleText, (40, 250))

    subtitleText = fontSubtitle24.render("given initial value. Using a set incrememtation of value h, the point is ", True, BLACK)
    screen.blit(subtitleText, (40, 270))

    subtitleText = fontSubtitle24.render("approximated for every subsequent point for every x value increased by the", True, BLACK)
    screen.blit(subtitleText, (40, 290))

    subtitleText = fontSubtitle24.render("value of h. ", True, BLACK)
    screen.blit(subtitleText, (40, 310))

    subtitleText = fontSubtitle24.render("Although using Euler's method will not give an exact answer as it only ", True, BLACK)
    screen.blit(subtitleText, (40, 350))

    subtitleText = fontSubtitle24.render("calculates an approximate of the acutal value, it is useful when other ", True, BLACK)
    screen.blit(subtitleText, (40, 370))

    subtitleText = fontSubtitle24.render("methods of solving differential equations prove to be difficult to use. ", True, BLACK)
    screen.blit(subtitleText, (40, 390))

    #flip() is used to update the screen
    #tick() is used to regulate the framerate
    pg.display.flip()
    clock.tick(FRAMERATE)

def explanationScreen():
    '''
    Used to draw an explanation of Euler's method. Called when screenOn is 'info'

    :return None: Exits the program when the 'quit' button is pressed or the window is closed
    :return None: Changes the game state to 'main_menu' when the 'back' button is pressed #TODO: this
    '''

    global isRunning, screenOn, expScreenOn

    #Quitting if the red 'x' on the window bar is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

        # Drawing
    screen.fill(LIGHT_GRAY)

    #Drawing notebook background
    for l in range(40):
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(l*(16),0), end_pos=(l*16,480))
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(0,l*12), end_pos=(640,l*12))

    pg.draw.line(surface=screen, color=LIGHT_RED, start_pos=(20,0), end_pos=(20,480), width=3)

    '''
    Checking the 'continue' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (expButtons['menu'] == True):
        if (expMenuButton.getPressed() == True):
            expMenuButton.drawPressed()
        else:
            expMenuButton.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (expMenuButton.rect.collidepoint(mouseX,mouseY)):
                expNextButton.draw()
                screenOn = 'main_menu'
            else:
                pass
    else:
        expMenuButton.draw()

    '''
    Checking the 'mmenu' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (expButtons['continue'] == True):
        if (expNextButton.getPressed() == True):
            expNextButton.drawPressed()
        else:
            expNextButton.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            #If this unclick occurs while the mouse is on the button
            #and not because it was dragged off the button
            if (expNextButton.rect.collidepoint(mouseX,mouseY)):
                expNextButton.draw()
                expScreenOn=3

            else:
                pass
    else:
        expNextButton.draw()

    #Updating the button state variables, allowing the states this frame to be used
    #in the next frame's comparison
    expButtons['continue'] = expNextButton.getPressed()
    expButtons['menu'] =  expMenuButton.getPressed()

    subtitleText = fontTitle.render("Info: Explanation", True, BLACK)
    screen.blit(subtitleText, (90, 20))

    subtitleText = fontSubtitle24.render("When you click on the continue button, you will be asked to enter the", True, BLACK)
    screen.blit(subtitleText, (40, 90))

    subtitleText = fontSubtitle24.render("following information:", True, BLACK);
    screen.blit(subtitleText, (40, 110))

    subtitleText = fontSubtitle24.render("dy/dx expression:  --> The first order differential equation that's being", True, BLACK)
    screen.blit(subtitleText, (60, 150))

    subtitleText = fontSubtitle24.render("used to approximate. Must only contain x and y", True, BLACK)
    screen.blit(subtitleText, (230, 170))

    subtitleText = fontSubtitle24.render("variables. ", True, BLACK);
    screen.blit(subtitleText, (230, 190))

    subtitleText = fontSubtitle24.render("Initial point position (x0, y0) --> The boundary conditions (the starting ", True, BLACK)
    screen.blit(subtitleText, (60, 230))

    subtitleText = fontSubtitle24.render("point) for Euler's method.", True, BLACK)
    screen.blit(subtitleText, (305, 250))

    subtitleText = fontSubtitle24.render("h --> this is the increment value that your x value will change by per", True, BLACK)
    screen.blit(subtitleText, (60,  290))

    subtitleText = fontSubtitle24.render("approximation.", True, BLACK)
    screen.blit(subtitleText, (98, 310))

    subtitleText = fontSubtitle24.render("y(  ) --> this is the y(x) - enter the x value that you want to approx. at", True, BLACK)
    screen.blit(subtitleText, (98, 350))

    #flip() is used to update the screen
    #tick() is used to regulate the framerate
    pg.display.flip()
    clock.tick(FRAMERATE)

def explanationScreen2():
    '''
    Used to draw an explanation of Euler's method on the second panel. Called when
    is 'info'

    :return None: Exits the program when the 'quit' button is pressed or the window is closed
    :return None: Exits the program when the 'quit' button is pressed or the window is closed
    :return None: Exits the program when the 'quit' button is pressed or the window is closed
    :return None: Changes the game state to 'main_menu' when the 'back' button is pressed #TODO: this
    '''
    global isRunning, screenOn, expScreenOn

    # Quitting if the red 'x' on the window bar is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

        # Drawing
    screen.fill(LIGHT_GRAY)

    # Drawing notebook background
    for l in range(40):
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(l * (16), 0), end_pos=(l * 16, 480))
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(0, l * 12), end_pos=(640, l * 12))

    pg.draw.line(surface=screen, color=LIGHT_RED, start_pos=(20, 0), end_pos=(20, 480), width=3)

    '''
    Checking the 'mmenu' button state this frame, comparing it to the state the last frame,
    drawing the appropriate button and performing the appropriate action    
    '''
    if (expButtons['continue'] == True):
        if (expNextButton.getPressed() == True):
            expNextButton.drawPressed()
        else:
            expNextButton.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            # If this unclick occurs while the mouse is on the button
            # and not because it was dragged off the button
            if (expNextButton.rect.collidepoint(mouseX, mouseY)):
                expNextButton.draw()
                screenOn = 'main_menu'

            else:
                pass
    else:
        expNextButton.draw()

    # Updating the button state variables, allowing the states this frame to be used
    # in the next frame's comparison
    expButtons['continue'] = expNextButton.getPressed()

    subtitleText = fontSubtitle24.render("After entering all the above information and clicking the '\"calculate\" button", True, BLACK)
    screen.blit(subtitleText, (35, 20))

    subtitleText = fontSubtitle24.render("the program will generate both a table of values showing the steps to each", True, BLACK)
    screen.blit(subtitleText, (35, 40))

    subtitleText = fontSubtitle24.render("increment for your differential equation, and it will also display a graph", True, BLACK)
    screen.blit(subtitleText, (35, 60))

    subtitleText = fontSubtitle24.render("showing the graphical solution for the points found using Euler's method. ", True, BLACK)
    screen.blit(subtitleText, (35, 80))

    subtitleText = fontSubtitle24.render("On the same screen you will be given options to change your h value as", True, BLACK)
    screen.blit(subtitleText, (35, 120))

    subtitleText = fontSubtitle24.render("long as it meets its conditions, as well as the point of approximation ", True, BLACK)
    screen.blit(subtitleText, (35, 140))

    subtitleText = fontSubtitle24.render("for the solution you want to find. The h value must be a valid number that ", True, BLACK)
    screen.blit(subtitleText, (35, 160))

    subtitleText = fontSubtitle24.render("evenly divides the the set of values from the initial point all the way to the", True, BLACK)
    screen.blit(subtitleText, (35, 180))

    subtitleText = fontSubtitle24.render("final approximation point. For example, When applying Euler's method with ", True, BLACK)
    screen.blit(subtitleText, (35, 200))

    subtitleText = fontSubtitle24.render("the intial x value as 0 that solves at the appoximation point y(1), possible ", True, BLACK)
    screen.blit(subtitleText, (35, 220))

    subtitleText = fontSubtitle24.render("h values can be 0.1, 0.2, or 0.5, but cannot be values like 0.3 or -0.2.", True, BLACK)
    screen.blit(subtitleText, (35, 240))

    subtitleText = fontSubtitle24.render("You will also be able to change the final approximation value y(x). Once", True, BLACK)
    screen.blit(subtitleText, (35, 280))

    subtitleText = fontSubtitle24.render("again, ensure that the h value can evenly divide into the new range of ", True, BLACK)
    screen.blit(subtitleText, (35, 300))

    subtitleText = fontSubtitle24.render("values set from this change. ", True, BLACK)
    screen.blit(subtitleText, (35, 320))

    subtitleText = fontSubtitle24.render("Finally, to exit the program, click the \"Quit\" button during either", True, BLACK)
    screen.blit(subtitleText, (35, 360))

    subtitleText = fontSubtitle24.render("the homescreen or the display screen showing the graphs and values. ", True, BLACK)
    screen.blit(subtitleText, (35, 380))

    subtitleText = fontSubtitle24.render("Have fun with using Euler's method! ", True, BLACK)
    screen.blit(subtitleText, (35, 420))


    #flip() is used to update the screen
    #tick() is used to regulate the framerate
    pg.display.flip()
    clock.tick(FRAMERATE)

def approxEuler(h, xLast, yLast, DyByDx):
    '''
    Method used to evaluate the differential function DyByDx using xLast and
    yLast in the place of x and y, respectively, and add it to the previous y-value in
    order to get the new y-value based off Euler
    '''
    x = xLast
    y = yLast
    return(yLast + eval(DyByDx)*h)

def makePointList(h, x, y, xFin, DyByDx, roundLvl):
    '''
    Method used to create a list of points using Euler's method, given an
    initial x, y, h values and a differential function DyByDx until xFin.
    roundLvl represents the number of decimal points to round to (4, usually).
    '''
    global coords #List of coordinates
    coords = []
    coords.append((x,y)) #Adding the initial (x,y) value to the coords list

    x = x
    y = y

    i = 0 #Storing the iteration of the loop

    #While the current x isn't that of the final x (It will reach it, as an invalid h value won't be accepted)
    while (x != xFin):
        # The program tries to evaluate the DyByDx function. If the function is not continuous, this will throw an error, which
        # will be caught by the except section, which will add a "CONT?" value to signify this error in user input.
        try:
            eval(DyByDx)
            # If the function IS continuous, the new points are added to the coords list
            coords.append((round(coords[i][0]+h, roundLvl), round(approxEuler(h, coords[i][0], coords[i][1], DyByDx), roundLvl)))
        except:
            coords.append((round(coords[i][0] + h, roundLvl),"CONT?"))

        #Changing the X value by the h value. The direction of change (+/-) depends on which way the value needs to go to reach xFin
        if (xFin > x):
            x += abs(h)
        else:
            x -= abs(h)
        x = round(x, roundLvl)
        i += 1

#Textboxes found in the enter info screen
textboxFX = TextBox(135,140,300,40,3,BLACK)
textboxBoundX = TextBox(100,255,120,40,3,BLACK)
textboxBoundY = TextBox(300,255,120,40,3,BLACK)
textboxHVal = TextBox(100,360,120,40,3,BLACK)
textboxYAtX = TextBox(143,420,120,40,3,BLACK)
boxes = [textboxFX, textboxBoundX, textboxBoundY, textboxHVal, textboxYAtX]
def enterInfoScreen():
    '''
    A method used to gather information from the user on the conditions of calculation.
    A majority of errortrapping occurs here, and the program will not let the user continue
    if there are some issues with any of the initial conditions.
    '''
    events = pg.event.get() #Getting input events (KB, Mouse, etc.)
    global isRunning, screenOn, xBound, yBound, fX, hVal, yAtX #Global variables used for calculations

    #Drawing the screen
    screen.fill(LIGHT_GRAY)

    #Creating the Calculate! button
    enterInfoButton = Button(420,355,200,80,CYAN,"CALCULATE!",36)

    #Drawing notebook background lines
    for l in range(40):
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(l*(16),0), end_pos=(l*16,480))
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(0,l*12), end_pos=(640,l*12))

    pg.draw.line(surface=screen, color=LIGHT_RED, start_pos=(20,0), end_pos=(20,480), width=3)

    #Drawing text on the screen
    text = fontSubtitle60.render("Enter Information", True, BLACK)
    screen.blit(text, (50, 30))

    text = fontSubtitle40.render("Enter your F(x) [dy/dx]", True, BLACK)
    screen.blit(text, (50, 110))

    text = fontSubtitle40.render("F(x) = ", True, DARK_GRAY)
    screen.blit(text, (50, 145))

    text = fontSubtitle40.render("Enter your boundary conditions:", True, BLACK)
    screen.blit(text, (50, 220))

    text = fontSubtitle40.render("x = ", True, DARK_GRAY)
    screen.blit(text, (50, 260))

    text = fontSubtitle40.render("y = ", True, DARK_GRAY)
    screen.blit(text, (250, 260))

    text = fontSubtitle40.render("Enter your h-value:", True, BLACK)
    screen.blit(text, (50, 330))

    text = fontSubtitle40.render("h = ", True, DARK_GRAY)
    screen.blit(text, (50, 365))

    text = fontSubtitle40.render("Find y(                )", True, BLACK)
    screen.blit(text, (50, 425))

    #Drawing the Calculate! button
    enterInfoButton.draw()

    #Drawing all the textboxes, checking if they're clicked, entering text if they are.
    #All that is handled in the TextBox class
    for box in boxes:
        box.draw()
        box.checkClick()
        box.enterText(events)

    #ERRORTRAPPING
    '''
    textboxBoundX:
    required value - float
    will not allow the user to pass if the value entered is not a float
    '''
    if (textboxBoundX.text != ""): #Check only occurs if the textbox isn't empty
        try:
            xBound = float(textboxBoundX.text) #Throws an error if the value is not a float
            textboxBoundX.validEntry = True

        except:
            textboxBoundX.validEntry = False
    else:
        xBound = None

    '''
    textboxBoundY:
    required value - float
    will not allow the user to pass if the value entered is not a float
    '''
    if (textboxBoundY.text != ""): #Check only occurs if the textbox isn't empty
        try:
            yBound = float(textboxBoundY.text) #Throws an error if the value is not a float
            textboxBoundY.validEntry = True

        except:
            textboxBoundY.validEntry = False
    else:
        yBound = None

    '''
    textboxFX:
    required value - valid function, can be constant or 1st degree differential
    will not allow the user to pass if the value entered does not match the above criteria
    '''
    if (textboxFX.text != ""): #Check only occurs if the textbox isn't empty
        try:
            fX1 = textboxFX.text
            if xBound != None:
                x = xBound
            else:
                x = 1
            if yBound != None:
                y = yBound
            else:
                y = 1
            eval(fX1) #Throws an error if the function throws an error, including but not limited to:
                      # division by zero, variable does not exist in the function (using a,b instead of x,y), and operation does not exist
            textboxFX.validEntry = True
            fX = fX1
        except:
            textboxFX.validEntry = False
    else:
        fX = None

    '''
    textboxHVal:
    required value - float
    will not allow the user to pass if the value entered is not a float
    '''
    if (textboxHVal.text != ""): #Check only occurs if the textbox isn't empty
        try:
            hVal = float(textboxHVal.text) #Throws an error if the value isn't a float
            textboxHVal.validEntry = True
        except:
            textboxHVal.validEntry = False
    else:
        hVal = None

    '''
    textboxYAtX:
    required value - float that is a multiple of the H Value
    will not allow the user to pass if the above conditions are not met
    '''
    if (textboxYAtX.text != ""): #Check only occurs if the textbox isn't empty
        try:
            tolerance = 10**(-10)
            yAtX = float(textboxYAtX.text) #Throws an error if the value isn't a float
            '''
            Due to python's gung-ho precision when it comes to number storage, using the modulus operator to check
            whether the yAtX is divisible by the hVal wouldn't work in the case of floats. This is because
            something like 4.0 is actually stored as 3.999999999971924..., so a modulus operator would result in
            a value of 10**-17, etc. As such, a different operation is used to check whether the number is 'basically'
            divisible by the h value (lower than the tolerance, which is 10^-10)
            '''
            if (abs((yAtX-xBound)/hVal - round((yAtX-xBound)/hVal)) < tolerance):
                textboxYAtX.validEntry = True
            else:
                textboxYAtX.validEntry = False
        except:
            textboxYAtX.validEntry = False
    else:
        yAtX = None

    #If the Calculate! button is pressed and all the values are valid, the program continues
    if (enterInfoButton.getPressed() == True):
        if (hVal != None and xBound != None and yBound != None and fX != None and yAtX != None
                and textboxHVal.validEntry == True
                and textboxFX.validEntry == True and textboxBoundX.validEntry == True
                and textboxBoundY.validEntry == True and textboxYAtX.validEntry == True):
            screenOn = "program"
        else:
            pass
    #flip() is used to update the screen
    #tick() is used to regulate the framerate
    pg.display.flip()
    clock.tick(FRAMERATE)

def mainProgram():
    '''
    Method used to calculate the values using Euler's method and previous functions. It also creates
    a MatPlotLib plot that graphs the points.
    '''
    events = pg.event.get()
    global isRunning, screenOn, xBound, yBound, fX, hVal, showPlot, coords

    # Quitting if the red 'x' on the window bar is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

    #Creating a list of points using the Euler method
    coords = []
    makePointList(h=hVal, x=xBound, y=yBound, xFin=yAtX, DyByDx=fX, roundLvl=4)
    # Clearing the plot
    plt.clf()
    plt.cla()
    plt.close()

    #Creating the 'go to main menu' and 'graph' buttons
    mainMenuBtn = Button(330, 418, 110, 44, LIGHT_GREEN, "MENU", 26)
    mainPltBtn = Button(470, 418, 110, 44, LIGHT_GREEN, "GRAPH", 26)

    # Drawing
    screen.fill(LIGHT_GRAY)
    # Drawing notebook background
    for l in range(40):
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(l * (16), 0), end_pos=(l * 16, 480))
        pg.draw.line(surface=screen, color=LIGHT_BLUE, start_pos=(0, l * 12), end_pos=(640, l * 12))
    #Drawing the red margin line
    pg.draw.line(surface=screen, color=LIGHT_RED, start_pos=(20, 0), end_pos=(20, 480), width=3)

    '''
        Checking the 'main menu' button state this frame, comparing it to the state the last frame,
        drawing the appropriate button and performing the appropriate action    
    '''
    if (mainPgmButtons['menu'] == True):
        if (mainMenuBtn.getPressed() == True):
            mainMenuBtn.drawPressed()
        else:
            mainMenuBtn.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            # If this unclick occurs while the mouse is on the button
            # and not because it was dragged off the button
            if (mainMenuBtn.rect.collidepoint(mouseX, mouseY)):
                mainMenuBtn.draw()
                screenOn = 'main_menu'

            else:
                pass
    else:
        mainMenuBtn.draw()

    # Updating the button state variables, allowing the states this frame to be used
    # in the next frame's comparison
    mainPgmButtons['menu'] = mainMenuBtn.getPressed()

    '''
       Checking the 'main menu' button state this frame, comparing it to the state the last frame,
       drawing the appropriate button and performing the appropriate action    
    '''
    if (mainPgmButtons['openGraph'] == True):
        if (mainPltBtn.getPressed() == True):
            mainPltBtn.drawPressed()
        else:
            mainPltBtn.draw()
            mouseX, mouseY = pg.mouse.get_pos()
            # If this unclick occurs while the mouse is on the button
            # and not because it was dragged off the button
            if (mainPltBtn.rect.collidepoint(mouseX, mouseY)):
                mainPltBtn.draw()
                showPlot = True

            else:
                pass
    else:
        mainPltBtn.draw()

    # Updating the button state variables, allowing the states this frame to be used
    # in the next frame's comparison
    mainPgmButtons['openGraph'] = mainPltBtn.getPressed()

    # Drawing graph
    pg.draw.line(surface=screen, color=BLACK, start_pos=(40, 70), end_pos=(290, 70), width=7)
    pg.draw.line(surface=screen, color=BLACK, start_pos=(140, 30), end_pos=(140, HEIGHT - 60), width=7)

    # Drawing labels
    text = fontSubtitle60.render("x        y(x)", True, BLACK)
    screen.blit(text, (70, 20))

    # Drawing the initial information
    text = fontSubtitle50.render(f"F(x) = ", True, DARK_GRAY)
    screen.blit(text, (320, 50))
    text = fontSubtitle40.render(f"{fX}", True, LIME_GREEN)
    screen.blit(text, (420, 55))
    text = fontSubtitle50.render(f"Given (", True, DARK_GRAY)
    screen.blit(text, (320, 100))
    text = fontSubtitle50.render(f"{xBound}, {yBound}", True, LIME_GREEN)
    screen.blit(text, (440, 100))
    text = fontSubtitle50.render(")", True, DARK_GRAY)
    screen.blit(text, (410+getFontSize(f"{xBound}, {yBound}", 50, "arial.ttf")[0], 100))
    text = fontSubtitle50.render(f"h =", True, DARK_GRAY)
    screen.blit(text, (320, 150))
    text = fontSubtitle50.render(f"{hVal}", True, LIME_GREEN)
    screen.blit(text, (380, 150))
    text = fontSubtitle50.render(f"Looking for y(", True, DARK_GRAY)
    screen.blit(text, (320, 200))
    text = fontSubtitle50.render(f"{yAtX}", True, LIME_GREEN)
    screen.blit(text, (555, 200))
    text = fontSubtitle50.render(")", True, DARK_GRAY)
    screen.blit(text, (555+getFontSize(f"{yAtX}", 50, "arial.ttf")[0], 200))

    # Drawing instructions
    text = fontSubtitle40.render("Press GRAPH to see the", True, BLACK)
    screen.blit(text, (300, 310))
    text = fontSubtitle40.render("   graph. Close graph", True, BLACK)
    screen.blit(text, (300, 340))
    text = fontSubtitle40.render("   window when done!", True, BLACK)
    screen.blit(text, (300, 370))

    # Drawing values
    for i in range(0, min(10,len(coords))):
        text = fontSubtitle50.render(str(coords[len(coords)-(1+i)][0]), True, BLACK)
        screen.blit(text, (50, 75+i*35))
        text = fontSubtitle50.render(str(coords[len(coords)-(1+i)][1]), True, BLACK)
        screen.blit(text, (165, 75+i*35))

    # flip() is used to update the screen
    # tick() is used to regulate the framerate
    pg.display.flip()
    clock.tick(FRAMERATE)

    # MatPlotLib Plot Code
    # Creating the original plot points
    x_coords = []
    y_coords = []
    for c in coords:
        x_coords.append(c[0])
        y_coords.append(c[1])

    #Creating the x/y axes
    xC2 = []
    for i in x_coords:
        xC2.append(i)

    yC2 = []
    for i in y_coords:
        yC2.append(i)
    xC2.sort()
    try:
        yC2.sort()
    except:
        pass
    try:
        xAxis = [min(0,xC2[0]-(0.1*abs(xC2[0]))), max(0,xC2[len(xC2)-1]+(0.1*abs(yC2[len(xC2)-1])))]
    except:
        xAxis = [0,0]
    try:
        yAxis = [min(0,yC2[0]-(0.1*abs(yC2[0]))), max(0,yC2[len(yC2)-1]+(0.1*abs(yC2[len(yC2)-1])))]
    except:
        yAxis = [0,0]
    zeros = [0,0]


    #Plotting the axes
    plt.plot(xAxis, zeros, linestyle='dashed', color='black', linewidth=1)
    plt.plot(zeros, yAxis, linestyle='dashed', color='black', linewidth=1)

    #Plotting the original points
    plt.scatter(np.array(x_coords), np.array(y_coords))

    # Adding titles
    plt.title(f"Plot Data for {fX} from {xBound} to {yAtX}")
    plt.suptitle("Close this window to continue using the program!\n", fontsize='medium')
    plt.xlabel('x', fontweight='bold')
    plt.ylabel('y', fontweight='bold')

    # Drawing plot if plot draw button is pressed, stopping drawing plot when plot is closed by user
    if showPlot:
        plt.show()
        while (plt.get_fignums()):
            pass
        showPlot = False


#Main program loop
while isRunning:
    if screenOn == "main_menu": mainMenu()
    elif screenOn == "enter_info": enterInfoScreen()
    elif screenOn == "program": mainProgram()
    elif screenOn == "info": explanationMenu()
