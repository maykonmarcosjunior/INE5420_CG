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
        
        self.__G = np.array([np.array(c) for c in coords])
        self.__MBSpline = np.array(
            [
             [-1, 3, -3, 1],
             [3, -6, 3, 0],
             [-3, 0, 3, 0],
             [1, 4, 1, 0]
            ]
        )
        self.__n_points = 100
