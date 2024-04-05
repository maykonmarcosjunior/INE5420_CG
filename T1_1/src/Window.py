import tkinter as tk
import numpy as np

import src.ViewPort as VP
from src.Objetos import Objeto2D as Obj2D


class Window:
    def __init__(self, master=None, width_=600, height_=400, max_width=1000, max_height=1000):
        self.__viewport_frame = tk.Frame(master)
        self.__viewport_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 80))

        # Title: Viewport
        tk.Label(
            self.__viewport_frame, text="Viewport", font="System 12 bold", pady=5
        ).pack()

        self.__viewport = VP.ViewPort(self.__viewport_frame, width_, height_)
        self.__viewport.pack()

        self.__SCN_limits = [-1, -1, 1, 1]
        self.__center = (width_ / 2, height_ / 2)
        self.__viewup = np.array([0, 1, 1])
        self.__viewup_angle = 0

        self.__xwmin = self.__ywmin = 0
        self.__xwmax = width_
        self.__ywmax = height_

        self.__min_width = 20
        self.__min_height = 20
        self.__max_width = max_width
        self.__max_height = max_height

        self.__zoom_step = 0.1
        self.__scaling_factor = 1
        self.__width_drawings = 2

        self.__SCN_matrix = None
        self.set_normalization_matrix(0)

    def set_normalization_matrix(self, angle: float = 0):
        self.__update_view_up_vector(np.radians(angle))

        theta = self.__viewup_angle

        #print("theta:", theta, "rad of:", angle, "degrees")
        T = np.array([[1, 0, 0], [0, 1, 0], [-self.__center[0], -self.__center[1], 1]])
        R = np.array([[np.cos(theta), np.sin(theta), 0], [-np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
        #print("\nviewup:", self.__viewup)
        S = np.array(
            [
                [2 * self.__scaling_factor / (self.__xwmax - self.__xwmin), 0, 0],
                [0, 2 * self.__scaling_factor / (self.__ywmax - self.__ywmin), 0],
                [0, 0, 1],
            ]
        )
        # self.__SCN_matrix = T @ R @ S
        self.__SCN_matrix = np.matmul(np.matmul(T, R), S)

    def __update_view_up_vector(self, theta: np.ndarray):
        rotate_matrix = np.array(
            [
                [np.cos(theta), np.sin(theta), 0],
                [-np.sin(theta), np.cos(theta), 0],
                [0, 0, 1],
            ]
        )
        self.__viewup = np.matmul(self.__viewup, rotate_matrix)

        # The arctan2 function gives the angle that the vector makes with the positive x-axis.
        # To get the angle made with the positive y-axis, we subtract the result from pi/2.
        # The multiplication by -1 is needed to make the rotation counter-clockwise.
        self.__viewup_angle = -1 * (np.pi / 2 - np.arctan2(self.__viewup[1], self.__viewup[0]))

    def draw_object(self, object: Obj2D.Objeto2D):
        obj_scn_coords = object.calculate_coords(self.__SCN_matrix)
        #print("objeto coords, ", obj_scn_coords)
        if object.obj_type == "Point":
            self.draw_point(obj_scn_coords[0], object.color)
        elif object.obj_type == "Line":
            self.draw_line(obj_scn_coords, object.color)
        elif object.obj_type == "Wireframe":
            self.draw_wireframe(obj_scn_coords, object.color)

    def draw_point(self, coords: tuple[float], color: str) -> None:
        # clipping
        if not (self.__xwmin <= coords[0] <= self.__xwmax and self.__ywmin <= coords[1] <= self.__ywmax):
            return
        vp_x, vp_y = self.__viewport.viewport_transform(coords[0], coords[1])
        self.__viewport.create_oval(vp_x - self.__width_drawings, vp_y - self.__width_drawings, vp_x + self.__width_drawings, vp_y + self.__width_drawings, fill=color, outline=color)

    def draw_line(self, coords: list[tuple[float]], color: str) -> None:
        clipped_coords = self.__cohen_sutherland(coords)
        # clipped_coords = self.__liang_barsky(coords)
        if clipped_coords == []:
            return
        vp_x_min, vp_y_min = self.__viewport.viewport_transform(
            clipped_coords[0][0], clipped_coords[0][1], self.__xwmin,
             self.__xwmax, self.__ywmin, self.__ywmax
             )
        vp_x_max, vp_y_max = self.__viewport.viewport_transform(
            clipped_coords[1][0], clipped_coords[1][1], self.__xwmin,
             self.__xwmax, self.__ywmin, self.__ywmax
             )
        self.__viewport.create_line(vp_x_min, vp_y_min, vp_x_max, vp_y_max,
                                     fill=color, width=self.__width_drawings)

    def draw_wireframe(self, coords: list[tuple[float]], color: str) -> None:
        for i in range(len(coords) - 1):
            self.draw_line([coords[i], coords[i + 1]], color)
        self.draw_line([coords[-1], coords[0]], color)

    def __cohen_sutherland(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        clipped_coords = []
        p1, p2 = coords
        Xw_min, Yw_min, Xw_max, Yw_max = self.__SCN_limits
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        RC1 = [
                (p1[1] > Yw_max), (p1[1] < Yw_min),
                (p1[0] > Xw_max), (p1[0] < Xw_min)
            ]
        RC2 = [
                (p2[1] > Yw_max), (p2[1] < Yw_min),
                (p2[0] > Xw_max), (p2[0] < Xw_min)
            ]
        RC = [i and j for i, j in zip(RC1, RC2)]
        if RC == [False, False, False, False]:
            clipped_coords = [p1, p2]
            if RC1 != RC2:
                m = (p2[1] - p1[1]) / (p2[0] - p1[0])
                yE = m * (Xw_min - p1[0]) + p1[1]
                yD = m * (Xw_max - p1[0]) + p1[1]
                xT = (Yw_max - p1[1]) / m + p1[0]
                xF = (Yw_min - p1[1]) / m + p1[0]
                pX_min = pX_max = pY_min = pY_max = None
                if (RC1[3] or RC2[3]) and (Yw_min <= yE <= Yw_max):
                    pX_min = (Xw_min, yE)
                    clipped_coords[0] = pX_min
                if (RC1[2] or RC2[2]) and (Yw_min <= yD <= Yw_max):
                    pX_max = (Xw_max, yD)
                    clipped_coords[1] = pX_max
                if (RC1[0] or RC2[0]) and (Xw_min <= xT <= Xw_max):
                    pY_max = (xT, Yw_max)
                    if xT > xF:
                        clipped_coords[1] = pY_max
                    else:
                        clipped_coords[0] = pY_max
                if (RC1[1] or RC2[1]) and (Xw_min <= xF <= Xw_max):
                    pY_min = (xF, Yw_min)
                    if xT > xF:
                        clipped_coords[0] = pY_min
                    else:
                        clipped_coords[1] = pY_min
                if clipped_coords == [p1, p2]:
                    clipped_coords = []
                
        else:
            print("Line outside window")
        return clipped_coords
    
    def __liang_barsky(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        clipped_coords = []
        p1, p2 = coords
        Xw_min, Yw_min, Xw_max, Yw_max = self.__SCN_limits
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        p = [-dx, dx, -dy, dy]
        q = [p1[0] - Xw_min, Xw_max - p1[0], p1[1] - Yw_min, Yw_max - p1[1]]
        u1 = 0
        u2 = 1
        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return []
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, u)
                else:
                    u2 = min(u2, u)
        if u1 < u2:
            clipped_coords = [(p1[0] + u1 * dx, p1[1] + u1 * dy), (p1[0] + u2 * dx, p1[1] + u2 * dy)]
        return clipped_coords
    
    def __update_width_drawings(self, zoom_type: str):
        current_window_size = self.__xwmax - self.__xwmin
        last_size = current_window_size - (2 * self.__zoom_step) if zoom_type == "out" else current_window_size + (2 * self.__zoom_step)
        self.__width_drawings *= last_size / current_window_size

    def delete(self, object_name="all"):
        if object_name == "all":
            self.__viewport.delete("all")

    def __zoom(self, c_xwmin: int, c_xwmax: int, c_ywmin: int, c_ywmax: int) -> None:
        if self.__is_min_size() and c_xwmin > 0:
            return
        if self.__is_max_size() and c_xwmin < 0:
            return

        self.__xwmin += c_xwmin
        self.__xwmax += c_xwmax
        self.__ywmin += c_ywmin
        self.__ywmax += c_ywmax

        zoom_type = "in" if c_xwmin > 0 else "out"
        self.__update_width_drawings(zoom_type)

    def zoom_in(self) -> None:
        self.__zoom(self.__zoom_step)

    def zoom_out(self) -> None:
        self.__zoom(-self.__zoom_step)

    def pan_x(self, change: int) -> None:
        self.__center[0] += change * np.cos(-self.__viewup_angle)
        self.__center[1] += change * np.sin(-self.__viewup_angle)

    def pan_y(self, change: int) -> None:
        self.__center[0] += change * np.sin(self.__viewup_angle)
        self.__center[1] += change * np.cos(self.__viewup_angle)

    def __is_min_size(self) -> bool:
        if (self.__xwmax - self.__xwmin == self.__min_width) or (self.__ywmax - self.__ywmin == self.__min_height):
            print("Maximum zoom reached!")
            return True
        return False

    def __is_max_size(self) -> bool:
        if (self.__xwmax - self.__xwmin == self.__max_width) or (self.__ywmax - self.__ywmin == self.__max_height):
            print("Maximum zoom reached!")
            return True
        return False
