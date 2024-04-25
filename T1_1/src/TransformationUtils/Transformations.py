from enum import Enum
from abc import ABC


class RotationType(Enum):
    world_center = 0
    object_center = 1
    any_point = 2


class Rotation3DType(Enum):
    X = 0
    Y = 1
    Z = 2
    center_X = 3
    center_Y = 4
    center_Z = 5
    any_axis = 6

class Transformation(ABC):
    def __init__(self):
        pass


class Translation(Transformation):
    def __init__(self, dx: float, dy: float, dz: float=0):
        super().__init__()
        self.__dx = dx
        self.__dy = dy
        self.__dz = dz

    @property
    def dx(self) -> float:
        return self.__dx

    @property
    def dy(self) -> float:
        return self.__dy

    @property
    def dz(self) -> float:
        return self.__dz

    def __str__(self) -> str:
        return f"Translation: dx: {self.__dx} dy: {self.__dy} dz: {self.__dz}"


class Scaling(Transformation):
    def __init__(self, sx: float, sy: float, sz: float=1):
        super().__init__()
        self.__sx = sx
        self.__sy = sy
        self.__sz = sz

    @property
    def sx(self) -> float:
        return self.__sx

    @property
    def sy(self) -> float:
        return self.__sy

    @property
    def sz(self) -> float:
        return self.__sz

    def __str__(self) -> str:
        return f"Scaling: sx: {self.__sx} sy: {self.__sy} sz: {self.__sz}"


class Rotation(Transformation):
    def __init__(self, rotation_type: str, angle: float, x: float = 0, y: float = 0, z: float = 0):
        super().__init__()

        self.__rotation_type = rotation_type
        self.__angle = angle
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def rotation_type(self) -> str:
        return self.__rotation_type

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def z(self) -> float:
        return self.__z

    def __str__(self) -> str:
        return f"Rotation: {self.__rotation_type}, angle: {self.__angle}, x: {self.__x}, y: {self.__y} z: {self.__z}"
