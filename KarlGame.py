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

        self.character = controllable(Point2D(),0.6,self)
        self.wall = Walls(wallwidth,self)
        self.wallbounds = Bounds(self.bounds.xmin+wallwidth,self.bounds.ymin+wallwidth,self.bounds.xmax-wallwidth,self.bounds.ymax-wallwidth)
        self.cannons = []
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

    def keypress(self,event):
        if event.keysym == 'Up':
            self.character.change_direction(True,self.character.UP_VECTOR)
        if event.keysym == 'Down':
            self.character.change_direction(True,self.character.DOWN_VECTOR)
        if event.keysym == 'Left':
            self.character.change_direction(True,self.character.LEFT_VECTOR)
        if event.keysym == 'Right':
            self.character.change_direction(True,self.character.RIGHT_VECTOR)
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

    def gameoverscreen(self):
        self.root.mainloop()

game = KarlGame(3.0)

while not game.gameover:
    sleep(1.0/60.0)
    game.update()

game.gameoverscreen()