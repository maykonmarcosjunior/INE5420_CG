from src.Objetos.Objeto2D import Objeto2D
from src.Objetos.Objeto3D import ObjectType

class Linha2D(Objeto2D):
    def __init__(self, name, coordenadas=[(0, 0), (1, 1)],
                 obj_type=ObjectType.LINE, color="#000000"):
        super().__init__(name, coordenadas, obj_type, color)
