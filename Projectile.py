from Game import Agent
from geometry import Vector2D, Point2D

class Launcher(Agent):

    def __init__(self,position,direction,world):
        super().__init__(position,world)
        self.direction = direction

    def shape(self):
        dirc = self.direction
        perp = self.direction.perp()
        p1 = self.position + -dirc.over(1.5) + perp.over(3.0)
        p2 = self.position + dirc.over(4.0) + perp.over(3.0)
        p3 = self.position + dirc.over(4.0) + perp.over(7.0)
        p4 = self.position + dirc.over(1.0) + perp.over(7.0)
        p5 = self.position + dirc.over(1.0) + -perp.over(7.0)
        p6 = self.position + dirc.over(4.0) + -perp.over(7.0)
        p7 = self.position + dirc.over(4.0) + -perp.over(3.0)
        p8 = self.position + -dirc.over(1.5) + -perp.over(3.0)
        return[p1,p2,p3,p4,p5,p6,p7,p8]

    def color(self):
        return '#9494b8'

    def update(self):
        heading = self.world.character.position - self.position
        self.direction = heading.direction()


    def fire(self):
        self.world.add(Projectile)

    def shapeOLD(self):
        p1 = self.position + Vector2D(-0.35,-1.0)
        p2 = self.position + Vector2D(-0.35,0.5)
        p3 = self.position + Vector2D(-0.15,0.5)
        p4 = self.position + Vector2D(-0.15,1.5)
        p5 = self.position + Vector2D(0.15,1.5)
        p6 = self.position + Vector2D(0.15,0.5)
        p7 = self.position + Vector2D(0.35,0.5)
        p8 = self.position + Vector2D(0.35,-1.0)
        return[p1,p2,p3,p4,p5,p6,p7,p8]

class Projectile(Agent):

    def __init__(self,position,velocity,world):
        super().__init__(position,world)
        self.velocity = velocity

    def shape():
        pass