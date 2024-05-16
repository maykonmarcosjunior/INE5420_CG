import math
from src.Objetos.Objeto3D import Objeto3D, ObjectType
import numpy as np

"""
Estenda o seu sistema para representar superfícies 3D através de suas matrizes de geometria.
Cada superfície pode ser representada por uma lista de matrizes, cada matriz representando um “retalho”.
Crie uma tela de entrada de dados onde você pode entrar com conjuntos de pontos de controle, 16 a 16, no mesmo padrão dos outros objetos com as linhas da matriz separadas por ";":
(x_11,y_11,z_11),(x_12,y_12,z_12),...;(x_21,y_21,z_21),(x_22,y_22,z_22),...;...(x_ij,y_ij,z_ij)
O clipping é em 2D.
"""

class BezierBicurve(Objeto3D):
    def __init__(self, name: str, coords: list[list[tuple[float]]],
                 obj_type=ObjectType.BEZIER_BICURVE, color="#000000",
                 curves: list[tuple[int]]=[]):
        new_coords = []
        for curve in coords:
            new_coords.extend(curve)
        super().__init__(name, new_coords, obj_type, color, curves)
        
        self.__G = np.array([np.array(c) for c in coords])
        self.__MB = np.array(
            [
             [-1, 3, -3, 1],
             [3, -6, 3, 0],
             [-3, 3, 0, 0],
             [1, 0, 0, 0]
            ]
        )
        self.__n_points = 50

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
        #curves = [self.generate_curve(c) for c in ctrl_pts]
        curves = self.calculate_piece(ctrl_pts)
        curves.extend(self.calculate_piece(ctrl_pts.transpose(1, 0, 2)))
        return curves

    def generate_curve(self, ctrl_pts:np.array) -> list[list[float]]:
        curve_pieces = []
        # The groups overlap to give the curve continuity
        N = len(ctrl_pts)
        L = N - 2 - (N - 1) % 3
        for i in range(0, L, 3):
            sub_matrix = [curve[i:i+4] for curve in ctrl_pts[i : i + 4]]
            curve_pieces.extend(
                self.calculate_piece(np.array(sub_matrix))
            )
        return curve_pieces


    def calculate_piece(self, G:np.array) -> list[list[float]]:
        param_values = np.linspace(0, 1, self.__n_points)
        sub_curves = []
        for s in param_values:
            sub_curve = []
            for t in param_values:
                sub_curve.append(self.Q(s, t, G))
            sub_curves.append(sub_curve)    
        return sub_curves


    def Q(self, s:float, t:float, G:np.array) -> list[float]:
        S = self.params(s)
        SMB = np.matmul(S, self.__MB)
        TT = self.params(t)
        MTT = np.matmul(self.__MB.transpose(), TT)
        x = SMB @ G[:, :, 0] @ MTT
        y = SMB @ G[:, :, 1] @ MTT
        return x, y


    def params(self, u: float, N=4):
        array = [u**j for j in range(N-1, -1, -1)]
        return np.array(array)


    @property
    def curves(self):
        return self.__G
