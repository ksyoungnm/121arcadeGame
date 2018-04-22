from tkinter import font
from tkinter import *
from Game import Game
from geometry import Vector2D, Point2D, Bounds
from Projectile import Launcher
from time import sleep
from random import choice
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

        self.highscore = 0

        self.overFrame = Frame(self,bg='#690087',highlightcolor='white',highlightthickness=0)
        self.typefont = font.Font(family='American Typewriter')

        self.startLabel = Label(self.overFrame,text='Hello!',bg='#690087',fg='white')

        self.controlsLabel = Label(self.overFrame,text='up:up\ndown:down\nleft:left\nright:right',bg='purple',fg='white')

        self.statsLabel = Label(self.overFrame,text='highscore:\ndeaths:\ncoins collected:\nshields broken:\nguns destroyed:',bg='#5230ff',fg='white')

        self.restartLabel = Label(self.overFrame,text='Game Over!',bg='black',fg='white')


        self.startButton = Label(self.overFrame,text='Play Game',bg='#690087',fg='white',highlightthickness=2,highlightcolor='white')
        self.startButton.bind('<Enter>',self.enterExit)
        self.startButton.bind('<Leave>',self.enterExit)
        self.startButton.bind('<Button-1>',self.startGame)

        self.controlsButton = Label(self.overFrame,text='Controls',bg='#690087',fg='white',highlightthickness=2,highlightcolor='white')
        self.controlsButton.bind('<Enter>',self.enterExit)
        self.controlsButton.bind('<Leave>',self.enterExit)
        self.controlsButton.bind('<Button-1>',self.controlMenu)

        self.statsButton = Label(self.overFrame,text='Stats',bg='#690087',fg='white',highlightthickness=2,highlightcolor='white')
        self.statsButton.bind('<Enter>',self.enterExit)
        self.statsButton.bind('<Leave>',self.enterExit)
        self.statsButton.bind('<Button-1>',self.statsMenu)

        self.restartButton = Label(self.overFrame,text='Play Again',bg='black',fg='white',highlightthickness=2,highlightcolor='white')
        self.restartButton.bind('<Enter>',self.enterExit)
        self.restartButton.bind('<Leave>',self.enterExit)
        self.restartButton.bind('<Button-1>',self.startGame)

        self.remenuButton = Label(self.overFrame,text='Main Menu',bg='black',fg='white',highlightthickness=2,highlightcolor='white')
        self.remenuButton.bind('<Enter>',self.enterExit)
        self.remenuButton.bind('<Leave>',self.enterExit)
        self.remenuButton.bind('<Button-1>',self.startMenu)

        self.startMenu(None)

        self.root.mainloop()

    def startMenu(self,event):
        self.canvas.delete('all')
        for widget in self.overFrame.winfo_children():
            widget.grid_forget()

        self.canvas.configure(bg='#690087')
        self.overFrame.configure(bg='#690087')
        
        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame,tags='menu')

        self.startButton.configure(bg='#690087',fg='white')
        self.controlsButton.configure(bg='#690087',fg='white')
        self.statsButton.configure(bg='#690087',fg='white')

        self.startLabel.grid(row=0,pady=4,sticky='ew')
        self.startButton.grid(row=1,pady=1,sticky='ew')
        self.controlsButton.grid(row=2,pady=1,sticky='ew')
        self.statsButton.grid(row=3,pady=1,sticky='ew')

        self.overFrame.focus_set()
        Frame.update(self)

    def controlMenu(self,event):
        self.canvas.delete('all')
        for widget in self.overFrame.winfo_children():
            widget.grid_forget()

        self.canvas.configure(bg='purple')
        self.overFrame.configure(bg='purple')
        
        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame,tags='menu')

        self.remenuButton.configure(bg='purple',fg='white')

        self.controlsLabel.grid(row=0,pady=4,sticky='ew')
        self.remenuButton.grid(row=1,pady=1,sticky='ew')
        
        self.overFrame.focus_set()
        Frame.update(self)

    def statsMenu(self,event):
        self.canvas.delete('all')
        for widget in self.overFrame.winfo_children():
            widget.grid_forget()

        self.canvas.configure(bg='#5230ff')
        self.overFrame.configure(bg='#5230ff')
        
        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame,tags='menu')

        self.remenuButton.configure(bg='#5230ff',fg='white')

        self.statsLabel.grid(row=0,pady=4,sticky='ew')
        self.remenuButton.grid(row=1,pady=1,sticky='ew')
        
        self.overFrame.focus_set()
        Frame.update(self)

    def restartMenu(self):
        for widget in self.overFrame.winfo_children():
            widget.grid_forget()

        self.overFrame.configure(bg='black')

        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame,tags='menu')

        self.restartButton.configure(bg='black',fg='white')
        self.remenuButton.configure(bg='black',fg='white')

        self.restartLabel.grid(row=0,pady=4,sticky='ew')
        self.restartButton.grid(row=1,pady=1,sticky='ew')
        self.remenuButton.grid(row=2,pady=1,sticky='ew')

        self.overFrame.focus_set()
        Frame.update(self)

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
            self.draw_oval(missile.shape(),missile.color(),'bullets')

        b = self.worldToPixel([full_points[0],full_points[2]])
        l = self.canvas.find_overlapping(b[0][0],b[0][1],b[1][0],b[1][1])
        for thing in l:
            if 'bullets' in self.canvas.gettags(thing):
                self.gameover = True
                return
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

    def startGame(self,event):

        self.gameover = False
        self.character = None
        self.cannons = []
        self.bullets = []
        self.walls = []

        self.canvas.delete('all')
        self.canvas.create_rectangle((0,0),(self.WINDOW_WIDTH+1,self.WINDOW_HEIGHT+1),fill='#000000',tags='backdrop')

        self.scoreLabel = self.canvas.create_text(750,45,text='Score: 0',fill='white',font=self.typefont,anchor='ne')
        self.highscoreLabel = self.canvas.create_text(750,60,text='Highscore: '+str(self.highscore),fill='white',font=self.typefont,anchor='ne')

        self.makeWalls()

        self.character = Controllable(Point2D(),1.0,self)

        for i in range(-20,40,20):
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymin),Vector2D(0.0,1.0),self))
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymax),Vector2D(0.0,-1.0),self))
        for k in range(3):
            kr = (k-1)*15
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmin,float(kr)),Vector2D(1.0,0.0),self))
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmax,float(kr)),Vector2D(-1.0,0.0),self))


        counter = 0
        score = 0
        highscore = self.highscore

        while not self.gameover:
            if counter % 10 == 5:
                choice(self.cannons).fire()
            self.canvas.itemconfigure(self.scoreLabel,text='Score: '+str(score))
            if score > highscore:
                highscore = score
                self.canvas.itemconfigure(self.highscoreLabel,text='Highscore: '+str(highscore))
            counter += 1
            score += 1
            sleep(1.0/60.0)
            self.update()

        self.highscore = highscore

        self.restartMenu()
        self.root.mainloop()

game = KarlGame()