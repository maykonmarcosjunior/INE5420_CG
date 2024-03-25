import tkinter as tk

import src.ViewPort as VP
from src.Objetos import Objeto2D as Obj2D


class Window:
    def __init__(self, master=None, width_=600, height_=400):
        self.__viewport_frame = tk.Frame(master)
        self.__viewport_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 80))

        # Title: Viewport
        tk.Label(
            self.__viewport_frame, text="Viewport", font="System 12 bold", pady=5
        ).pack()

        self.__viewport = VP.ViewPort(self.__viewport_frame, width_, height_)
        self.__viewport.pack()

        self.__xwmin = self.__ywmin = 0
        self.__xwmax = width_
        self.__ywmax = height_

        self.__min_width = 20
        self.__min_height = 20

    def draw_object(self, object: Obj2D.Objeto2D):
        if object.obj_type == "Point":
            self.draw_point(object.coordinates[0])
        elif object.obj_type == "Line":
            self.draw_line(object.coordinates)
        elif object.obj_type == "Wireframe":
            self.draw_wireframe(object.coordinates)

    def draw_point(self, coords: tuple[float]) -> None:
        vp_x, vp_y = self.__viewport.viewport_transform(coords[0], coords[1], self.__xwmin, self.__xwmax, self.__ywmin, self.__ywmax)
        self.__viewport.create_oval(vp_x - 1, vp_y - 1, vp_x + 1, vp_y + 1, fill="black")

    def draw_line(self, coords: list[tuple[float]]) -> None:
        vp_x_min, vp_y_min = self.__viewport.viewport_transform(coords[0][0], coords[0][1], self.__xwmin, self.__xwmax, self.__ywmin, self.__ywmax)
        vp_x_max, vp_y_max = self.__viewport.viewport_transform(coords[1][0], coords[1][1], self.__xwmin, self.__xwmax, self.__ywmin, self.__ywmax)
        self.__viewport.create_line(vp_x_min, vp_y_min, vp_x_max, vp_y_max, fill="black", width=2)

    def draw_wireframe(self, coords: list[tuple[float]]) -> None:
        for i in range(len(coords) - 1):
            self.draw_line([coords[i], coords[i + 1]])
        self.draw_line([coords[-1], coords[0]])

    def delete(self, object_name="all"):
        if object_name == "all":
            self.__viewport.delete("all")

    def __zoom(self, c_xwmin: int, c_xwmax: int, c_ywmin: int, c_ywmax: int) -> None:
        if self.__is_min_size():
            return

        self.__xwmin += c_xwmin
        self.__xwmax += c_xwmax
        self.__ywmin += c_ywmin
        self.__ywmax += c_ywmax

    def zoom_in(self) -> None:
        self.__zoom(10, -10, 10, -10)

    def zoom_out(self) -> None:
        self.__zoom(-10, 10, -10, 10)

    def pan_x(self, change: int) -> None:
        self.__xwmin += change
        self.__xwmax += change

    def pan_y(self, change: int) -> None:
        self.__ywmin += change
        self.__ywmax += change

    def __is_min_size(self) -> bool:
        if (self.__xwmax - self.__xwmin == self.__min_width) or (self.__ywmax - self.__ywmin == self.__min_height):
            print("Maximum zoom reached!")
            return True
        return False
