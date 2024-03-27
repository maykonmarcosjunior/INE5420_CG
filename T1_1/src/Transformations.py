from enum import Enum
from abc import ABC


class RotationType(Enum):
    world_center = 0
    object_center = 1
    any_point = 2


class Transformation(ABC):
    def __init__(self):
        pass


class Translation(Transformation):
    def __init__(self, dx: float, dy: float):
        super().__init__()
        self.__dx = dx
        self.__dy = dy

    @property
    def dx(self) -> float:
        return self.__dx

    @property
    def dy(self) -> float:
        return self.__dy

    def __str__(self) -> str:
        return f"Translation: dx: {self.__dx} dy: {self.__dy}"


class Scaling(Transformation):
    def __init__(self, sx: float, sy: float):
        super().__init__()
        self.__sx = sx
        self.__sy = sy

    @property
    def sx(self) -> float:
        return self.__sx

    @property
    def sy(self) -> float:
        return self.__sy

    def __str__(self) -> str:
        return f"Scaling: sx: {self.__sx} sy: {self.__sy}"


class Rotation(Transformation):
    def __init__(self, rotation_type: str, angle: float, x: float = 0, y: float = 0):
        super().__init__()

        self.__rotation_type = rotation_type
        self.__angle = angle
        self.__x = x
        self.__y = y

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

    def __str__(self) -> str:
        return f"Rotation: {self.__rotation_type}, angle: {self.__angle}, x: {self.__x}, y: {self.__y}"
