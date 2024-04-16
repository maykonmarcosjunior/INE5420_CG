import tkinter as tk
from src.TransformationUtils.TopLevel.TransformationTopLevel import TransformationToplevel
from src.TransformationUtils.Transformations import RotationType, Rotation


class RotateToplevel(TransformationToplevel):
    def __init__(self, master=None, title="Rotation Options", width=300, height=300):
        super().__init__(master, title, width, height)


        self.__choosed_rotation_type = None
        self.__angle = None
        self.__x = self.__y = 0

        self.__x_label = tk.Label(self, text="X:")
        self.__x_entry = tk.Entry(self)
        self.__y_label = tk.Label(self, text="Y:")
        self.__y_entry = tk.Entry(self)

    def _place_labels_and_entries(self) -> None:
        self.__rotation_type = tk.StringVar()
        self.__rotation_type.set(RotationType.object_center)
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
