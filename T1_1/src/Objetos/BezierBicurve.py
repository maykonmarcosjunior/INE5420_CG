from src.Objetos.Objeto3D import Objeto3D, ObjectType

class BezierBicurve(Objeto3D):
    def __init__(self, name: str, coords: list[tuple[float]],
                 obj_type=ObjectType.BEZIER_BICURVE.value, color="#000000",
                 curves: list[tuple[int]]=[]):
        super().__init__(name, coords, obj_type, color, curves)
        self.__curves = curves
        self.__coords = coords
