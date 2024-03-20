import tkinter as tk
from src.Objetos import Ponto2D as P2D
from src.Objetos import Linha2D as L2D
from src.Objetos import WireFrame as WF
from src.Objetos import Objeto2D as Obj2D


class ViewPort(tk.Canvas):
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        tk.Canvas.__init__(self, master, width=width_, height=height_, bg=bg_)

        self.bind("<ButtonPress-1>", self.__pan_start)
        self.bind("<B1-Motion>", self.__pan_move)

        self.configure(scrollregion=self.bbox("all"))

        self.__scale_step = 0.1
        self.__pan_x = 0
        self.__pan_y = 0
        self.__current_scale = 1.0

        self.__xwmin = self.__xvmin = self.__ywmin = self.__yvmin = 0
        self.__xwmax = self.__xvmax = width_
        self.__ywmax = self.__yvmax = height_

        # if you insert any new items into the Canvas, you multiply those coordinates by the scale factor as well
        # (otherwise they will look either too large or too small compared to the rest of the Canvas items)

    # TODO: terminar, falta arrumar as coordenadas da window no pan move e no zoom
    def __pan_start(self, event):
        self.scan_mark(event.x, event.y)

    def __pan_move(self, event):  # Ajustar a window
        self.scan_dragto(event.x, event.y, gain=1)

    # todo: the zoom in and out return different values
    def __zoom(self, zoom_step: float):
        zoom_factor = 1 + zoom_step
        self.__current_scale *= zoom_factor

        self.__xwmin = self.__xvmax - self.__xwmax / zoom_factor
        self.__ywmin = self.__yvmax - self.__ywmax / zoom_factor

        self.__xwmax *= 1 / zoom_factor
        self.__ywmax *= 1 / zoom_factor

        # Calculate the center of the canvas
        canvas_center_x = self.winfo_width() / 2
        canvas_center_y = self.winfo_height() / 2

        # Zoom in or out centered around the canvas center
        self.scale("all", canvas_center_x, canvas_center_y, zoom_factor, zoom_factor)

    def zoom_in(self):
        self.__zoom(self.__scale_step)

    def zoom_out(self):
        self.__zoom(-self.__scale_step)

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
        self.create_oval(vp_x - 3, vp_y - 3, vp_x + 3, vp_y + 3, fill="black")

    def draw_line(self, coords: list[tuple[float]]) -> None:
        vp_x_min, vp_y_min = self.viewport_transform(coords[0][0], coords[0][1])
        vp_x_max, vp_y_max = self.viewport_transform(coords[1][0], coords[1][1])
        self.create_line(vp_x_min, vp_y_min, vp_x_max, vp_y_max, fill="black", width=3)

    def draw_wireframe(self, coords: list[tuple[float]]) -> None:
        for i in range(len(coords) - 1):
            self.draw_line([coords[i], coords[i + 1]])
        self.draw_line([coords[-1], coords[0]])
