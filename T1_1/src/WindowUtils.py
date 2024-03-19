import tkinter as tk


class ObjectListFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        var = tk.Variable(value=[])

        listbox = tk.Listbox(self, listvariable=var, height=6, selectmode=tk.EXTENDED)

        listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=listbox.yview)

        listbox["yscrollcommand"] = scrollbar.set

        scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)


class DrawWindow(tk.Toplevel):
    def __init__(self, master=None, height=300, width=400):
        super().__init__(master)
        self.title("Draw Options")
        self.geometry(f"{width}x{height}")

        tk.Label(self, text="Name:").pack(pady=(10, 0))
        self.__object_name = tk.Entry(self)
        self.__object_name.pack(fill=tk.X, padx=20)

        self.__object_type_var = tk.StringVar(self)
        self.__object_type_var.set("Point")  # Default value

        self.__options_list = ["Point", "Line", "Polygon"]
        tk.Label(self, text="Choose object type:").pack()
        tk.OptionMenu(self, self.__object_type_var, *self.__options_list).pack()

        tk.Label(self, text='Enter Coordinates (in the format "(x1, y1),(x2, y2),..."):').pack()
        self.__coord_entry = tk.Entry(self)
        self.__coord_entry.pack(fill=tk.X, padx=20)
        
        submit_button = tk.Button(self, text="Submit", command=self.__get_object)
        submit_button.pack()

    def __get_object(self):
        return self.__coord_entry.get()
    
    def __submit_option(self): 
        choosed_type = self.__object_type_var.get()
        
        points_str = self.__coord_entry.get().strip().split(",")
        points = [tuple(map(float, s.strip("()").split(", "))) for s in points_str]
        
        match choosed_type:
            case "Point":
                if len(points) != 1: # TODO
                    return
            case "Line":
                if len(points) != 2:
                    return
            case "Polygon":
                if len(points) < 3:
                    return
                
        self.__object_to_be_drawn[choosed_type] = points
