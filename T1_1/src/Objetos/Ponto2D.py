from src.Objetos.Objeto2D import Objeto2D

class Ponto2D(Objeto2D):
    def __init__(self, name:str, coordenadas=[(0, 0)], obj_type="Point"):
        super().__init__(name, coordenadas, obj_type)

