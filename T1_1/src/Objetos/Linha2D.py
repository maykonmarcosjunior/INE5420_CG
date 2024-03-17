from src.Objetos.Objeto2D import Objeto2D

class Linha2D(Objeto2D):
    def __init__(self, name, coordenadas=[(0, 0), (1, 1)]):
        super().__init__(name, coordenadas)
