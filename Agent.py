from geometry import Vector2D, Point2D

class Agent:

    def __init__(self,position,world):
        self.position = position
        self.velocity = Vector2D()
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

    def __init__(self,position,size,world):
        super().__init__(position,world)
        #So I bind the movement keys here, I guess because it makes more sense to me conceptually.
        #keys are bound to the movement of the character, and each press/release to a different change
        #in velocity.
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

    #I'll admit it's not the most elegant of solutions, but hey it works and it works for speeds
    #of all magnitudes.

    def moveUp(self,event):
        self.velocity.dy += 1
    def stopUp(self,event):
        self.velocity.dy -= 1
    def moveDown(self,event):
        self.velocity.dy -= 1
    def stopDown(self,event):
        self.velocity.dy += 1
    def moveLeft(self,event):
        self.velocity.dx -= 1
    def stopLeft(self,event):
        self.velocity.dx += 1
    def moveRight(self,event):
        self.velocity.dx += 1
    def stopRight(self,event):
        self.velocity.dx -= 1

    def update(self):
        #I'm choosing to not include an acceleration vector for movement cause I wan't the player controlled character to feel more snappy.
        self.position = self.position + (self.velocity.direction()*self.MAX_SPEED)
        self.world.walltrim(self)