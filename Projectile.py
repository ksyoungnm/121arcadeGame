from Agent import Agent
from geometry import Vector2D, Point2D

class Launcher(Agent):

    def __init__(self,position,direction,world):
        super().__init__(position,world)
        self.direction = direction
        self.size = 1.5

    def shape(self):
        #I'm kinda proud of this, the shape of the gun is entirely calculated based on its
        #heading, so each time it's drawn it's drawn in the right orientation. I set the heading
        #to be equal to the vector drawn towards the player, so the guns will track the player
        #and shape will be updated accordingly.
        dirc = self.direction
        perp = self.direction.perp()
        p1 = self.position + -dirc.over(1.5*(1/self.size)) + perp.over(3.0*(1/self.size))
        p2 = self.position + dirc.over(4.0*(1/self.size)) + perp.over(3.0*(1/self.size))
        p3 = self.position + dirc.over(4.0*(1/self.size)) + perp.over(7.0*(1/self.size))
        p4 = self.position + dirc.over(1.0*(1/self.size)) + perp.over(7.0*(1/self.size))
        p5 = self.position + dirc.over(1.0*(1/self.size)) + -perp.over(7.0*(1/self.size))
        p6 = self.position + dirc.over(4.0*(1/self.size)) + -perp.over(7.0*(1/self.size))
        p7 = self.position + dirc.over(4.0*(1/self.size)) + -perp.over(3.0*(1/self.size))
        p8 = self.position + -dirc.over(1.5*(1/self.size)) + -perp.over(3.0*(1/self.size))
        return[p1,p2,p3,p4,p5,p6,p7,p8]

    def color(self):
        return '#9494b8'

    def update(self):
        #see shape note
        heading = self.world.character.position - self.position
        self.direction = heading.direction()

    def fire(self):
        #creates a projectile in the direction of the player.
        Projectile(self.position,self.direction,self.world)

class Projectile(Agent):

    def __init__(self,position,velocity,world):
        super().__init__(position,world)
        self.velocity = velocity
        self.size = 0.6
        #these next variables can only be assigned here because the bullet never changes directions.
        #keeps me from having to calculate new directions every time the object is updated.
        self.v0 = self.velocity.over(2.0) + self.velocity.perp().over(4.0)
        self.v1 = self.velocity.over(2.0) + -self.velocity.perp().over(4.0)
        self.v2 = -self.velocity.over(2.0) + -self.velocity.perp().over(4.0)
        self.v3 = -self.velocity.over(2.0) + self.velocity.perp().over(4.0)
        self.world.bullets.append(self)

    def shape(self):
        #see above note
        p0 = self.position + self.v0
        p1 = self.position + self.v1
        p2 = self.position + self.v2
        p3 = self.position + self.v3
        return [p0,p1,p2,p3]

    def color(self):
        return "#FF0000"

    def update(self):
        #moves forward at a rate dependent on the game's bullet_speed parameter, and removes itself
        #if it hits a wall.
        self.position = self.position + (self.velocity * self.world.bullet_speed)
        leading_edge = self.position + self.velocity.over(4.0)
        if (leading_edge.x > self.world.wallbounds.xmax) or (leading_edge.x < self.world.wallbounds.xmin) or (leading_edge.y > self.world.wallbounds.ymax) or (leading_edge.y < self.world.wallbounds.ymin):
            self.world.remove(self)


















