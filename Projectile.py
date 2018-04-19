from Agent import Agent
from geometry import Vector2D, Point2D

class Launcher(Agent):

    def __init__(self,position,direction,world):
        super().__init__(position,world)
        self.direction = direction
        self.size = 1.5

    def shape(self):
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
        heading = self.world.character.position - self.position
        self.direction = heading.direction()

    def fire(self):
        Projectile(self.position,self.direction,self.world)

# class Projectile(Agent):

#     MAX_SPEED = 0.5


#     def __init__(self,position,velocity,world):
#         super().__init__(position,world)
#         self.velocity = velocity
#         self.shapekind = 'oval'
#         self.size = 0.6
#         self.v0 = self.velocity.over(2.0) + self.velocity.perp().over(4.0)
#         self.v1 = self.velocity.over(2.0) + -self.velocity.perp().over(4.0)
#         self.v2 = -self.velocity.over(2.0) + -self.velocity.perp().over(4.0)
#         self.v3 = -self.velocity.over(2.0) + self.velocity.perp().over(4.0)
#         self.hit_radius = 0.4

#     def shape(self):
#         p0 = self.position + self.v0
#         p1 = self.position + self.v1
#         p2 = self.position + self.v2
#         p3 = self.position + self.v3
#         return [p0,p1,p2,p3]

#     def color(self):
#         return "#FF0000"

#     def update(self):
#         self.position = self.position + (self.velocity * self.MAX_SPEED)
#         leading_edge = self.position + self.velocity.over(4.0)
#         if (leading_edge.x > self.world.wallbounds.xmax) or (leading_edge.x < self.world.wallbounds.xmin) or (leading_edge.y > self.world.wallbounds.ymax) or (leading_edge.y < self.world.wallbounds.ymin):
#             self.world.remove(self)
#         if (self.world.character.position-self.position).magnitude() - self.world.character.hit_radius < self.hit_radius:
#             self.world.gameover = True


















