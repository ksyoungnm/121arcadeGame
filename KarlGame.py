from Game import *
from geometry import Vector2D
from time import sleep

TIME_STEP = 0.5

class controllable(Agent):

    MAX_SPEED = Vector2D(1.0,0.0)

    UP_VECTOR = Vector2D(0.0,1.0)
    DOWN_VECTOR = Vector2D(0.0,-1.0)
    LEFT_VECTOR = Vector2D(-1.0,0.0)
    RIGHT_VECTOR = Vector2D(1.0,0.0)

    def change_direction(self,movestop,direction):
        if movestop:
            self.velocity = self.velocity + direction * TIME_STEP
        else:
            self.velocity = self.velocity - direction * TIME_STEP

    def update(self):
        self.position = self.position + self.velocity
        self.world.trim(self)

class KarlGame(Game):

    def __init__(self):

        super().__init__('KarlGame',60.0,45.0,800,600,topology='bound')

        self.character = controllable(Point2D(),self)

    def keypress(self,event):
        if event.keysym == 'Up':
            self.character.change_direction(True,self.character.UP_VECTOR)
        if event.keysym == 'Down':
            self.character.change_direction(True,self.character.DOWN_VECTOR)
        if event.keysym == 'Left':
            self.character.change_direction(True,self.character.LEFT_VECTOR)
        if event.keysym == 'Right':
            self.character.change_direction(True,self.character.RIGHT_VECTOR)

    def keyrelease(self,event):
        if event.keysym == 'Up':
            self.character.change_direction(False,self.character.UP_VECTOR)
        if event.keysym == 'Down':
            self.character.change_direction(False,self.character.DOWN_VECTOR)
        if event.keysym == 'Left':
            self.character.change_direction(False,self.character.LEFT_VECTOR)
        if event.keysym == 'Right':
            self.character.change_direction(False,self.character.RIGHT_VECTOR)

game = KarlGame()

while True:
    sleep(1.0/60.0)
    game.update()

