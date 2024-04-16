from src.Objetos.Objeto2D import Objeto2D, ObjectType

class WireFrame(Objeto2D):
    def __init__(self, name, coordenadas=[(0, 0), (1, 1), (0, 2)], obj_type=ObjectType.WIREFRAME, color="000000", fill=False):
        super().__init__(name, coordenadas, obj_type, color)
        self.__fill = fill

    @property
    def fill(self) -> bool:
        return self.__fill
