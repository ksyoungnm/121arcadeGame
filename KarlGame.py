from tkinter import *
from Game import Game
from geometry import Vector2D, Point2D, Bounds
# from Projectile import Launcher
from time import sleep
# from random import choice
from Agent import controllable

class KarlGame(Game):

    def __init__(self):

        super().__init__('KarlGame',80.0,60.0,800,600,topology='bound')

        self.wallwidth = 3.0
        self.wallbounds = self.bounds.scale_in(self.wallwidth)

        self.character = None
        self.cannons = []
        self.bullets = []
        self.walls = []
        
        self.gameover = False
        self.pause = False

        self.overFrame = Frame(self)
        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame)

        Label(self.overFrame,text='Hello!',background='yellow').grid(row=0)
        Button(self.overFrame,text='Play Game',command=self.startGame).grid(row=1)

        # Label(self.overMenu,text='GAME OVER',background='green').grid(row=0)
        # Button(self.overMenu,text='Restart?',command=self.startGame).grid(row=1)
        # Button(self.overMenu,text='Main Menu',command=self.mainMenu).grid(row=2)

        # self.startMenu.grid()
        self.root.mainloop()

    def update(self):
        self.character.update()
        self.canvas.delete('agent')
        self.draw_poly(self.character.shape(),self.character.color(),'agent')
        Frame.update(self)

    def keypress(self,event):
        if event.keysym == 'Up':
            self.character.change_direction(True,self.character.UP_VECTOR)
        if event.keysym == 'Down':
            self.character.change_direction(True,self.character.DOWN_VECTOR)
        if event.keysym == 'Left':
            self.character.change_direction(True,self.character.LEFT_VECTOR)
        if event.keysym == 'Right':
            self.character.change_direction(True,self.character.RIGHT_VECTOR)
        if event.keysym == 'Escape':
            self.pause = True
        if event.char == 'q':
            self.gameover = True

    def keyrelease(self,event):
        if event.keysym == 'Up':
            self.character.change_direction(False,self.character.UP_VECTOR)
        if event.keysym == 'Down':
            self.character.change_direction(False,self.character.DOWN_VECTOR)
        if event.keysym == 'Left':
            self.character.change_direction(False,self.character.LEFT_VECTOR)
        if event.keysym == 'Right':
            self.character.change_direction(False,self.character.RIGHT_VECTOR)

    def twopointBox(self,topleft,botright):
        p1 = topleft
        p2 = Point2D(botright.x,topleft.y)
        p3 = botright
        p4 = Point2D(topleft.x,botright.y)
        return [p1,p2,p3,p4]

    def makeWalls(self):
        side = float(self.bounds.xmax)
        top = float(self.bounds.ymax)
        wide = float(self.wallwidth)

        w1 = self.worldToWall([Point2D(-side,top),Point2D(side,top-wide)])
        w2 = self.worldToWall([Point2D(side-wide,top-wide),Point2D(side,-top+wide)])
        w3 = self.worldToWall([Point2D(-side,-top+wide),Point2D(side,-top)])
        w4 = self.worldToWall([Point2D(-side,top-wide),Point2D(-side+wide,-top+wide)])

        self.walls.append(self.canvas.create_rectangle(w1, fill='#FFFFFF',tags='wall'))
        self.walls.append(self.canvas.create_rectangle(w2, fill='#FFFFFF',tags='wall'))
        self.walls.append(self.canvas.create_rectangle(w3, fill='#FFFFFF',tags='wall'))
        self.walls.append(self.canvas.create_rectangle(w4, fill='#FFFFFF',tags='wall'))

    # def gameoverscreen(self):
    #     self.overFrame = Frame(self.root)
    #     Label(self.overFrame,text='GAME OVER',background='green').grid(row=0)
    #     Button(self.overFrame,text='restart',command=self.newstart).grid(row=1)
        
    #     self.canvas.create_window(self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT//2,window=self.overFrame)
        
    #     self.root.mainloop()

    def startGame(self):

        self.gameover = False
        self.character = None
        self.cannons = []
        self.bullets = []
        self.walls = []

        self.canvas.delete('all')
        self.canvas.create_rectangle((0,0),(self.WINDOW_WIDTH,self.WINDOW_HEIGHT),fill='#000000',tags='backdrop')

        self.makeWalls()

        self.character = controllable(Point2D(),0.6,self)

        while True:
            sleep(1.0/60.0)
            self.update()

        # for i in range(-15,30,15):
        #     self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymin),Vector2D(0.0,1.0),self))
        #     self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymax),Vector2D(0.0,-1.0),self))
        # for k in range(3):
        #     kr = (k-1)*11.25
        #     self.cannons.append(Launcher(Point2D(self.wallbounds.xmin,float(kr)),Vector2D(1.0,0.0),self))
        #     self.cannons.append(Launcher(Point2D(self.wallbounds.xmax,float(kr)),Vector2D(-1.0,0.0),self))
        

        # self.update()
        # sleep(1.0)
        # counter = 0
        # while not self.gameover:
        #     if counter == 10:
        #         choice(self.cannons).fire()
        #         counter = 0
        #     sleep(1.0/60.0)
        #     self.update()
        #     counter += 1
        # self.gameoverscreen()

game = KarlGame()