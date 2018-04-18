from geometry import Point2D, Vector2D

class Wall:

    def __init__(self,width):
        side = float(self.bounds.xmax)
        top = float(self.bounds.ymax)
        wide = float(self.wallwidth)



        
    def pointsGen(self,topleft,botright):
        p1 = topleft
        p2 = Point2D(botright.x,topleft.y)
        p3 = botright
        p4 = topleft[0],botright[1]
        return [p1,p2,p3,p4]

