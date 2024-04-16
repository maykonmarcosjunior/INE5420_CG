from src.Objetos.Objeto2D import Objeto2D, ObjectType
import numpy as np


class CurvaBezier(Objeto2D):
    def __init__( self, name, coordenadas=[(0, 0), (1, 1)], obj_type=ObjectType.BEZIER_CURVE, color="#000000"):
        super().__init__(name, coordenadas, obj_type, color)

        # As coordenadas guardadas são os pontos de controle

        self.__M_b = np.array(
            [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]
        )

    def generate_curve(self, control_points_normalized):
        curve_pieces = []
        for i in range(0, len(control_points_normalized) - 2 - (len(control_points_normalized) - 1) % 3, 3):
            curve_pieces.append(
                self.__calculate_curve_piece(np.array(control_points_normalized[i : i + 4]))
            )

        return curve_pieces

    def __calculate_curve_piece(self, control_points: np.array, point_number=100):
        sub_curve = []
        t_values = np.linspace(0, 1, point_number)

        for t in t_values:
            T = np.array([t**3, t**2, t, 1])
            TM_b = np.matmul(T, self.__M_b)

            x = np.matmul(TM_b, control_points[:, 0]) # Multiply the TM_b by the x coordinates in control points
            y = np.matmul(TM_b, control_points[:, 1]) # Multiply the TM_b by the y coordinates in control points
            sub_curve.append([x, y])

        return sub_curve
