from tkinter import *
from geometry import Bounds, Point2D, Vector2D
    
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

        self.bind_all('<KeyPress>',self.keypress)
        self.bind_all('<KeyRelease>',self.keyrelease)

        self.canvas = Canvas(self, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, bg='purple')
        
        self.grid()
        self.canvas.grid()

        self.canvas.xview_moveto(0.0)
        self.canvas.yview_moveto(0.0)
        
    def trim(self,agent):
        if self.topology == 'wrapped':
            agent.position = self.bounds.wrap(agent.position)
        elif self.topology == 'bound':
            agent.position = self.bounds.clip(agent.position)
        elif self.topology == 'open':
            pass

    def walltrim(self,agent):
        agent.position = self.wallbounds.hitboxtrim(agent.position,agent.size/2)

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        self.agents.remove(agent)
        self.bullets.remove(agent)

    def update(self):
        pass

    def worldToPixel(self,shape):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        return points

    def drawagent(self,shape,color):
        points = self.worldToPixel(shape)
        return self.canvas.create_rectangle(points,fill=color,width=0,tags='agent')

    def draw_poly(self, shape, color, tags):
        points = self.worldToPixel(shape)
        first_point = points[0]
        points.append(first_point)
        return self.canvas.create_polygon(points, width=0, fill=color, tags=tags)

    def draw_oval(self, shape, color, tags):
        points = self.worldToPixel(shape)
        first_point = points[0]
        points.append(first_point)
        return self.canvas.create_polygon(points, width=0, fill=color, smooth=1, tags=tags)

    def keypress(self,event):
        pass

    def keyrelease(self,event):
        pass