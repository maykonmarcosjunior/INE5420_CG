import tkinter as tk
import numpy as np

import src.ViewPort as VP
from src.Objetos import Objeto2D as Obj2D
from src.TransformationUtils.Clipper import Clipper


class Window:
    def __init__(self, master=None, width_=600, height_=400):
        self.__viewport_frame = tk.Frame(master)
        self.__viewport_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 80))

        # Title: Viewport
        tk.Label(
            self.__viewport_frame, text="Viewport", font="System 12 bold", pady=5
        ).pack()

        self.__viewport = VP.ViewPort(self.__viewport_frame, width_, height_)
        # middle point of the window
        self.__center = np.array([width_ / 2, height_ / 2, 1])
        # view up vector
        self.__viewup = np.array([0, 1, 1])
        self.__viewup_angle = 0
        # using the normalized device coordinates
        self.__clipper = Clipper("SCN", "L-B")

        self.__xwmin = self.__ywmin = 0
        self.__xwmax = width_
        self.__ywmax = height_

        self.__zoom_step = 0.1
        self.__scaling_factor = 1
        self.__width_drawings = 2

        self.__SCN_matrix = None
        self.set_normalization_matrix(0)

    def set_normalization_matrix(self, angle: float = 0):
        self.__update_view_up_vector(np.radians(angle))

        theta = self.__viewup_angle

        #print("theta:", theta, "rad of:", angle, "degrees")
        T = np.array([
                      [1, 0, 0], [0, 1, 0],
                      [-self.__center[0], -self.__center[1], 1]
                     ])
        R = self.__get_rotate_matrix(theta)
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
        rotate_matrix = self.__get_rotate_matrix(theta)
        self.__viewup = np.matmul(self.__viewup, rotate_matrix)

        # The arctan2 function gives the angle that the vector makes with the positive x-axis.
        # To get the angle made with the positive y-axis, we subtract the result from pi/2.
        # The multiplication by -1 is needed to make the rotation counter-clockwise.
        self.__viewup_angle = -1 * (np.pi / 2 - np.arctan2(self.__viewup[1], self.__viewup[0]))

    def unrotate_vector(self, dx: float, dy: float) -> tuple[float, float]:
        old_vector = np.array([dx, dy, 0])
        new_vector = np.dot(old_vector, self.__get_rotate_matrix(- self.__viewup_angle))
        return new_vector[0], new_vector[1]

    def __get_rotate_matrix(self, theta: float) -> np.array:
        return np.array([[np.cos(theta), np.sin(theta), 0],
                         [-np.sin(theta), np.cos(theta), 0],
                         [0, 0, 1]])

    def __get_translate_matrix(self, dx: float, dy: float) -> np.array:
        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    def draw_object(self, object: Obj2D.Objeto2D):
        obj_coords = object.calculate_coords(self.__SCN_matrix)

        if object.obj_type == Obj2D.ObjectType.POINT:
            self.draw_point(obj_coords[0], object.color)
        elif object.obj_type == Obj2D.ObjectType.LINE:
            self.draw_line(obj_coords, object.color)
        elif object.obj_type == Obj2D.ObjectType.WIREFRAME:
            self.draw_wireframe(obj_coords, object.color, object.fill)
        elif object.obj_type in [Obj2D.ObjectType.BEZIER_CURVE, Obj2D.ObjectType.BSPLINE_CURVE]:
            self.draw_curve(object.generate_curve(obj_coords), object.color)

    def draw_point(self, coords: tuple[float], color: str) -> None:
        # if the point is outside the window, it is not drawn
        self.__viewport.draw_oval(self.__clipper.clip_point(coords),
                                  color, self.__width_drawings)

    def draw_line(self, coords: list[tuple[float]], color: str) -> None:
        self.__viewport.draw_line(self.__clipper.clip_line(coords),
                                  color, self.__width_drawings)

    def draw_wireframe(self, coords: list[tuple[float]], color: str, fill=False) -> None:
        self.__viewport.draw_polygon(self.__clipper.clip_polygon(coords),
                                     color, self.__width_drawings, fill)

    def draw_curve(self, coords: list[tuple[float]], color: str) -> None:
        self.__viewport.draw_curve(self.__clipper.clip_curve(coords),
                                   color, self.__width_drawings)

    def __update_width_drawings(self):
        self.__width_drawings = 2 * self.__scaling_factor

    def delete(self, object_name="all"):
        if object_name == "all":
            self.__viewport.delete("all")

    def __zoom(self, zoom_step: float) -> None:
        self.__scaling_factor *= 1 + zoom_step
        self.__update_width_drawings()

    def zoom_in(self) -> None:
        self.__zoom(self.__zoom_step)

    def zoom_out(self) -> None:
        self.__zoom(-self.__zoom_step)

    def pan_x(self, change: int) -> None:
        changed_x, changed_y = self.unrotate_vector(change, 0)
        self.__center = np.dot(self.__center,
                               self.__get_translate_matrix(changed_x, changed_y))

    def pan_y(self, change: int) -> None:
        changed_x, changed_y = self.unrotate_vector(0, change)
        self.__center = np.dot(self.__center,
                               self.__get_translate_matrix(changed_x, changed_y))

    def draw_viewport_outer_frame(self) -> None:
        self.__viewport.draw_outer_frame()

    # works for both lines and polygons algorithms
    def set_clipping_algorithm(self, algorithm: str) -> None:
        self.__clipper.set_clipping_algorithm(algorithm)
    
    # define the world limits for clipping
    def set_clipping_window(self, window: str) -> None:
        self.__clipper.set_window(window)
