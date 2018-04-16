from geometry import Point2D, Vector2D

class Wall:

    def __init__(self,TOP_LEFT,BOTTOM_RIGHT,world):
        self.TOP_LEFT = TOP_LEFT
        self.BOTTOM_RIGHT = BOTTOM_RIGHT
        self.world = world
        self.shapekind = 'poly'
        self.world.add(self)

    def shape(self):
        p1 = self.TOP_LEFT
        p2 = Point2D(self.BOTTOM_RIGHT.x,self.TOP_LEFT.y)
        p3 = self.BOTTOM_RIGHT
        p4 = Point2D(self.TOP_LEFT.x,self.BOTTOM_RIGHT.y)
        return[p1,p2,p3,p4]

    def color(self):
        return '#FFFFFF'
    
    def update(self):
        pass

class Walls:

    def __init__(self,width,world):
        self.width = width
        self.contain = []
        self.world = world

        self.contain.append(Wall(Point2D(-30.0,22.5),Point2D(31.0,22.5-self.width),self.world))
        self.contain.append(Wall(Point2D(30.0-self.width,22.5-self.width),Point2D(31.0,-22.5+self.width),self.world))
        self.contain.append(Wall(Point2D(-30.0,-22.5+self.width),Point2D(31.0,-23.5),self.world))
        self.contain.append(Wall(Point2D(-30.0,22.5-self.width),Point2D(-30.0+self.width,-22.5+self.width),self.world))