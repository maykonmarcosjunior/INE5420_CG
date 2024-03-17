import tkinter as tk
from src.Objetos import Ponto2D
from src.Objetos import Linha2D
from src.Objetos import WireFrame



class ViewPort(tk.Canvas):
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        tk.Canvas.__init__(self, master, width=width_, height=height_, bg=bg_)

        self.__width = width_
        self.__height = height_
        self.bind("<ButtonPress-1>", self.__pan_start)
        self.bind("<B1-Motion>", self.__pan_move)
        
        #self.bind("<Button-4>", self.__zoom_in)
        #self.bind("<Button-5>", self.__zoom_out)
        
        self.configure(scrollregion=self.bbox("all"))
        
        self.__zoom_factor = 0.1
        
    def __pan_start(self, event):
        self.scan_mark(event.x, event.y)
        
    def __pan_move(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def zoom_in(self):
        self.scale("all", 0, 0, 1 + self.__zoom_factor, 1 + self.__zoom_factor)
        
    def zoom_out(self):
        self.scale("all", 0, 0, 1 - self.__zoom_factor, 1 - self.__zoom_factor)

    def viewport_transform(self, x, y):
        vx = (x - self.pan_x) / self.zoom
        vy = self.__height - (y - self.pan_y) / self.zoom
        return vx, vy
        
