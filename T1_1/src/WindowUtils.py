import tkinter as tk
from src.Objetos import Objeto2D as Obj2D


class ObjectListFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__current_index = 0
        var = tk.Variable(value=[])

        self.__listbox = tk.Listbox(self, listvariable=var, height=6, selectmode=tk.EXTENDED)

        self.__listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.__listbox.yview)

        self.__listbox["yscrollcommand"] = scrollbar.set

        scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        
    def add_new_object(self, new_object: Obj2D.Objeto2D):
        self.__listbox.insert(self.__get_index(), new_object.name)
        
    def __get_index(self) -> int:
        self.__current_index += 1
        return self.__current_index
        


class DrawWindow(tk.Toplevel):
    def __init__(self, master=None, height=300, width=400):
        super().__init__(master)
        self.__coordinates_str = None  # Value to be returned
        self.__name_str = None

        self.title("Draw Options")
        self.geometry(f"{width}x{height}")

        tk.Label(self, text="Name:").pack(pady=(10, 0))
        self.__object_name = tk.Entry(self)
        self.__object_name.pack(fill=tk.X, padx=20)

        # self.__object_type_var = tk.StringVar(self)
        # self.__object_type_var.set("Point")  # Default value

        # self.__options_list = ["Point", "Line", "Polygon"]
        # tk.Label(self, text="Choose object type:").pack()
        # tk.OptionMenu(self, self.__object_type_var, *self.__options_list).pack()

        tk.Label(
            self, text='Enter Coordinates (in the format "(x1, y1),(x2, y2),..."):'
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
