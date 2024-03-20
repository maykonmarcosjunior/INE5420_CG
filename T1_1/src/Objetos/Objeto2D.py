class Objeto2D:
    def __init__(self, name: str, coords:list[tuple[float]], obj_type=None):
        self.__name = name
        self.__coords = coords
        self.__obj_type = obj_type
    
    def __str__(self):
        return f"Objeto2D: {self.__name} - {self.__coords}"
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def coordinates(self) -> list[tuple[float]]:
        return self.__coords
    
    @property
    def obj_type(self) -> str:
        return self.__obj_type
