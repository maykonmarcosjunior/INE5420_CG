import tkinter as tk
import numpy as np

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
        # x_min, y_min, x_max, y_max
        # using the normalized device coordinates
        self.__world_limits = [-1, -1, 1, 1]
        # middle point of the window
        self.__center = np.array([width_ / 2, height_ / 2, 1])
        # view up vector
        self.__viewup = np.array([0, 1, 1])
        self.__viewup_angle = 0
        self.__clipping_algorithm = "C-S"

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
        T = np.array([[1, 0, 0], [0, 1, 0], [-self.__center[0], -self.__center[1], 1]])
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

    def draw_object(self, object: Obj2D.Objeto2D):
        obj_coords = object.calculate_coords(self.__SCN_matrix)
        #print("objeto coords, ", obj_coords)
        if object.obj_type == "Point":
            self.draw_point(obj_coords[0], object.color)
        elif object.obj_type == "Line":
            self.draw_line(obj_coords, object.color)
        elif object.obj_type == "Wireframe":
            self.draw_wireframe(obj_coords, object.color, object.fill)

    def unrotate_vector(self, dx: float, dy: float) -> tuple[float, float]:
        old_vector = np.array([dx, dy, 0])
        new_vector = np.dot(old_vector, self.__get_rotate_matrix(- self.__viewup_angle))
        return new_vector[0], new_vector[1]

    def __get_rotate_matrix(self, theta: float) -> np.array:
        return np.array([[np.cos(theta), np.sin(theta), 0], [-np.sin(theta), np.cos(theta), 0], [0, 0, 1]])

    def __get_translate_matrix(self, dx: float, dy: float) -> np.array:
        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    def draw_point(self, coords: tuple[float], color: str) -> None:
        # clipping
        x_min, y_min, x_max, y_max = self.__world_limits
        if not (x_min <= coords[0] <= x_max and y_min <= coords[1] <= y_max):
            return
        self.__viewport.draw_oval(*coords, color, self.__width_drawings)

    def draw_line(self, coords: list[tuple[float]], color: str) -> None:
        clipped_coords = self.__clip_line(coords)
        if clipped_coords == []:
            return
        self.__viewport.draw_line(*clipped_coords, color, self.__width_drawings)
    
    def draw_wireframe(self, coords: list[tuple[float]], color: str, fill=False) -> None:
        clipped_coords = self.__sutherland_hodgman(coords)
        if clipped_coords == []:
            return

        self.__viewport.draw_polygon(clipped_coords, color, self.__width_drawings, fill)
    
    def __clip_line(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        if self.__clipping_algorithm == "L-B":
            return self.__liang_barsky(coords)
        elif self.__clipping_algorithm == "C-S":
            return self.__cohen_sutherland(coords)
        elif self.__clipping_algorithm == "N-L-N":
            return self.__nicholl_lee_nicholl(coords)
        else:
            print("Invalid clipping algorithm")
            return []

    def __sutherland_hodgman(self, polygon):
        def inside(p, edge):
            # Função para verificar se um ponto 'p' está dentro de uma aresta 'edge'
            # Usa o produto vetorial para determinar se o ponto está à esquerda da
            # aresta quando esta é percorrida no sentido anti-horário.
            edge_0, edge_1 = edge
            x0, y0 = edge_0
            x1, y1 = edge_1
            x, y = p
            '''
            O produto vetorial entre dois vetores 2D (a, b) e (c, d)
            - é dado pela fórmula: a * d - b * c.
            Se o resultado do produto vetorial for positivo,
            - significa que o vetor (c, d) está à esquerda do vetor (a, b).
            Se o resultado for negativo,
            - significa que o vetor (c, d) está à direita do vetor (a, b).
            Se o resultado for zero,
            - significa que os vetores são colineares.
            '''
            return (x1 - x0) * (y - y0) > (y1 - y0) * (x - x0)

        def compute_intersection(p1, p2, edge):
            # Função para calcular a interseção de uma aresta 'edge' com a linha formada por 'p1' e 'p2'
            # Usando o método de determinantes para encontrar o ponto de interseção
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = edge[0]
            x4, y4 = edge[1]

            """
            Determinante:
                O determinante de uma matriz 2x2 [a, b; c, d] é dado pela fórmula: a * d - b * c.
                O determinante é usado para verificar se duas linhas são paralelas.
                Se o determinante for zero, significa que as linhas são paralelas ou coincidentes.
            Fórmula da Interseção:
                Se as linhas não forem paralelas, é possível calcular o ponto de interseção.
                A fórmula para calcular o ponto de interseção é derivada de um sistema de equações lineares.
                O ponto de interseção é calculado usando a fórmula:
                    (x1 + t * (x2 - x1), y1 + t * (y2 - y1)),
                onde 't' é um parâmetro que determina a posição
                do ponto de interseção ao longo da linha formada por 'p1' e 'p2'.
            """

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                return None  # As linhas são paralelas ou coincidentes
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return x, y

        clipped_polygon = polygon[:]  # Cria uma cópia do polígono original para modificar
        
        # window = [((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (0, 0))]
        window_points = [
                    (self.__world_limits[0], self.__world_limits[1]),
                    (self.__world_limits[2], self.__world_limits[1]),
                    (self.__world_limits[2], self.__world_limits[3]),
                    (self.__world_limits[0], self.__world_limits[3])
                  ]
        window = [(window_points[i], window_points[(i + 1) % 4]) for i in range(4)]

        for edge in window:
            new_polygon = []
            prev_point = clipped_polygon[-1]

            for point in clipped_polygon:
                if inside(point, edge):
                    if not inside(prev_point, edge):
                        intersection = compute_intersection(prev_point, point, edge)
                        if intersection:
                            new_polygon.append(intersection)
                    new_polygon.append(point)
                elif inside(prev_point, edge):
                    intersection = compute_intersection(prev_point, point, edge)
                    if intersection:
                        new_polygon.append(intersection)
                prev_point = point

            clipped_polygon = new_polygon
        return clipped_polygon

    def __liang_barsky(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        clipped_coords = []
        p1, p2 = coords
        Xw_min, Yw_min, Xw_max, Yw_max = self.__world_limits
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
    
    def __compute_outcode(self, x, y):
        xmin, ymin, xmax, ymax = self.__world_limits
        code = 0
        if x < xmin:
            code |= 1
        elif x > xmax:
            code |= 2
        if y < ymin:
            code |= 4
        elif y > ymax:
            code |= 8
        return code
    
    def __cohen_sutherland(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        p1, p2 = coords
        Xw_min, Yw_min, Xw_max, Yw_max = self.__world_limits

        if p1[0] > p2[0]:
            p1, p2 = p2, p1

        RC1 = self.__compute_outcode(*p1)
        RC2 = self.__compute_outcode(*p2)

        RC0 = RC1 | RC2
        if RC0 == 0:
            return coords

        RC = RC1 & RC2
        if RC != 0:
            print("Line outside window")
            return []

        clipped_coords = [p1, p2]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == dy == 0:
            x, y = p1
            if Xw_min <= x <= Xw_max and Yw_min <= y <= Yw_max:
                return [(x, y)]
            else:
                return []
        elif dx == 0:
            x = p1[0]
            y1 = max((min(p1[1], Yw_max)), Yw_min)
            y2 = max((min(p2[1], Yw_max)), Yw_min)
            return [(x, y1), (x, y2)]
        elif dy == 0:
            y = p1[1]
            x1 = max((min(p1[0], Xw_max)), Xw_min)
            x2 = max((min(p2[0], Xw_max)), Xw_min)
            return [(x1, y), (x2, y)]
        m = dy / dx
        yE = m * (Xw_min - p1[0]) + p1[1]
        yD = m * (Xw_max - p1[0]) + p1[1]
        xT = (Yw_max - p1[1]) / m + p1[0]
        xF = (Yw_min - p1[1]) / m + p1[0]
        pX_min = pX_max = pY_min = pY_max = None
        if (RC0 & 1) and (Yw_min <= yE <= Yw_max):
            pX_min = (Xw_min, yE)
            clipped_coords[0] = pX_min
        elif (RC0 & 2) and (Yw_min <= yD <= Yw_max):
            pX_max = (Xw_max, yD)
            clipped_coords[1] = pX_max
        if (RC0 & 4) and (Xw_min <= xF <= Xw_max):
            pY_min = (xF, Yw_min)
            if xT > xF:
                clipped_coords[0] = pY_min
            else:
                clipped_coords[1] = pY_min
        elif (RC0 & 8) and (Xw_min <= xT <= Xw_max):
            pY_max = (xT, Yw_max)
            if xT > xF:
                clipped_coords[1] = pY_max
            else:
                clipped_coords[0] = pY_max
        if clipped_coords == [p1, p2]:
            clipped_coords = []
        clipped_coords = [tuple(float(i) for i in j) for j in clipped_coords]
        return clipped_coords

    def __nicholl_lee_nicholl(self, line):
        p1, p2 = line
        xmin, ymin, xmax, ymax = self.__world_limits
        outcode1 = self.__compute_outcode(*p1)
        outcode2 = self.__compute_outcode(*p2)
        accept = False

        while True:
            if not (outcode1 | outcode2):
                accept = True
                break
            elif outcode1 & outcode2:
                break
            else:
                x = None
                y = None
                outcode_out = outcode1 if outcode1 else outcode2

                if outcode_out & 1:
                    x = xmin
                    y = p1[1] + (p2[1] - p1[1]) * (xmin - p1[0]) / (p2[0] - p1[0])
                elif outcode_out & 2:
                    x = xmax
                    y = p1[1] + (p2[1] - p1[1]) * (xmax - p1[0]) / (p2[0] - p1[0])
                elif outcode_out & 4:
                    y = ymin
                    x = p1[0] + (p2[0] - p1[0]) * (ymin - p1[1]) / (p2[1] - p1[1])
                elif outcode_out & 8:
                    y = ymax
                    x = p1[0] + (p2[0] - p1[0]) * (ymax - p1[1]) / (p2[1] - p1[1])

                if outcode_out == outcode1:
                    p1 = (x, y)
                    outcode1 = self.__compute_outcode(x, y)
                else:
                    p2 = (x, y)
                    outcode2 = self.__compute_outcode(x, y)

        if accept:
            return [tuple(float(i) for i in j) for j in [p1, p2]]
        else:
            return []
    
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
        self.__center = np.dot(self.__center, self.__get_translate_matrix(changed_x, changed_y))

    def pan_y(self, change: int) -> None:
        changed_x, changed_y = self.unrotate_vector(0, change)
        self.__center = np.dot(self.__center, self.__get_translate_matrix(changed_x, changed_y))

    def set_clipping_algorithm(self, algorithm: str) -> None:
        if algorithm in ["C-S", "L-B", "N-L-N"]:
            print("Clipping Algorithm Changed:", algorithm)
            self.__clipping_algorithm = algorithm

    def draw_viewport_outer_frame(self) -> None:
        self.__viewport.draw_outer_frame()
