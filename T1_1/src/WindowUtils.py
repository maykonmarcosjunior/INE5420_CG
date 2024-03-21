import tkinter as tk     


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
