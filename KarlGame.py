from tkinter import font
from tkinter import *
from Game import Game
from geometry import Vector2D, Point2D, Bounds
from Projectile import Launcher
from time import sleep
from random import choice,random,getrandbits
from Agent import Controllable
from Interactables import SpeedUp,SpeedDown,Coin

class KarlGame(Game):

    def __init__(self):

        super().__init__('KarlGame',80.0,60.0,800,600,topology='bound')


        #Initiates walls and wall boundaries.
        self.wallwidth = 3.0
        self.wallbounds = self.bounds.scale_in(self.wallwidth)
        
        #Initiates other objects to be updated.
        self.character = None
        self.cannons = []
        self.bullets = []
        self.walls = []
        self.pickups = []
        self.buttonList = []

        #Setting other gameplay variables.
        self.bullet_speed = 0.3
        self.FIRE_RATE = 10

        #Initializes other gameplay state variables.
        self.score = 0
        self.highscore = 0
        self.gameover = False
        self.pause = False
        self.counter = 0
        self.speedTimer = 0

        #Initializes variables to track lifetime stats.
        self.lifetimeDeaths = 0
        self.lifetimeCoins = 0
        self.lifetimeTimes = 0
        
        #Binds all keys presses and key releases to an empty function, so pressing random'
        #buttons won't have an effect.
        self.bind_all('<KeyPress>',self.keypress)
        self.bind_all('<KeyRelease>',self.keyrelease)

        #I use this frame to add Labels and Buttons, etc. to the canvas so I can make menus, etc.
        self.overFrame = Frame(self,bg='#690087',highlightcolor='white',highlightthickness=0)

        #Initializes said Labels and Buttons
        self.makeLabels()
        self.makeButtons()

        #creates the start menu, runs mainloop to wait for user input.
        self.startMenu(None)
        self.root.mainloop()

    def keypress(self,event):
        pass

    def keyrelease(self,event):
        pass

    def quit(self,event):
        #Used by the quit menu to exit the application.
        self.root.destroy()

    def set_character_speed(self,amount,duration):
        #should be fairly self explanatory. Starts a timer,changes char.speed.
        self.character.MAX_SPEED = amount
        self.speedTimer = duration

    def update(self):
        #Default behavior was to just update and redraw everyone, but since I used a draw_poly
        #and a draw_oval method, I just update everything explicitly.
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

        #So hitboxes were something I struggled with until I found this. Instead of having those
        #actual world objects trying to detect collision, I just let the canvas widget do its thing
        #with the find_overlapping method. Huge plus is I don't have to write out the collisions
        #myself, and it gets rid of the funkyness involving overlapping ovals with polygons!
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

    def makeWalls(self):
        #I once had dreams of coding a level in which the walls would move around and pulsate,
        #but those have since died. I just draw em once at the beggining of the game and leave
        #em. No use in updating if their not moving right?
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
        #should be pretty self explanatory I hope.
        for i in range(-20,40,20):
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymin),Vector2D(0.0,1.0),self))
            self.cannons.append(Launcher(Point2D(float(i),self.wallbounds.ymax),Vector2D(0.0,-1.0),self))
        for k in range(3):
            kr = (k-1)*15
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmin,float(kr)),Vector2D(1.0,0.0),self))
            self.cannons.append(Launcher(Point2D(self.wallbounds.xmax,float(kr)),Vector2D(-1.0,0.0),self))

    def makeScoreLabel(self):
        #initializes the score label
        self.scoreLabel = self.canvas.create_text(
            750,45,text='Score: 0',fill='white',
            font=self.typefont,anchor='ne'
            )
        self.highscoreLabel = self.canvas.create_text(
            750,60,text='Highscore: '+str(self.highscore),
            fill='white',font=self.typefont,anchor='ne'
            )

    def makeBackdrop(self):
        #makes the backdrop. totally unnecessary to be a separate function but for data abstractions sake and
        #so all the 'make' functions in the startGame method could look nice together.
        self.canvas.create_rectangle(
            (0,0),(self.WINDOW_WIDTH+1,self.WINDOW_HEIGHT+1),
            fill='#000000',tags='backdrop'
            )

    def startGame(self,event):

        #Have to reinitialize all of the important variables so the restart function will work.
        self.gameover = False
        self.character = None
        self.newHighscore = False
        self.bullet_speed = 0.4
        self.cannons = []
        self.bullets = []
        self.walls = []
        self.pickups = []
        self.FIRE_RATE = 10
        
        self.canvas.delete('all')

        #makes all of the background canvas objects
        self.makeBackdrop()
        self.makeScoreLabel()
        self.makeWalls()
        self.makeGuns()

        #binds the pause menu keys
        self.bind_all('<KeyPress-Escape>',self.pauseMenu)
        self.bind_all('<KeyPress- >',self.pauseMenu)

        #makes the controllable player character
        self.character = Controllable(Point2D(),1.0,self)

        #initializes the keeping track of things variables
        self.counter = 0
        self.score = 0

        self.runGame()

    def runGame(self):

        while not self.gameover:

            #game gradually gets harder as the bullets get faster and the guns fire quicker.
            #probably could have done this more elegantly but I'm running low on time, and it's
            #good enough.
            if self.counter == 450:
                self.bullet_speed = 0.45
                self.FIRE_RATE = 9
            elif self.counter == 900:
                self.bullet_speed = 0.5
                self.FIRE_RATE = 8
            elif self.counter == 1350:
                self.bullet_speed = 0.55
                self.FIRE_RATE = 6
            elif self.counter == 900:
                self.bullet_speed = 0.6
                self.FIRE_RATE = 4

            #fires a random gun every so often
            if self.counter % self.FIRE_RATE == 1:
                choice(self.cannons).fire()

            #generates powerups/coins. Is completely random. probably could have done this a little
            #more elegantly as well but eh oh well.
            if random() > 0.995:
                if bool(getrandbits(1)):
                    Coin(Point2D.random(self.wallbounds),'yellow',self)
                elif bool(getrandbits(1)):
                    SpeedDown(Point2D.random(self.wallbounds),'green',self)
                else:
                    SpeedUp(Point2D.random(self.wallbounds),'green',self)

            #sets the score so its visible on the screen
            self.canvas.itemconfigure(self.scoreLabel,text='Score: '+str(self.score))
            if self.score > self.highscore:
                self.newHighscore = True
                self.highscore = self.score
                self.canvas.itemconfigure(self.highscoreLabel,text='Highscore: '+str(self.highscore))

            #deals with the powerup timer and resets bullet/character speed when it expires. Also would have
            #liked to integrate this more cleanly with the scaling difficulty but oh well.
            if self.speedTimer > 1:
                self.speedTimer -= 1
            elif self.speedTimer == 1:
                self.set_character_speed(0.5,0)
                if self.counter > 900:
                    self.bullet_speed = 0.6
                else:
                    self.bullet_speed = 0.5

            #updates the important stuff
            self.counter += 1
            self.score += 1
            sleep(1.0/60.0)
            self.update()

        #stuff following this point happens after the game loop has exited, i.e. when the character is
        #hit with a bullet. display a highscore message, rebinds the control keys to an empty function
        #so the game doesn't freak out while you're messing around in the menus. Also makes the restart
        #menu.
        self.lifetimeDeaths += 1
        
        if self.newHighscore:
            self.canvas.create_text(
                400,225,text='New Highscore! Congrats!\nScore: '+str(self.highscore),fill='white',justify='center')

        self.bind_all('<KeyPress>',self.keypress)
        self.bind_all('<KeyRelease>',self.keyrelease)

        self.restartMenu()
        self.root.mainloop()



    #Stuff following this is configuration and settings for the tkinter menus and windows junk. Not
    #super interesting to read nor to comment on, so I'll try to do little summaries at the top of each section
    #instead.


    #Labels are fairly self-explanatory, they just display text. (as opposed to the buttons I make later,
    #which are technically labels bound to mouse events to make them buttons.)

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
            '\nTimelines Dialated: '+str(self.lifetimeTimes),
            bg='#5230ff',fg='white'
            )
        self.restartLabel = Label(self.overFrame,
            text='Game Over!',bg='black',fg='white'
            )
        self.quitLabel = Label(self.overFrame,
            text='Are you sure?\nAll data will be lost.',
            bg='black',fg='white'
            )

        #As mentioned above, buttons aren't configurable so I made these as Labels and bound
        #the entry/exit of the mouse to change the highlight pattern of the Label. Also bound
        #a button press to associated menus. Looks pretty good actually.
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

    #The Menu functions I'm also pretty proud of. Each is just an alteration of the background canvas by adding
    #a window object and gridding the associated Labels/Buttons into that window. Restart Menu doen't clear the background 
    #Canvas so you can see how you died. Thought it was a nice touch :)

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
            '\nTimelines Dialated: '+str(self.lifetimeTimes)
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

    def enterExit(self,event):
        #Because regular button widgets aren't configurable, I made my labels into buttons instead.
        #This happens when you hover over a 'button' so it looks nice.
        e = event.widget
        bg = e.cget('background')
        fg = e.cget('foreground')
        e.configure(background=fg,foreground=bg)

game = KarlGame()