from tkinter import *

ww = 800
wh = 600
wide = 30.0

root = Tk()
c = Canvas(root,width=ww,height=wh,bd=0,bg='green')
c.grid()
c.create_rectangle([(0,0),(ww+1,wh+1)],fill='#000000',width=0)

c.create_rectangle((0,0),(ww+1,wide+1),fill='white',width=0)
c.create_rectangle((ww-wide,wide),(ww+1,wh-wide+1),fill='white',width=0)
c.create_rectangle((0,wh-wide),(ww+1,wh+1),fill='white',width=0)
c.create_rectangle((0,wide),(wide+1,wh-wide+1),fill='white',width=0)

# c.create_rectangle((0,0),(803,10),fill='white',width=0)
# c.create_rectangle((0,0),(803,5),fill='purple',width=0)
# c.create_rectangle((0,0),(803,4),fill='yellow',width=0)
# c.create_rectangle((0,0),(803,3),fill='blue',width=0)
# c.create_rectangle((0,0),(803,2),fill='green',width=0)
# c.create_rectangle((0,0),(803,1),fill='red',width=0)
# c.create_rectangle((0,0),(4,603),fill='yellow',width=0)
# c.create_rectangle((0,0),(3,603),fill='blue',width=0)
# c.create_rectangle((0,0),(2,603),fill='green',width=0)
# c.create_rectangle((0,0),(1,603),fill='red',width=0)
c.xview_moveto(0.0)
c.yview_moveto(0.0)

root.mainloop()
