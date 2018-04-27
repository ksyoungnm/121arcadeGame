from geometry import Vector2D

class Pickup:

    def __init__(self,position,color,world):

        #Actually the initialization for all of my specific pickups is the same, it's just
        #their effects are different. I would have loved to better integrate this system
        #with the timer in the main KarlGame file, but I haven't the time. I once dreamed of
        #pickups that would make the character smaller/bigger, or reverse the arrow key directions
        #so pushing up means going down. ACtually those wouldn't be so hard to do, just the
        #integration into the main game is kinda putting me off it.

        self.world = world
        self.world.pickups.append(self)
        self.position = position
        corners = [self.position+Vector2D(-0.5,0.5),self.position-Vector2D(-0.5,0.5)]
        pts = self.world.worldToPixel(corners)
        self.selfID = self.world.canvas.create_rectangle(pts,fill=color,width=0,tags='Pickup')

class SpeedUp(Pickup):

    def effect(self):
        #speeds up the character, slows down the bullets

        self.world.lifetimeTimes += 1
        self.world.set_character_speed(0.7,400)
        self.world.bullet_speed = 0.2
        self.world.canvas.delete(self.selfID)
        self.world.pickups.remove(self)

class SpeedDown(Pickup):

    def effect(self):
        #just slows down the character, because I thought also speeding up the bullets
        #seemed a little too cruel.
        self.world.lifetimeTimes += 1
        self.world.set_character_speed(0.3,400)
        self.world.canvas.delete(self.selfID)
        self.world.pickups.remove(self)

class Coin(Pickup):

    def effect(self):
        #weee 400 free points.
        self.world.lifetimeCoins += 1
        self.world.score += 400
        self.world.canvas.delete(self.selfID)
        self.world.pickups.remove(self)
