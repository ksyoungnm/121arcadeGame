from Game import *
from geometry import Vector2D
from Projectile import Launcher
from time import sleep

TIME_STEP = 0.5

class controllable(Agent):

    MAX_SPEED = 0.5

    UP_VECTOR = Vector2D(0.0,1.0)
    DOWN_VECTOR = Vector2D(0.0,-1.0)
    LEFT_VECTOR = Vector2D(-1.0,0.0)
    RIGHT_VECTOR = Vector2D(1.0,0.0)

    def __init__(self,position,size,world):
        super().__init__(position,world)
        self.size = size
        self.hit_radius = 0.4

    def shape(self):
        upperright = self.position + Vector2D(self.size/2,self.size/2)
        lowerright = self.position + Vector2D(-self.size/2,self.size/2)
        lowerleft = self.position + Vector2D(-self.size/2,-self.size/2)
        upperleft = self.position + Vector2D(self.size/2,-self.size/2)
        return [upperright,lowerright,lowerleft,upperleft]

    def change_direction(self,movestop,direction):
        if movestop:
            self.velocity = self.velocity + direction * TIME_STEP
        else:
            self.velocity = self.velocity - direction * TIME_STEP

    def update(self):
        self.position = self.position + (self.velocity.direction() * self.MAX_SPEED)
        self.world.walltrim(self)

class KarlGame(Game):

    def __init__(self,wallwidth):

        super().__init__('KarlGame',60.0,45.0,800,600,topology='bound')

        
        self.wallbounds = Bounds(self.bounds.xmin+wallwidth,self.bounds.ymin+wallwidth,self.bounds.xmax-wallwidth,self.bounds.ymax-wallwidth)
        self.wallwidth=wallwidth
        self.cannons = []
        self.overFrame = Frame(self.root)

        
        self.gameover = False
        self.pause = False

        Label(self.overFrame,text='Hello!',background='yellow').grid(row=0)
        Button(self.overFrame,text='Play Game',command=self.newstart).grid(row=1)
        self.canvas.create_window(self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT//2,window=self.overFrame)
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
        if event.char == ' ':
            for gun in self.cannons:
                gun.fire()

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

    # def pausescreen(self):

    def gameoverscreen(self):
        self.overFrame = Frame(self.root)
        Label(self.overFrame,text='GAME OVER',background='green').grid(row=0)
        Button(self.overFrame,text='restart',command=self.newstart).grid(row=1)
        
        self.canvas.create_window(self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT//2,window=self.overFrame)
        
        self.root.mainloop()

    def newstart(self):
        self.gameover = False
        self.PlayGame()

    def PlayGame(self):
        self.overFrame.destroy()
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
        while not self.gameover:
            sleep(1.0/60.0)
            self.update()
        self.gameoverscreen()

game = KarlGame(3.0)
game.PlayGame()