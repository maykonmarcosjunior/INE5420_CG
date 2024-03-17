class Objeto2D:
    def __init__(self, name: str, coords:list[tuple[float]]):
        self.__name = name
        self.__coords = coords
    
    def __str__(self):
        return f"Objeto2D: {self.__name} - {self.__coords}"
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def coords(self) -> list[tuple[float]]:
        return self.__coords
