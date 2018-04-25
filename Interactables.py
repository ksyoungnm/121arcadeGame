from geometry import Vector2D

class Pickup:

    def __init__(self,position,color,world):
        self.world = world
        self.world.pickups.append(self)
        self.position = position
        corners = [self.position+Vector2D(-0.5,0.5),self.position-Vector2D(-0.5,0.5)]
        pts = self.world.worldToPixel(corners)
        self.selfID = self.world.canvas.create_rectangle(pts,fill=color,width=0,tags='Pickup')

class SpeedUp(Pickup):

    def effect(self):
        self.world.character.MAX_SPEED = 0.75
        self.world.canvas.delete(self.selfID)
