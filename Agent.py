from geometry import Vector2D, Point2D

class Agent:

    def __init__(self,position,world):
        self.position = position
        self.velocity = Vector2D()
        self.shapekind = 'poly'
        self.world = world
        self.world.add(self)

    def color(self):
        return '#FFFFFF'

    def shape(self):
        upperright = self.position + Vector2D(1,1)
        lowerright = self.position + Vector2D(1,-1)
        lowerleft = self.position + Vector2D(-1,-1)
        upperleft = self.position + Vector2D(-1,1)
        return [upperright,lowerright,lowerleft,upperleft]

    def update(self):
        pass

class Controllable(Agent):

    MAX_SPEED = 0.5

    UP_VECTOR = Vector2D(0.0,1.0)
    DOWN_VECTOR = Vector2D(0.0,-1.0)
    LEFT_VECTOR = Vector2D(-1.0,0.0)
    RIGHT_VECTOR = Vector2D(1.0,0.0)

    def __init__(self,position,size,world):
        super().__init__(position,world)
        self.world.bind_all('<Key-Up>',self.moveUp)
        self.world.bind_all('<KeyRelease-Up>',self.stopUp)
        self.world.bind_all('<Key-Down>',self.moveDown)
        self.world.bind_all('<KeyRelease-Down>',self.stopDown)
        self.world.bind_all('<Key-Left>',self.moveLeft)
        self.world.bind_all('<KeyRelease-Left>',self.stopLeft)
        self.world.bind_all('<Key-Right>',self.moveRight)
        self.world.bind_all('<KeyRelease-Right>',self.stopRight)
        self.size = size
        self.hit_radius = 0.4

    def shape(self):
        upperright = self.position + Vector2D(self.size/2,self.size/2)
        lowerright = self.position + Vector2D(self.size/2,-self.size/2)
        lowerleft = self.position + Vector2D(-self.size/2,-self.size/2)
        upperleft = self.position + Vector2D(-self.size/2,self.size/2)
        return [upperright,lowerright,lowerleft,upperleft]

    def moveUp(self,event):
        self.change_direction(True,self.UP_VECTOR)
    def stopUp(self,event):
        self.change_direction(False,self.UP_VECTOR)
    def moveDown(self,event):
        self.change_direction(True,self.DOWN_VECTOR)
    def stopDown(self,event):
        self.change_direction(False,self.DOWN_VECTOR)
    def moveLeft(self,event):
        self.change_direction(True,self.LEFT_VECTOR)
    def stopLeft(self,event):
        self.change_direction(False,self.LEFT_VECTOR)
    def moveRight(self,event):
        self.change_direction(True,self.RIGHT_VECTOR)
    def stopRight(self,event):
        self.change_direction(False,self.RIGHT_VECTOR)

    def change_direction(self,movestop,direction):
        if movestop:
            self.velocity = self.velocity + direction * self.MAX_SPEED
        else:
            self.velocity = self.velocity - direction * self.MAX_SPEED

    def update(self):
        self.position = self.position + (self.velocity.direction() * self.MAX_SPEED)
        self.world.walltrim(self)