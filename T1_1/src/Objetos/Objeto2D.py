import numpy as np
from enum import Enum
from random import randint
from src.Objetos.Objeto3D import Objeto3D
from src.TransformationUtils.Transformations import RotationType, Transformation

class ObjectType(Enum):
    OBJECT2D = 1
    POINT = 2
    LINE = 3
    WIREFRAME = 4
    BEZIER_CURVE = 5
    BSPLINE_CURVE = 6


class Objeto2D(Objeto3D):
    def __init__(self, name: str, coords: list[tuple[float]], obj_type=None, color="#000000"):
        super_coords = [(c[0], c[1], 0.0) for c in coords]
        super().__init__(name, super_coords, obj_type, color)

'''
    def calculate_coords(self, matrix: np.ndarray) -> list[tuple[float]]:
        R = np.array(
            [
                np.dot(np.array([coord[0], coord[1], 1]), matrix)[:-1]
                for coord in self.__coords
            ]
        )
        return self.__convert_to_tuples_list(R)
        
    
    def apply_transformations(self, transformations: list[Transformation], transform_vector_function: callable) -> None:
        for transform in transformations:
            match transform.__class__.__name__:
                case "Translation":
                    # The user-entered coordinates represent the desired translation,
                    # but when the window is rotated, 
                    # the object's coordinates need to be updated differently.
                    # This is achieved by using the unrotated vector.
                    self.translation(*transform_vector_function(transform.dx, transform.dy))
                case "Rotation":
                    self.rotation(
                        transform.rotation_type,
                        transform.angle,
                        transform.x,
                        transform.y,
                    )
                case "Scaling":
                    self.scaling(transform.sx, transform.sy)

    def __get_translation_matrix(self, dx: float, dy: float) -> np.array:
        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    def __get_scaling_matrix(self, sx: float, sy: float) -> np.array:
        return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def __get_rotation_matrix(self, angle: float) -> np.array:
        theta = np.radians(angle)
        return np.array(
            [
                [np.cos(theta), np.sin(theta), 0],
                [-np.sin(theta), np.cos(theta), 0],
                [0, 0, 1],
            ]
        )

    def geometric_center(self) -> tuple[float]:
        return tuple(np.mean(self.__coords, axis=0))

    def translation(self, dx: float, dy: float) -> None:
        matrix = self.__get_translation_matrix(dx, dy)
        self.__coords = np.array(
            [
                np.dot(np.array([coord[0], coord[1], 1]), matrix)[:-1]
                for coord in self.__coords
            ]
        )

    def scaling(self, sx: float, sy: float) -> None:
        cx, cy = self.geometric_center()
        temp_matrix = np.matmul(
            self.__get_translation_matrix(-cx, -cy), self.__get_scaling_matrix(sx, sy)
        )
        scaling_matrix = np.matmul(temp_matrix, self.__get_translation_matrix(cx, cy))

        self.__coords = np.array(
            [
                np.dot(np.array([coord[0], coord[1], 1]), scaling_matrix)[:-1]
                for coord in self.__coords
            ]
        )

    def rotation(self, rotation_type: str="RotationType.any_point", angle: float=90, x: float=0, y: float=0) -> None:
        matrix = []

        if rotation_type == str(RotationType.any_point):
            matrix = self.__aux_rotation((x, y), angle)
        elif rotation_type == str(RotationType.world_center):
            matrix = self.__get_rotation_matrix(angle)
        elif rotation_type == str(RotationType.object_center):
            matrix = self.__aux_rotation(self.geometric_center(), angle)
        else:
            print("Invalid rotation type")
            return

        self.__coords = np.array(
            [
                np.dot(np.array([coord[0], coord[1], 1]), matrix)[:-1]
                for coord in self.__coords
            ]
        )
    def __aux_rotation(self, center: tuple[float, float], angle: float) -> np.array:
        dx, dy = center
        temp_matrix = np.matmul(
            self.__get_translation_matrix(-dx, -dy), self.__get_rotation_matrix(angle)
        )
        return np.matmul(temp_matrix, self.__get_translation_matrix(dx, dy))

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def coordinates(self) -> list[tuple[float]]:
        coords = self.__convert_to_tuples_list(self.__coords)
        return coords
    
    @property
    def obj_type(self) -> str:
        return self.__obj_type
    
    @property
    def color(self) -> str:
        return self.__color

    def __str__(self):
        coords = [tuple(round(i, 2) for i in j) for j in self.coordinates]
        return f"{self.obj_type}: - {self.__name} - {coords}"
    
    def __convert_to_tuples_list(self, coords: np.ndarray) -> list[tuple[float]]:
        return [tuple(float(j) for j in i) for i in coords.tolist()]

    def certify_format(self, name:str, coords:list[tuple[float]], obj_type:str):
        if not isinstance(name, str):
            print("Invalid name for", self, ", renamed to 'obj'")
            name = 'obj'
        if len(coords) == 0:
            print("No coordinates defined for", self, ", defined as (0,0)")
            coords = [(0,0)]
        if obj_type not in ObjectType:
            print("Invalid object type")
            obj_type = None
        if obj_type is None:
            print("Object type not defined for", self, ", automatically guessed")
            if len(coords) == 1:
                obj_type = ObjectType.POINT
            elif len(coords) == 2:
                obj_type = ObjectType.LINE
            else:
                obj_type = ObjectType.WIREFRAME
        if len(coords) == 1 and obj_type != ObjectType.POINT:
            print("Wrong object type")
            obj_type = ObjectType.POINT
        if len(coords) == 2 and obj_type != ObjectType.LINE:
            print("Wrong object type")
            obj_type = ObjectType.LINE
        if len(coords) > 2 and obj_type not in [ObjectType.WIREFRAME, ObjectType.BEZIER_CURVE, ObjectType.BSPLINE_CURVE]:
            print("Wrong object type")
            obj_type = ObjectType.WIREFRAME
        if (obj_type == ObjectType.BEZIER_CURVE or obj_type == ObjectType.BSPLINE_CURVE) and len(coords) < 4:
            added_points = [(randint(-1000, 1000), randint(-1000, 1000)) for _ in range(4 - len(coords))]
            print("Insufficient Control Points for Curve")
            print(f"The following random points will be added to the coordinates: {added_points}")
            coords.extend(added_points)
        if not all(isinstance(i, tuple) for i in coords):
            print("Invalid format for coordinates, should be a list of tuples")
            coords = [tuple(i) for i in coords]
        if any(len(i) < 2 for i in coords):
            print("Invalid format for coordinates, 2 values are needed for each point")
            print("points with less than 2 values will be remanaged to (0,0)")
            for i in range(len(coords)):
                if len(coords[i]) < 2:
                    coords[i] = (0, 0)
        if any(len(i) > 2 for i in coords):
            print(
                "Invalid format for coordinates, only 2 values are needed for each point"
            )
            print("extra values will be removed")
            coords = [(j[i] for i in range(2)) for j in coords]
        if not all(isinstance(i, (float, float)) for i in coords):
            try:
                coords = [tuple(float(i) for i in j) for j in coords]
            except:
                print("Invalid format for coordinates, the tuples should be made of floats")
                print("coordinates will be remanaged to (i, i)")
                coords = [(i, i) for i in range(len(coords))]
        output_coords = np.array(coords)
        return name, output_coords, obj_type
'''
