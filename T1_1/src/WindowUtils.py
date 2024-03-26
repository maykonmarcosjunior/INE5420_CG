import tkinter as tk
from typing import Callable


class DrawWindow(tk.Toplevel):
    def __init__(self, master=None, height=400, width=600):
        super().__init__(master)
        self.__coordinates_str = None  # Value to be returned
        self.__name_str = None

        self.title("Draw Options")
        self.geometry(f"{width}x{height}")

        tk.Label(self, text="Name:").pack(pady=(10, 0))
        self.__object_name = tk.Entry(self)
        self.__object_name.pack(fill=tk.X, padx=20)

        tk.Label(
            self, text='Enter Coordinates (in the format "((x1, y1),(x2, y2),...)"):'
        ).pack(pady=(10, 0))
        self.__coord_entry = tk.Entry(self)
        self.__coord_entry.pack(fill=tk.X, padx=20)

        tk.Button(self, text="Submit", command=self.__submit_option).pack(pady=10)

    def show_window(self):
        self.wait_window()
        return self.get_name_and_coordinates()

    def __submit_option(self):
        self.__coordinates_str = self.__coord_entry.get()
        self.__name_str = self.__object_name.get()
        self.destroy()

    def get_name_and_coordinates(self) -> tuple[str, str]:
        return self.__name_str, self.__coordinates_str


class OptionsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        tk.Label(self, text="Function Menu", font="System 12 bold").pack(
            fill=tk.X, pady=(20, 0)
        )

        self.__object_frame = tk.Frame(self)
        self.__object_frame.pack(pady=10)

        self.__zoom_frame = tk.Frame(self)
        self.__zoom_frame.pack(pady=10)

        self.__nav_frame = tk.Frame(self)
        self.__nav_frame.pack(pady=10)

    def add_button(self, button_text: str, function: Callable, parent="", side=tk.TOP, padx=0, pady=0):
        tk.Button(self.__define_master(parent), text=button_text, command=function).pack(pady=pady, padx=padx, side=side)

    def add_label(self, label_text: str, parent="", side=tk.TOP, padx=0, pady=0):
        tk.Label(self.__define_master(parent), text=label_text).pack(side=side, padx=padx, pady=pady)

    def __define_master(self, parent: str):
        match parent:
            case "object":
                return self.__object_frame
            case "zoom":
                return self.__zoom_frame
            case "nav":
                return self.__nav_frame
        return self
