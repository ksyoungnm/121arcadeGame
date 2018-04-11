from tkinter import *
from geometry import Bounds, Point2D, Vector2D

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
        lowerright = self.position + Vector2D(-1,1)
        lowerleft = self.position + Vector2D(-1,-1)
        upperleft = self.position + Vector2D(1,-1)
        return [upperright,lowerright,lowerleft,upperleft]

    def update(self):
        pass

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
    
class Game(Frame):

    def __init__(self,name,w,h,ww,wh,topology='wrapped'):

        self.WINDOW_WIDTH = ww
        self.WINDOW_HEIGHT = wh
        self.bounds = Bounds(-w/2,-h/2,w/2,h/2)
        self.topology = topology

        self.agents = []

        self.root = Tk()
        self.root.title(name)
        Frame.__init__(self, self.root)
        

        self.canvas = Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        

        self.bind_all('<KeyPress>',self.keypress)
        self.bind_all('<KeyRelease>',self.keyrelease)
        
        self.grid()
        self.canvas.grid()

        

    def trim(self,agent):
        if self.topology == 'wrapped':
            agent.position = self.bounds.wrap(agent.position)
        elif self.topology == 'bound':
            agent.position = self.bounds.clip(agent.position)
        elif self.topology == 'open':
            pass

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        self.agents.remove(agent)

    def update(self):
        for agent in self.agents:
            agent.update()
        self.clear()
        for agent in self.agents:
            if agent.shapekind == 'poly':
                self.draw_poly(agent.shape(),agent.color())
            elif agent.shapekind == 'oval':
                self.draw_oval(agent.shape(),agent.color())
        Frame.update(self)

    def draw_poly(self, shape, color):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        first_point = points[0]
        points.append(first_point)
        self.canvas.create_polygon(points, fill=color)

    def draw_oval(self, shape, color):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        self.canvas.create_polygon(points, fill=color, smooth=1)


    def clear(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, fill="#000000")

    def keypress(self,event):
        pass

    def keyrelease(self,event):
        pass