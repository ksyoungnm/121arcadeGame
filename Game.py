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

        self.canvas = Canvas(self, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        
        self.grid()
        self.canvas.grid()
        
        

    def trim(self,agent):
        if self.topology == 'wrapped':
            agent.position = self.bounds.wrap(agent.position)
        elif self.topology == 'bound':
            agent.position = self.bounds.clip(agent.position)
        elif self.topology == 'open':
            pass

    def walltrim(self,agent):
        agent.position = self.wallbounds.hitboxtrim(agent)

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


    def worldToWall(self,blist):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        ul = blist[0]
        br = blist[1]
        points = [ ((ul.x - x)*wh/h , wh - (ul.y - y)* wh/h) ] + [ (((br.x - x)*wh/h) + 1 , wh - ((br.y - y)* wh/h) + 1) ]
        return points

    def worldToPixel(self,shape):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        return points

    def draw_poly(self, shape, color, tags):
        points = self.worldToPixel(shape)
        first_point = points[0]
        points.append(first_point)
        return self.canvas.create_polygon(points, fill=color, tags=tags)

    def draw_oval(self, shape, color, tags):
        points = self.worldToPixel(shape)
        first_point = points[0]
        points.append(first_point)
        return self.canvas.create_polygon(points, fill=color, smooth=1, tags=tags)

    def clear(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, fill="#000000")

    def keypress(self,event):
        pass

    def keyrelease(self,event):
        pass