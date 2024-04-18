import numpy as np

class Transformator:
    def __init__(self, system:str="SCN", height: int = 400, width: int = 600):
        self.__system = system

        self.__xwmin = self.__ywmin = 0
        self.__xwmax = width
        self.__ywmax = height
        # middle point of the window
        self.__center = np.array([width / 2, height / 2, 1])
        self.__scaling_factor = 1


        self.__SCN_matrix = None
        # view up vector
        self.__viewup = np.array([0, 1, 1])
        self.__viewup_angle = 0
        self.set_normalization_matrix(0)

    def set_normalization_matrix(self, angle: float = 0):
        self.__update_view_up_vector(np.radians(angle))

        theta = self.__viewup_angle

        #print("theta:", theta, "rad of:", angle, "degrees")
        T = np.array([
                      [1, 0, 0], [0, 1, 0],
                      [-self.__center[0], -self.__center[1], 1]
                     ])
        R = self.__get_rotate_matrix(theta)
        #print("\nviewup:", self.__viewup)
        S = np.array(
            [
                [2 * self.__scaling_factor / (self.__xwmax - self.__xwmin), 0, 0],
                [0, 2 * self.__scaling_factor / (self.__ywmax - self.__ywmin), 0],
                [0, 0, 1],
            ]
        )
        # self.__SCN_matrix = T @ R @ S
        self.__SCN_matrix = np.matmul(np.matmul(T, R), S)

    def __update_view_up_vector(self, theta: np.ndarray):
        rotate_matrix = self.__get_rotate_matrix(theta)
        self.__viewup = np.matmul(self.__viewup, rotate_matrix)

        # The arctan2 function gives the angle that the vector makes with the positive x-axis.
        # To get the angle made with the positive y-axis, we subtract the result from pi/2.
        # The multiplication by -1 is needed to make the rotation counter-clockwise.
        self.__viewup_angle = -1 * (np.pi / 2 - np.arctan2(self.__viewup[1], self.__viewup[0]))

    def unrotate_vector(self, dx: float, dy: float) -> tuple[float, float]:
        old_vector = np.array([dx, dy, 0])
        rotate_matrix = self.__get_rotate_matrix(- self.__viewup_angle)
        new_vector = np.dot(old_vector, rotate_matrix)
        return new_vector[0], new_vector[1]

    def __get_rotate_matrix(self, theta: float) -> np.array:
        return np.array([[np.cos(theta), np.sin(theta), 0],
                         [-np.sin(theta), np.cos(theta), 0],
                         [0, 0, 1]])

    def __get_translate_matrix(self, dx: float, dy: float) -> np.array:
        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
    
    @property
    def matrix(self) -> np.array:
        return self.__SCN_matrix
    
    @property
    def scaling_factor(self) -> float:
        return self.__scaling_factor
    
    @scaling_factor.setter
    def scaling_factor(self, value: float):
        self.__scaling_factor = value
    
    @property
    def center(self) -> np.array:
        return self.__center
    
    def update_center(self, dx:float, dy:float):
        changed_x, changed_y = self.unrotate_vector(dx, dy)
        translate_matrix = self.__get_translate_matrix(changed_x, changed_y)
        self.__center = np.dot(self.__center, translate_matrix)
