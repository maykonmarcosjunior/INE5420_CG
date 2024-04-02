import tkinter as tk
from src.Objetos import Objeto2D as Obj2D


class ViewPort(tk.Canvas):
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        tk.Canvas.__init__(self, master, width=width_, height=height_, bg=bg_)

        self.configure(scrollregion=self.bbox("all"))

        self.__width = width_
        self.__height = height_
        

    def viewport_transform(self, x: float, y: float) -> list[float]:
        vx = ((x + 1) * (self.__width) / 2)
        vy = (1 - (y + 1) / 2) * (self.__height)

        return [vx, vy]
