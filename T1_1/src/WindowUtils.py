import tkinter as tk
from tkinter import colorchooser
from typing import Callable


class DrawWindow(tk.Toplevel):
    def __init__(self, master=None, height=400, width=600):
        super().__init__(master)
        self.__coordinates_str = None  # Value to be returned
        self.__name_str = None
        self.__color = "#000000"

        self.title("Draw Options")
        self.geometry(f"{width}x{height}")

        tk.Label(self, text="Name:").pack(pady=(10, 0))
        self.__object_name = tk.Entry(self)
        self.__object_name.pack(fill=tk.X, padx=20)

        tk.Label(
            self, text='Enter Coordinates (in the format "(x1, y1),(x2, y2),..."):'
        ).pack(pady=(10, 0))
        self.__coord_entry = tk.Entry(self)
        self.__coord_entry.pack(fill=tk.X, padx=20)

        tk.Button(self, text="Choose Color", command=self.__choose_color).pack(pady=(20, 0))

        tk.Label(self, text="Selected Color:").pack(pady=10)
        self.__selected_color_label = tk.Label(self, bg=self.__color, width=5, height=1)
        self.__selected_color_label.pack()

        tk.Button(self, text="Submit", command=self.__submit_option).pack(pady=(20, 0))

    def show_window(self) -> tuple[str, str, str]:
        self.wait_window()
        return self.get_informations()

    def __submit_option(self) -> None:
        self.__coordinates_str = self.__coord_entry.get()
        self.__name_str = self.__object_name.get()
        self.destroy()

    def get_informations(self) -> tuple[str, str, str]:
        return self.__name_str, self.__coordinates_str, self.__color

    def __choose_color(self) -> None:
        color = colorchooser.askcolor("#000000", title="Choose color")[1]
        if color:
            self.__selected_color_label.config(bg=color)
            self.__color = color


class OptionsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        tk.Label(self, text="Function Menu", font="System 12 bold").pack(
            fill=tk.X, pady=(20, 0)
        )
        
        self.__default_font = "TkDefaultFont 10"

        self.__object_frame = tk.Frame(self)
        self.__object_frame.pack(pady=10)

        self.__zoom_frame = tk.Frame(self)
        self.__zoom_frame.pack(pady=10)

        self.__nav_frame = tk.Frame(self)
        self.__nav_frame.pack(pady=10)

        self.__rotation_frame = tk.Frame(self)
        self.__rotation_frame.pack(pady=10)
        
        self.__clipping_frame = tk.Frame(self)
        self.__clipping_frame.pack(pady=10)

    def add_button(self, button_text: str, function: Callable, parent="object", side=tk.TOP, padx=0, pady=0) -> None:
        tk.Button(self.__define_master(parent), text=button_text, command=function).pack(pady=pady, padx=padx, side=side)

    def add_label(self, label_text: str, parent="object", side=tk.TOP, padx=0, pady=0, bold=False) -> None:
        font = self.__default_font if not bold else "TkDefaultFont 10 bold"
        tk.Label(self.__define_master(parent), text=label_text, font=font).pack(side=side, padx=padx, pady=pady)

    def add_entry(self, parent="object", side=tk.TOP, padx=0, pady=0, var_name="Variable") -> None:
        master = self.__define_master(parent)
        var = tk.StringVar(master=master, name=var_name)
        tk.Entry(master=master, textvariable=var).pack(side=side, padx=padx, pady=pady)

    def get_var_value(self, parent="object", var_name="Variable", var_type: callable=None):
        str_value = self.__define_master(parent).getvar(var_name)
        try:
            value = var_type(str_value)
            return value
        except ValueError:
            return None

    def __define_master(self, parent: str) -> tk.Frame:
        match parent:
            case "object":
                return self.__object_frame
            case "zoom":
                return self.__zoom_frame
            case "nav":
                return self.__nav_frame
            case "rotation":
                return self.__rotation_frame
            case "clipping":
                return self.__clipping_frame
        return self
