import numpy as np
from enum import Enum
from random import randint
from abc import ABC
from src.TransformationUtils.Transformations import Rotation3DType, Transformation

class ObjectType(Enum):
    OBJECT3D = 1
    POINT = 2
    LINE = 3
    WIREFRAME = 4
    BEZIER_CURVE = 5
    BSPLINE_CURVE = 6


class Objeto3D(ABC):
    def __init__(self, name: str, coords: list[tuple[float]],
                 obj_type=ObjectType.OBJECT3D, color="#000000"):
        self.__name, self.__coords, self.__obj_type = self.certify_format(name, coords, obj_type)
        self.__color = color

    def apply_transformations(self, transformations: list[Transformation],
                              transform_vector_function: callable) -> None:
        for transform in transformations:
            match transform.__class__.__name__:
                case "Translation":
                    # The user-entered coordinates represent the desired translation,
                    # but when the window is rotated, 
                    # the object's coordinates need to be updated differently.
                    # This is achieved by using the unrotated vector.
                    self.translation(*transform_vector_function(transform.dx, transform.dy, transform.dz))
                case "Rotation":
                    self.rotation(
                        transform.rotation_type,
                        transform.angle,
                        transform.p1,
                        transform.p2
                    )
                case "Scaling":
                    self.scaling(transform.sx, transform.sy, transform.sz)

    def get_translation_matrix(self, dx: float, dy: float, dz:float=0) -> np.array:
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]])

    def get_scaling_matrix(self, sx: float, sy: float, sz: float=0) -> np.array:
        return np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])

    def get_X_rotation_matrix(self, angle: float) -> np.array:
        theta = np.radians(angle)
        return np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(theta), np.sin(theta), 0],
                [0, -np.sin(theta), np.cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

    def get_Y_rotation_matrix(self, angle: float) -> np.array:
        theta = np.radians(angle)
        return np.array(
            [
                [np.cos(theta), 0, -np.sin(theta), 0],
                [0, 1, 0, 0],
                [np.sin(theta), 0, np.cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

    def get_Z_rotation_matrix(self, angle: float) -> np.array:
        theta = np.radians(angle)
        return np.array(
            [
                [np.cos(theta), np.sin(theta), 0, 0],
                [-np.sin(theta), np.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

    def geometric_center(self) -> tuple[float]:
        return tuple(np.mean(self.__coords, axis=0))

    def translation(self, dx: float, dy: float, dz: float=0) -> None:
        matrix = self.get_translation_matrix(dx, dy, dz)
        self.__coords = self.calculate_coords(matrix, convert=False)

    def scaling(self, sx: float, sy: float, sz:float=0) -> None:
        cx, cy, cz = self.geometric_center()
        temp_matrix = np.matmul(
            self.get_translation_matrix(-cx, -cy, -cz),
            self.get_scaling_matrix(sx, sy, sz)
        )
        scaling_matrix = np.matmul(temp_matrix,
                                   self.get_translation_matrix(cx, cy, cz))

        self.__coords = self.calculate_coords(scaling_matrix, convert=False)


    def __get_vector_angle(self, p1:tuple[float, float, float],
                           p2:tuple[float, float, float]) -> tuple[float, float, float]:
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        Qx = np.arctan2(dy, dx)
        Qy = np.arctan2(dz, dy)
        Qz = np.arctan2(dx, dz)        
        return Qx, Qy, Qz


    def __aux_rotation(self,
                       P:tuple[float, float, float],
                       p2:tuple[float, float, float],
                       angle: float) -> np.array:
        Qx, Qy, Qz = self.__get_vector_angle(P, p2)
        dx, dy, dz = P
        T = self.get_translation_matrix(-dx, -dy, -dz)
        Rx = self.get_X_rotation_matrix(Qx)
        Rz = self.get_Z_rotation_matrix(Qz)
        temp_matrix = np.matmul(T, Rx)
        temp_matrix = np.matmul(temp_matrix, Rz)
        # rotation itself
        Ry = self.get_Y_rotation_matrix(angle)
        temp_matrix = np.matmul(temp_matrix, Ry)
        # undoing auxiliary transformations
        Rx_reverse = self.get_X_rotation_matrix(-Qx)
        Rz_reverse = self.get_Z_rotation_matrix(-Qz)
        T_reverse = self.get_translation_matrix(dx, dy, dz)
        temp_matrix = np.matmul(temp_matrix, Rz_reverse)
        temp_matrix = np.matmul(temp_matrix, Rx_reverse)
        temp_matrix = np.matmul(temp_matrix, T_reverse)
        return temp_matrix


    def rotation(self,
                 rotation_type: str="RotationType.Z",
                 angle: float=90,
                 p1:tuple[float, float, float]=(0,0,0),
                 p2:tuple[float, float, float]=(0,0,0)) -> None:
        matrix = []

        if rotation_type == str(Rotation3DType.X):
            matrix = self.get_X_rotation_matrix(angle)
        elif rotation_type == str(Rotation3DType.Y):
            matrix = self.get_Y_rotation_matrix(angle)
        elif rotation_type == str(Rotation3DType.Z):
            matrix = self.get_Z_rotation_matrix(angle)
        elif rotation_type == str(Rotation3DType.center_X):
            center = self.geometric_center()
            p2 = (center[0] + 1, center[1], center[2])
            matrix = self.__aux_rotation(center, p2, angle)
        elif rotation_type == str(Rotation3DType.center_Y):
            center = self.geometric_center()
            p2 = (center[0], center[1] + 1, center[2])
            matrix = self.__aux_rotation(center, p2, angle)
        elif rotation_type == str(Rotation3DType.center_Z):
            center = self.geometric_center()
            p2 = (center[0], center[1], center[2] + 1)
            matrix = self.__aux_rotation(center, p2, angle)
        elif rotation_type == str(Rotation3DType.any_axis):
            matrix = self.__aux_rotation(p1, p2, angle)
        else:
            print("Invalid rotation type")
            return

        self.__coords = self.calculate_coords(matrix, convert=False)
    
    
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
        return [tuple(float(j) for j in i[:-1]) for i in coords.tolist()]


    def calculate_coords(self, matrix: np.ndarray, convert=True) -> list[tuple[float]]:
        R = np.array(
            [
                np.dot(np.array([coord[0], coord[1], coord[2], 1]), matrix)[:-1]
                for coord in self.__coords
            ]
        )
        if convert:
            R = self.__convert_to_tuples_list(R)
        return R

    
    def certify_format(self, name:str, coords:list[tuple[float]],
                       obj_type:str) -> tuple[str, np.array, ObjectType]:
        if not isinstance(name, str):
            print("Invalid name for", name, ", renamed to 'obj'")
            name = 'obj'
        if len(coords) == 0:
            print("No coordinates defined for", name, ", defined as (0,0,0)")
            coords = [(0,0,0)]
        if obj_type not in [ObjectType.POINT, ObjectType.LINE,
                                 ObjectType.WIREFRAME, ObjectType.OBJECT3D,
                                 ObjectType.BEZIER_CURVE, ObjectType.BSPLINE_CURVE]:
            print("Invalid object type", obj_type)
            print("Object type not defined for", name, ", automatically guessed")
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
        if len(coords) > 2 and obj_type not in [ObjectType.WIREFRAME,
                                                ObjectType.BEZIER_CURVE,
                                                ObjectType.BSPLINE_CURVE]:
            print("Wrong object type")
            obj_type = ObjectType.WIREFRAME
        if (obj_type == ObjectType.BEZIER_CURVE or obj_type == ObjectType.BSPLINE_CURVE) and len(coords) < 4:
            added_points = [(randint(-1000, 1000),
                             randint(-1000, 1000),
                             randint(-1000, 1000)) for _ in range(4 - len(coords))]
            print("Insufficient Control Points for Curve")
            print(f"The following random points will be added to the coordinates: {added_points}")
            coords.extend(added_points)
        if not all(isinstance(i, tuple) for i in coords):
            print("Invalid format for coordinates, should be a list of tuples")
            coords = [tuple(i) for i in coords]
        if any(len(i) < 3 for i in coords):
            print("Invalid format for coordinates, 3 values are needed for each point")
            print("points with less than 3 values will be remanaged to (0,0,0)")
            for i in range(len(coords)):
                if len(coords[i]) < 3:
                    coords[i] = (0, 0, 0)
        if any(len(i) > 3 for i in coords):
            print(
                "Invalid format for coordinates, only 3 values are needed for each point"
            )
            print("extra values will be removed")
            coords = [(j[i] for i in range(3)) for j in coords]
        if not all(isinstance(i, (float, float, float)) for i in coords):
            try:
                coords = [tuple(float(i) for i in j) for j in coords]
            except:
                print("Invalid format for coordinates, the tuples should be made of floats")
                print("coordinates will be remanaged to (i, i, i)")
                coords = [(i, i, i) for i in range(len(coords))]
        output_coords = np.array(coords)
        return name, output_coords, obj_type
