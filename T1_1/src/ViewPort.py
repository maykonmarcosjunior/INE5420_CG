import tkinter as tk
from src.Objetos import Objeto2D as Obj2D


class ViewPort(tk.Canvas):
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        tk.Canvas.__init__(self, master, width=width_, height=height_, bg=bg_)

        self.configure(scrollregion=self.bbox("all"))

        self.__xvmin = self.__yvmin = 0
        self.__xvmax = width_
        self.__yvmax = height_
        


    def viewport_transform(self, x: float, y: float, xw_min: float,
                           xw_max: float, yw_min: float, yw_max: float) -> list[float]:
        vx = (
            (x - xw_min)
            * (self.__xvmax - self.__xvmin)
            / (xw_max - xw_min)
        )
        vy = (1 - (y - yw_min) / (yw_max - yw_min)) * (
            self.__yvmax - self.__yvmin
        )

        return [vx, vy]
