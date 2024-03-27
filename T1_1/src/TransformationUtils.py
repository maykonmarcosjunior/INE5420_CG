import tkinter as tk
from abc import abstractmethod
from typing import Type
from src.Transformations import (
    RotationType,
    Rotation,
    Scaling,
    Translation,
    Transformation,
)


class TransformationsMenu(tk.Toplevel):
    def __init__(self, object_name: str, master=None, width=400, height=300):
        super().__init__(master)

        self.__transformations: list[Transformation] = []

        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.title(f"Object Transformations - {object_name}")

        tk.Label(self, text="Transformations", font="System 12 bold").pack(
            fill=tk.X, pady=15
        )

        tk.Button(
            self, text="Translate Object", command=self.__translate_toplevel
        ).pack(pady=15)
        tk.Button(self, text="Scale Object", command=self.__scale_toplevel).pack(
            pady=15
        )
        tk.Button(self, text="Rotate Object", command=self.__rotate_toplevel).pack(
            pady=15
        )

        tk.Button(
            self,
            text="Apply All Transformations",
            command=self.__apply_all,
            bg="green",
            fg="white",
        ).pack(pady=15)

    def __apply_all(self) -> None:
        self.destroy()

    def show_window(self) -> dict:
        self.wait_window()
        return self.__transformations

    def __translate_toplevel(self) -> None:
        t_toplevel = TranslateToplevel(self)
        translation = t_toplevel.show_window()

        if translation is not None:
            self.__transformations.append(translation)

    def __scale_toplevel(self) -> None:
        s_toplevel = ScaleToplevel(self)
        scaling = s_toplevel.show_window()

        if scaling is not None:
            self.__transformations.append(scaling)

    def __rotate_toplevel(self) -> None:
        r_toplevel = RotateToplevel(self)
        rotation = r_toplevel.show_window()

        if rotation is not None:
            self.__transformations.append(rotation)


class TransformationToplevel(tk.Toplevel):
    def __init__(
        self, master=None, title: str = "Options", width: int = 300, height: int = 300
    ):
        super().__init__(master)

        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.title(title)

        self._transformation_applied = False

        self._place_labels_and_entries()

        self._apply_button = tk.Button(
            self, text="Apply", command=self._apply_transformation
        )
        self._apply_button.pack(pady=10)

    def _apply_transformation(self) -> None:
        self._transformation_applied = True
        if self._validate_entries():
            self.destroy()

    @abstractmethod
    def _validate_entries(self) -> bool:
        pass

    @abstractmethod
    def _place_labels_and_entries(self) -> None:
        pass

    @abstractmethod
    def show_window(self) -> Type["TransformationToplevel"]:
        pass


class RotateToplevel(TransformationToplevel):
    def __init__(self, master=None, title="Rotation Options", width=300, height=300):
        super().__init__(master, title, width, height)

        self.__rotation_type = tk.StringVar()
        self.__rotation_type.set(RotationType.object_center)

        self.__choosed_rotation_type = None
        self.__angle = None
        self.__x = self.__y = 0

        self.__x_label = tk.Label(self, text="X:")
        self.__x_entry = tk.Entry(self)
        self.__y_label = tk.Label(self, text="Y:")
        self.__y_entry = tk.Entry(self)

    def _place_labels_and_entries(self) -> None:
        tk.Radiobutton(
            self,
            text="Rotation around the center of the world",
            variable=self.__rotation_type,
            value=RotationType.world_center,
            command=self.__on_rotation_type_change,
        ).pack()
        tk.Radiobutton(
            self,
            text="Rotation around the center of the object",
            variable=self.__rotation_type,
            value=RotationType.object_center,
            command=self.__on_rotation_type_change,
        ).pack()
        tk.Radiobutton(
            self,
            text="Rotation around any point",
            variable=self.__rotation_type,
            value=RotationType.any_point,
            command=self.__on_rotation_type_change,
        ).pack()

        tk.Label(self, text="Rotation Angle (in degrees):").pack()
        self.__angle_entry = tk.Entry(self)
        self.__angle_entry.pack()

    def __on_rotation_type_change(self) -> None:
        if self.__rotation_type.get() == str(RotationType.any_point):
            self._apply_button.pack_forget()
            self.__x_label.pack()
            self.__x_entry.pack()
            self.__y_label.pack()
            self.__y_entry.pack()
            self._apply_button.pack()
            return
        self.__x_label.pack_forget()
        self.__y_label.pack_forget()
        self.__x_entry.pack_forget()
        self.__y_entry.pack_forget()

    def _validate_entries(self, rotation_type: str) -> bool:
        try:
            self.__angle = float(self.__angle_entry.get())
            if rotation_type == str(RotationType.any_point):
                self.__x = float(self.__x_entry.get())
                self.__y = float(self.__y_entry.get())
            return True
        except ValueError as e:
            print("Error:", e)
            return False

    def _apply_transformation(self):
        self.__choosed_rotation_type = self.__rotation_type.get()
        self._transformation_applied = True
        if self._validate_entries(self.__choosed_rotation_type):
            self.destroy()

    def show_window(self):
        self.wait_window()
        if self._transformation_applied:
            return Rotation(
                self.__choosed_rotation_type, self.__angle, self.__x, self.__y
            )
        return None


class ScaleToplevel(TransformationToplevel):
    def __init__(self, master=None, title="Scaling Options", width=300, height=300):
        super().__init__(master, title, width, height)

        self.__sx = self.__sy = None

    def _place_labels_and_entries(self) -> None:
        tk.Label(self, text="Sx:").pack()
        self.__sx_entry = tk.Entry(self)
        self.__sx_entry.pack()

        tk.Label(self, text="Sy:").pack()
        self.__sy_entry = tk.Entry(self)
        self.__sy_entry.pack()

    def _validate_entries(self) -> bool:
        try:
            self.__sx = float(self.__sx_entry.get())
            self.__sy = float(self.__sy_entry.get())
            return True
        except ValueError as e:
            print("Error:", e)
            return False

    def show_window(self):
        self.wait_window()
        if self._transformation_applied:
            return Scaling(self.__sx, self.__sy)
        return None


class TranslateToplevel(TransformationToplevel):
    def __init__(self, master=None, title="Translation Options", width=300, height=300):
        super().__init__(master, title, width, height)

        self.__dx = self.__dy = None

    def _place_labels_and_entries(self) -> None:
        tk.Label(self, text="Dx:").pack()
        self.__dx_entry = tk.Entry(self)
        self.__dx_entry.pack()

        tk.Label(self, text="Dy:").pack()
        self.__dy_entry = tk.Entry(self)
        self.__dy_entry.pack()

    def _validate_entries(self) -> bool:
        try:
            self.__dx = float(self.__dx_entry.get())
            self.__dy = float(self.__dy_entry.get())
            return True
        except ValueError as e:
            print("Error:", e)
            return False

    def show_window(self) -> Translation:
        self.wait_window()
        if self._transformation_applied:
            return Translation(self.__dx, self.__dy)
        return None
