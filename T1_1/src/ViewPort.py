import tkinter as tk
from src.Objetos import Ponto2D as P2D
from src.Objetos import Linha2D as L2D
from src.Objetos import WireFrame as WF
from src.Objetos import Objeto2D as Obj2D


class ViewPort(tk.Canvas):
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        tk.Canvas.__init__(self, master, width=width_, height=height_, bg=bg_)

        self.display_file = []
        self.configure(scrollregion=self.bbox("all"))

        self.__xwmin = self.__xvmin = self.__ywmin = self.__yvmin = 0
        self.__xwmax = self.__xvmax = width_
        self.__ywmax = self.__yvmax = height_

    def draw_object(self, object: Obj2D):
        if object.obj_type == "Point":
            self.draw_point(object.coordinates[0])
        elif object.obj_type == "Line":
            self.draw_line(object.coordinates)
        elif object.obj_type == "Wireframe":
            self.draw_wireframe(object.coordinates)

    def draw_all_objects(self):
        self.delete("all")
        for obj in self.display_file:
            self.draw_object(obj)

    def __zoom(self, c_xwmin, c_xwmax, c_ywmin, c_ywmax):
        self.__xwmin += c_xwmin
        self.__xwmax += c_xwmax
        self.__ywmin += c_ywmin
        self.__ywmax += c_ywmax
        self.draw_all_objects()

    def zoom_in(self) -> None:
        self.__zoom(10, -10, 10, -10)

    def zoom_out(self) -> None:
        self.__zoom(-10, 10, -10, 10)

    def pan_x(self, change: int) -> None:
        self.__xwmin += change
        self.__xwmax += change
        self.draw_all_objects()

    def pan_y(self, change: int) -> None:
        self.__ywmin += change
        self.__ywmax += change
        self.draw_all_objects()

    def viewport_transform(self, x: float, y: float) -> list[float]:
        vx = (
            (x - self.__xwmin)
            * (self.__xvmax - self.__xvmin)
            / (self.__xwmax - self.__xwmin)
        )
        vy = (1 - (y - self.__ywmin) / (self.__ywmax - self.__ywmin)) * (
            self.__yvmax - self.__yvmin
        )

        return [vx, vy]

    def draw_point(self, coords: tuple[float]) -> None:
        vp_x, vp_y = self.viewport_transform(coords[0], coords[1])
        self.create_oval(vp_x - 1, vp_y - 1, vp_x + 1, vp_y + 1, fill="black")

    def draw_line(self, coords: list[tuple[float]]) -> None:
        vp_x_min, vp_y_min = self.viewport_transform(coords[0][0], coords[0][1])
        vp_x_max, vp_y_max = self.viewport_transform(coords[1][0], coords[1][1])
        self.create_line(vp_x_min, vp_y_min, vp_x_max, vp_y_max, fill="black", width=2)

    def draw_wireframe(self, coords: list[tuple[float]]) -> None:
        for i in range(len(coords) - 1):
            self.draw_line([coords[i], coords[i + 1]])
        self.draw_line([coords[-1], coords[0]])
