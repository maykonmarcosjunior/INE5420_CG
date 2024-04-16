import tkinter as tk
from src.TransformationUtils.TopLevel.TransformationTopLevel import TransformationToplevel
from src.TransformationUtils.Transformations import Translation


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
