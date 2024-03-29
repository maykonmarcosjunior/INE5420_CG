import tkinter as tk
from src.Objetos import Objeto2D as Obj2D


class ViewPort(tk.Canvas):
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        tk.Canvas.__init__(self, master, width=width_, height=height_, bg=bg_)

        self.configure(scrollregion=self.bbox("all"))

        self.__width = width_
        self.__height = height_
        


    def viewport_transform(self, x: float, y: float, xw_min: float,
                           xw_max: float, yw_min: float, yw_max: float,
                           SCN: bool = True) -> list[float]:
        if SCN:
            x *= self.__width
            y *= self.__height
        vx = (
            (x - xw_min)
            * (self.__width)
            / (xw_max - xw_min)
        )
        vy = (1 - (y - yw_min) / (yw_max - yw_min)) * (self.__height)
        
        # vx = (x + 1) / (2) * self.__width + 10
        # vy = (1 - (y + 1) / (2)) * self.__height + 10

        print("\nvx:", vx, "vy:", vy, "\n")

        return [vx, vy]
