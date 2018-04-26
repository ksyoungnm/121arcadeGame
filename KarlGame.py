from tkinter import font
from tkinter import *
from Game import Game
from geometry import Vector2D, Point2D, Bounds
from Projectile import Launcher
from time import sleep
from random import choice
from Agent import Controllable
from Interactables import SpeedUp

class KarlGame(Game):

    def __init__(self):

        super().__init__('KarlGame',80.0,60.0,800,600,topology='bound')

        self.wallwidth = 3.0
        self.wallbounds = self.bounds.scale_in(self.wallwidth)
        self.buttonList = []

        self.character = None
        self.cannons = []
        self.bullets = []
        self.walls = []
        self.pickups = []
        
        self.gameover = False
        self.pause = False
        self.speedTimer = 0

        self.highscore = 0
        self.lifetimeDeaths = 0
        self.lifetimeCoins = 0
        self.lifetimeShields = 0
        self.lifetimeGuns = 0

        self.bind_all('<KeyPress>',self.keypress)
        self.bind_all('<KeyRelease>',self.keyrelease)

        self.overFrame = Frame(self,bg='#690087',highlightcolor='white',highlightthickness=0)

        self.makeLabels()
        self.makeButtons()

        self.startMenu(None)

        self.root.mainloop()

    def makeLabels(self):

        self.typefont = font.Font(family='American Typewriter')
        self.boldfont = font.Font(weight='bold')
        self.gameFont = font.Font(family='Copperplate',slant='italic',size=28)
        self.authorFont = font.Font(family='Courier New',slant='italic',size=14)
        self.welcomefont = font.Font(family='Courier New')

        self.startLabel = Label(self.overFrame,
            text='Welcome To',bg='#690087',fg='white',
            font=self.authorFont
            )
        self.gameLabel = Label(self.overFrame,
            text='Dodger',bg='#690087',fg='white',
            font=self.gameFont
            )
        self.authorLabel = Label(self.overFrame,
            text='by Karl Young\n\n',bg='#690087',fg='white',
            font=self.authorFont
            )
        self.controlsLabel = Label(self.overFrame,
            text='Move Up: '+'\u2191'+'\n'+
            'Move Down: '+'\u2193'+'\n'+
            'Move Left: '+'\u2190'+'\n'+
            'Move Right: '+'\u2192'+'\n\n'+
            "Pause: Space or 'Esc'",
            bg='purple',fg='white'
            )
        self.statsLabel = Label(self.overFrame,
            text='Highscore: '+str(self.highscore),
            bg='#5230ff',fg='white'
            )
        self.statsLabel2 = Label(self.overFrame,
            text='\n\n\nLifetime',
            bg='#5230ff',fg='white',
            font=self.boldfont
            )
        self.statsLabel3 = Label(self.overFrame,
            text='Deaths: '+str(self.lifetimeDeaths)+
            '\n\nCoins Collected: '+str(self.lifetimeCoins)+
            '\nShields Broken: '+str(self.lifetimeShields)+
            '\nGuns Destroyed: '+str(self.lifetimeGuns),
            bg='#5230ff',fg='white'
            )
        self.restartLabel = Label(self.overFrame,
            text='Game Over!',bg='black',fg='white'
            )
        self.quitLabel = Label(self.overFrame,
            text='Are you sure?\nAll data will be lost.',
            bg='black',fg='white'
            )

    def makeButtons(self):

        self.startButton = Label(self.overFrame,
            text='Play Game', bg='#690087',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.startButton.bind('<Button-1>',self.startGame)
        self.buttonList.append(self.startButton)

        self.controlsButton = Label(self.overFrame,
            text='Controls',bg='#690087',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.controlsButton.bind('<Button-1>',self.controlMenu)
        self.buttonList.append(self.controlsButton)

        self.statsButton = Label(self.overFrame,
            text='Stats',bg='#690087',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.statsButton.bind('<Button-1>',self.statsMenu)
        self.buttonList.append(self.statsButton)
        
        self.restartButton = Label(self.overFrame,
            text='Play Again',bg='black',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.restartButton.bind('<Button-1>',self.startGame)
        self.buttonList.append(self.restartButton)

        self.remenuButton = Label(self.overFrame,
            text='Main Menu',bg='black',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.remenuButton.bind('<Button-1>',self.startMenu)
        self.buttonList.append(self.remenuButton)

        self.quitButton = Label(self.overFrame,
            text='Quit',bg='black',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.quitButton.bind('<Button-1>',self.quitMenu)
        self.buttonList.append(self.quitButton)

        self.confirmButton = Label(self.overFrame,
            text='Yes',bg='black',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.confirmButton.bind('<Button-1>',self.quit)
        self.buttonList.append(self.confirmButton)

        self.returnButton = Label(self.overFrame,
            text='No',bg='black',fg='white',
            highlightthickness=2,highlightcolor='white'
            )
        self.returnButton.bind('<Button-1>',self.startMenu)
        self.buttonList.append(self.returnButton)

        for button in self.buttonList:
            button.bind('<Enter>',self.enterExit)
            button.bind('<Leave>',self.enterExit)

    def quitMenu(self,event):
        self.canvas.delete('menu')
        for widget in self.overFrame.winfo_children():
            widget.grid_forget()

        canvasbg = self.canvas.cget('background')

        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame,tags='menu')

        self.quitLabel.configure(bg=canvasbg)
        self.confirmButton.configure(bg=canvasbg,fg='white')
        self.returnButton.configure(bg=canvasbg,fg='white')

        self.quitLabel.grid(row=0,column=0,columnspan=2,sticky='ew')
        self.confirmButton.grid(row=1,column=0,padx=0.5,sticky='ew')
        self.returnButton.grid(row=1,column=1,padx=0.5,sticky='ew')

        self.overFrame.focus_set()
        Frame.update(self)

    def quit(self,event):
        self.root.destroy()

    def set_character_speed(self,amount,duration):
        self.character.MAX_SPEED = amount
        self.speedTimer = duration

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
        self.quitButton.configure(bg='#690087',fg='white')

        self.startLabel.grid(row=0,pady=0,sticky='ew')
        self.gameLabel.grid(row=1,pady=0,sticky='ew')
        self.authorLabel.grid(row=2,pady=0,sticky='ew')
        self.startButton.grid(row=3,pady=1,sticky='ew')
        self.controlsButton.grid(row=4,pady=1,sticky='ew')
        self.statsButton.grid(row=5,pady=1,sticky='ew')
        self.quitButton.grid(row=6,pady=1,sticky='ew')

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

        self.statsLabel.configure(text='Highscore: '+str(self.highscore))
        self.statsLabel3.configure(
            text=
            'Deaths: '+str(self.lifetimeDeaths)+
            '\n\nCoins Collected: '+str(self.lifetimeCoins)+
            '\nShields Broken: '+str(self.lifetimeShields)+
            '\nGuns Destroyed: '+str(self.lifetimeGuns)
            )
        self.remenuButton.configure(bg='#5230ff',fg='white')


        self.statsLabel.grid(row=0,sticky='ew')
        self.statsLabel2.grid(row=1,sticky='ew')
        self.statsLabel3.grid(row=2,sticky='ew')
        self.remenuButton.grid(row=3,pady=4,sticky='ew')
        
        self.overFrame.focus_set()
        Frame.update(self)

    def restartMenu(self):
        for widget in self.overFrame.winfo_children():
            widget.grid_forget()

        self.overFrame.configure(bg='black')

        self.canvas.create_text(400,262,text='Game Over!',fill='white')
        self.overFrameobj = self.canvas.create_window(self.WINDOW_WIDTH/2,self.WINDOW_HEIGHT/2,window = self.overFrame,tags='menu')

        self.restartButton.configure(bg='black',fg='white')
        self.remenuButton.configure(bg='black',fg='white')

        self.restartButton.grid(row=1,pady=1,sticky='ew')
        self.remenuButton.grid(row=2,pady=1,sticky='ew')

        self.overFrame.focus_set()
        Frame.update(self)

    def pauseMenu(self,event):
        self.pause = not self.pause
        if self.gameover:
            return
        if self.pause:
            self.canvas.create_text(400,300,text="PAUSE\nPress "+event.keysym.capitalize()+" to resume.",fill='white',justify='center',tags='pause')
            self.root.mainloop()
        else:
            self.canvas.delete('pause')
            self.runGame()

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
        overlapping = self.canvas.find_overlapping(b[0][0],b[0][1],b[1][0],b[1][1])
        for thing in overlapping:
            tags = self.canvas.gettags(thing)
            if 'bullets' in tags:
                self.gameover = True
                return
            elif 'Pickup' in tags:
                for pick in self.pickups:
                    if thing == pick.selfID:
                        pick.effect()
                        break

        Frame.update(self)

    def keypress(self,event):
        pass

    def keyrelease(self,event):
        pass

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

    def makeGuns(self):
        for i in range(-20,40,20):
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymin),Vector2D(0.0,1.0),self))
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymax),Vector2D(0.0,-1.0),self))
        for k in range(3):
            kr = (k-1)*15
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmin,float(kr)),Vector2D(1.0,0.0),self))
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmax,float(kr)),Vector2D(-1.0,0.0),self))

    def makeScoreLabel(self):
        self.scoreLabel = self.canvas.create_text(
            750,45,text='Score: 0',fill='white',
            font=self.typefont,anchor='ne'
            )
        self.highscoreLabel = self.canvas.create_text(
            750,60,text='Highscore: '+str(self.highscore),
            fill='white',font=self.typefont,anchor='ne'
            )

    def makeBackdrop(self):
        self.canvas.create_rectangle(
            (0,0),(self.WINDOW_WIDTH+1,self.WINDOW_HEIGHT+1),
            fill='#000000',tags='backdrop'
            )

    def startGame(self,event):

        self.gameover = False
        self.character = None
        self.newHighscore = False
        self.cannons = []
        self.bullets = []
        self.walls = []
        self.pickups = []
        self.canvas.delete('all')


        self.makeBackdrop()
        self.makeScoreLabel()
        self.makeWalls()
        self.makeGuns()

        self.bind('<KeyPress-Escape>',self.pauseMenu)
        self.bind('<KeyPress- >',self.pauseMenu)

        self.character = Controllable(Point2D(),1.0,self)

        self.counter = 0
        self.score = 0

        self.runGame()

    def runGame(self):
        g=SpeedUp(Point2D(10,10),'green',self)

        while not self.gameover:
            # if self.counter % 10 == 5:
            #     choice(self.cannons).fire()
            self.canvas.itemconfigure(self.scoreLabel,text='Score: '+str(self.score))
            if self.score > self.highscore:
                self.newHighscore = True
                self.highscore = self.score
                self.canvas.itemconfigure(self.highscoreLabel,text='Highscore: '+str(self.highscore))
            if self.speedTimer > 0:
                self.speedTimer -= 1
            self.counter += 1
            self.score += 1
            sleep(1.0/60.0)
            self.update()

        self.lifetimeDeaths += 1
        
        if self.newHighscore:
            self.canvas.create_text(
                400,225,text='New Highscore! Congrats!\nScore: '+str(self.highscore),fill='white',justify='center')

        self.bind_all('<KeyPress>',self.keypress)
        self.bind_all('<KeyRelease>',self.keyrelease)
        self.restartMenu()
        self.root.mainloop()

game = KarlGame()