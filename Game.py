from tkinter import *
from geometry import Bounds, Point2D, Vector2D

class Agent:

    def __init__(self,position,world):
        self.position = position
        self.velocity = Vector2D()
        self.world = world
        self.world.add(self)

    def color(self):
        return '#FFFFFF'

    def shape(self):
        p1 = self.position + Vector2D( 0.4, 0.4)       
        p2 = self.position + Vector2D(-0.4, 0.4)        
        p3 = self.position + Vector2D(-0.4,-0.4)        
        p4 = self.position + Vector2D( 0.4,-0.4)
        return [p1,p2,p3,p4]

    def update(self):
        self.world.trim(self)
    
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
        
        self.canvas.pack()

        self.pack()

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
            self.draw_shape(agent.shape(),agent.color())
        Frame.update(self)

    def draw_shape(self, shape, color):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        first_point = points[0]
        points.append(first_point)
        self.canvas.create_polygon(points, fill=color)

    def clear(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, fill="#000000")

    def keypress(self,event):
        pass

    def keyrelease(self,event):
        pass