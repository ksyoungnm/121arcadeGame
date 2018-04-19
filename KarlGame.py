from tkinter import *
from Game import Game
from geometry import Vector2D, Point2D, Bounds
from Projectile import Launcher
from time import sleep
# from random import choice
from Agent import Controllable

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

        self.overFrame = Frame(self,bg='purple')
        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame)

        Label(self.overFrame,text='Hello!',bg='purple',fg='white').grid(row=0)
        fl = Label(self.overFrame,text='Play Game',background='purple',foreground='white')
        fl.grid(row=1)
        fl.bind('<Enter>',self.enterExit)
        fl.bind('<Leave>',self.enterExit)
        fl.bind('<Button-1>',self.startGame)

        # Label(self.overMenu,text='GAME OVER',background='green').grid(row=0)
        # Button(self.overMenu,text='Restart?',command=self.startGame).grid(row=1)
        # Button(self.overMenu,text='Main Menu',command=self.mainMenu).grid(row=2)

        # self.startMenu.grid()
        self.root.mainloop()

    def enterExit(self,event):
        e = event.widget
        bg = e.cget('background')
        fg = e.cget('foreground')
        e.configure(background=fg,foreground=bg)

    def update(self):
        self.character.update()
        self.canvas.delete('agent')
        full_points = self.character.shape()
        self.drawagent([full_points[0],full_points[2]],self.character.color())

        for gun in self.cannons:
            gun.update()
        self.canvas.delete('guns')
        for gun in self.cannons:
            self.draw_poly(gun.shape(),gun.color(),'guns')

        for missile in self.bullets:
            missile.update()
        self.canvas.delete('bullets')
        for missile in self.bullets:
            self.draw_poly(missile.shape(),missile.color(),'bullets')

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

    # def twopointBox(self,topleft,botright):
    #     p1 = topleft
    #     p2 = Point2D(botright.x,topleft.y)
    #     p3 = botright
    #     p4 = Point2D(topleft.x,botright.y)
    #     return [p1,p2,p3,p4]

    def makeWalls(self):
        ww = self.WINDOW_WIDTH
        wh = self.WINDOW_HEIGHT
        wide = self.wallwidth * wh/self.bounds.height()

        w1 = [(0,0),(ww+1,wide+1)]
        w2 = [(ww-wide,wide),(ww+1,wh-wide+1)]
        w3 = [(0,wh-wide),(ww+1,wh+1)]
        w4 = [(0,wide),(wide+1,wh-wide+1)]
        
        self.walls.append(self.canvas.create_rectangle(w1, fill='#FFFFFF',width=0,tags='wall'))
        self.walls.append(self.canvas.create_rectangle(w2, fill='#FFFFFF',width=0,tags='wall'))
        self.walls.append(self.canvas.create_rectangle(w3, fill='#FFFFFF',width=0,tags='wall'))
        self.walls.append(self.canvas.create_rectangle(w4, fill='#FFFFFF',width=0,tags='wall'))

    # def gameoverscreen(self):
    #     self.overFrame = Frame(self.root)
    #     Label(self.overFrame,text='GAME OVER',background='green').grid(row=0)
    #     Button(self.overFrame,text='restart',command=self.newstart).grid(row=1)
        
    #     self.canvas.create_window(self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT//2,window=self.overFrame)
        
    #     self.root.mainloop()

    def startGame(self,event):

        self.gameover = False
        self.character = None
        self.cannons = []
        self.bullets = []
        self.walls = []

        self.canvas.delete('all')
        self.canvas.create_rectangle((0,0),(self.WINDOW_WIDTH+1,self.WINDOW_HEIGHT+1),fill='#000000',tags='backdrop')

        self.makeWalls()

        self.character = Controllable(Point2D(),1.0,self)

        for i in range(-15,30,15):
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymin),Vector2D(0.0,1.0),self))
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymax),Vector2D(0.0,-1.0),self))
        for k in range(3):
            kr = (k-1)*11.25
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmin,float(kr)),Vector2D(1.0,0.0),self))
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmax,float(kr)),Vector2D(-1.0,0.0),self))

            
        while True:
            sleep(1.0/60.0)
            self.update()

        

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