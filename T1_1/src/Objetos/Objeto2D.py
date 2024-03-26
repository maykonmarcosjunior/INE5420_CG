import numpy as np


class Objeto2D:
    def __init__(self, name: str, coords: list[tuple[float]], obj_type=None, color="#000000"):
        self.__name, self.__coords, self.__obj_type = self.certify_format(name, coords, obj_type)
        self.__color = color

    def geometric_center(self) -> tuple[float]:
        return tuple(np.mean(self.__coords, axis=0))
    
    def translation(self, dx: float, dy: float):
        self.__coords += [dx, dy]
    
    def enlargement(self, factor: float):
        cx, cy = self.geometric_center()
        self.translation(-cx, -cy)
        self.__coords *= factor
        self.translation(cx, cy)
    
    def simple_rotation(self, angle: float):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        self.__coords = np.dot(self.__coords, rotation_matrix)
    
    def rotation(self, angle: float, center: tuple[float]):
        dx, dy = center
        self.translation(-dx, -dy)
        self.simple_rotation(angle)
        self.translation(dx, dy)

    def center_rotation(self, angle: float):
        self.rotation(angle, self.geometric_center())

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def coordinates(self) -> list[tuple[float]]:
        return [tuple(i) for i in self.__coords.tolist()]
    
    @property
    def obj_type(self) -> str:
        return self.__obj_type
    
    @property
    def color(self) -> str:
        return self.__color

    def __str__(self):
        coords = [tuple(round(i, 2) for i in j) for j in self.__coords]
        return f"{self.obj_type}: - {self.__name} - {coords}"
    
    def certify_format(self, name:str, coords:list[tuple[float]], obj_type:str):
        if not isinstance(name, str):
            print("Invalid name for", self, ", renamed to 'obj'")
            name = 'obj'
        if len(coords) == 0:
            print("No coordinates defined for", self, ", defined as (0,0)")
            coords = [(0,0)]
        if obj_type not in ["Point", "Line", "Wireframe"]:
            print("Invalid object type")
            obj_type = None
        if obj_type is None:
            print("Object type not defined for", self, ", automatically guessed")
            if len(coords) == 1:
                obj_type = "Point"
            elif len(coords) == 2:
                obj_type = "Line"
            else:
                obj_type = "Wireframe"            
        if len(coords) == 1 and obj_type != "Point":
            print("Wrong object type")
            obj_type = "Point"
        if len(coords) == 2 and obj_type != "Line":
            print("Wrong object type")
            obj_type = "Line"
        if len(coords) > 2 and obj_type != "Wireframe":
            print("Wrong object type")
            obj_type = "Wireframe"
        if not all(isinstance(i, tuple) for i in coords):
            print("Invalid format for coordinates, should be a list of tuples")
            coords = [tuple(i) for i in coords]
        if any(len(i) < 2 for i in coords):
            print("Invalid format for coordinates, 2 values are needed for each point")
            print("points with less than 2 values will be remanaged to (0,0)")
            for i in range(len(coords)):
                if len(coords[i]) < 2:
                    coords[i] = (0,0)
        if any(len(i) > 2 for i in coords):
            print("Invalid format for coordinates, only 2 values are needed for each point")
            print("extra values will be removed")
            coords = [(j[i] for i in range(2)) for j in coords]
        if not all(isinstance(i, (float, float)) for i in coords):
            print("Invalid format for coordinates, the tuples should be made of floats")
            coords = [tuple(float(i) for i in j) for j in coords]
        output_coords = np.array(coords)
        return name, output_coords, obj_type
        
