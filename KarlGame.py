from tkinter import *
from Game import Game
from geometry import Vector2D, Point2D, Bounds
from Projectile import Launcher
from time import sleep
from Walls import Walls
from random import choice
from Agent import controllable

class KarlGame(Game):

    def __init__(self,wallwidth):

        super().__init__('KarlGame',60.0,45.0,800,600,topology='bound')

        
        self.wallbounds = self.bounds.scale_in(wallwidth)


        self.wallwidth = wallwidth


        self.cannons = []

        
        self.gameover = False
        self.pause = False

        Label(self.startMenu,text='Hello!',background='yellow').grid(row=0)
        Button(self.startMenu,text='Play Game',command=self.startGame).grid(row=1)
        self.startMenu.grid()
        self.root.mainloop()

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

    def walltrim(self,agent):
        agent.position = self.wallbounds.hitboxtrim(agent)

    def gameoverscreen(self):
        self.overFrame = Frame(self.root)
        Label(self.overFrame,text='GAME OVER',background='green').grid(row=0)
        Button(self.overFrame,text='restart',command=self.newstart).grid(row=1)
        
        self.canvas.create_window(self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT//2,window=self.overFrame)
        
        self.root.mainloop()

    def newstart(self):
        self.gameover = False
        self.PlayGame()

    def startGame(self):

        self.gameover = False

        self.startMenu = 
        self.agents = []
        self.cannons = []

        self.wall = Walls(self.wallwidth,self)



        self.character = controllable(Point2D(),0.6,self)
        for i in range(-15,30,15):
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymin),Vector2D(0.0,1.0),self))
        for j in range(-15,30,15):
            self.cannons.append(Launcher(Point2D(float(j),self.wallbounds.ymax),Vector2D(0.0,-1.0),self))
        for k in range(3):
            kr = (k-1)*11.25
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmin,float(kr)),Vector2D(1.0,0.0),self))
        for l in range(3):
            lr = (l-1)*11.25
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmax,float(lr)),Vector2D(-1.0,0.0),self))
        self.gameover = False
        self.update()
        sleep(1.0)
        counter = 0
        while not self.gameover:
            if counter == 10:
                choice(self.cannons).fire()
                counter = 0
            sleep(1.0/60.0)
            self.update()
            counter += 1
        self.gameoverscreen()

game = KarlGame(3.0)
game.PlayGame()