from src.Objetos.Objeto2D import Objeto2D

class WireFrame(Objeto2D):
    def __init__(self, name, coordenadas=[(0, 0), (1, 1), (0, 2)], obj_type="Wireframe"):
        super().__init__(name, coordenadas, obj_type)
