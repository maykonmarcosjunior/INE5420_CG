import math
from src.Objetos.Objeto3D import Objeto3D, ObjectType
import numpy as np

class BSplineBicurve(Objeto3D):
    def __init__(self, name: str, coords: list[tuple[float]],
                 obj_type=ObjectType.BEZIER_BICURVE, color="#000000",
                 curves: list[tuple[int]]=[]):
        new_coords = []
        for curve in coords:
            new_coords.extend(curve)
        super().__init__(name, new_coords, obj_type, color, curves)

        # As coordenadas guardadas são os pontos de controle

        self.__MBS = (
            np.array([[-1, 3, -3, 1],
                      [3, -6, 3, 0],
                      [-3, 0, 3, 0],
                      [1, 4, 1, 0]]) / 6
        )

        self.__delta = 0.01
        self.__n = int(1 / self.__delta)


    def generate_curves(self, ctrl_pts_) -> list[list[list[float]]]:
        NN = len(ctrl_pts_)
        n_root = int(math.sqrt(NN))
        if n_root**2 != NN:
            raise ValueError("The number of control points is not a perfect square")
        ctrl_pts = []
        for i in range(n_root):
            curve = [np.array(ctrl_pts_[i*n_root + j]) for j in range(n_root)]
            ctrl_pts.append(np.array(curve))
        
        ctrl_pts = np.array(ctrl_pts)
        return self.generate_curve(ctrl_pts)  


    def generate_curve(self, ctrl_points) -> list[list[list[float]]]:
        points = []
        NS = len(ctrl_points)
        NT = len(ctrl_points[0])
        DS = int(1 / NS)
        DT = int(1 / NT)

        E_s = np.array(
            [
                [0, 0, 0, 1],
                [DS**3, DS**2, DS, 0],
                [6 * DS**3, 2 * DS**2, 0, 0],
                [6 * DS**3, 0, 0, 0],
            ]
        )
        E_t = np.array(
            [
                [0, 0, 0, 1],
                [DT**3, DT**2, DT, 0],
                [6 * DT**3, 2 * DT**2, 0, 0],
                [6 * DT**3, 0, 0, 0],
            ]
        ).transpose()
        for i in range(NS - 3):
            G = np.array(ctrl_points[i:i+4])
            g_x, g_y = G[:, :, 0], G[:, :, 1]

            c_x = self.__MBS @ g_x @ self.__MBS.transpose()
            c_y = self.__MBS @ g_y @ self.__MBS.transpose()

            DDx = E_s @ c_x @ E_t
            DDy = E_s @ c_y @ E_t

            x, dx, d2x, d3x = np.matmul(E_s, c_x)
            y, dy, d2y, d3y = np.matmul(E_s, c_y)

            points.extend(self.fwd_diff(x, dx, d2x, d3x, y, dy, d2y, d3y))

        return points


    def Q(self, s:float, t:float, G:np.array) -> list[float]:
        S = self.params(s)
        SMB = np.matmul(S, self.__MBS)
        TT = self.params(t)
        MTT = np.matmul(self.__MBS.transpose(), TT)
        x = SMB @ G[:, :, 0] @ MTT
        y = SMB @ G[:, :, 1] @ MTT
        return x, y


    def params(self, u: float, N=4):
        array = [u**j for j in range(N-1, -1, -1)]
        return np.array(array)
    
    def fwd_diff(self, x, dx, d2x,
                 d3x, y, dy, d2y, d3y) -> list[tuple[float, float]]:
        points = [(x, y)]

        for _ in range(self.__n):
            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y 
            points.append((x, y))

        return points
