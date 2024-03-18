import tkinter as tk
import logging


class ObjectListFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        var = tk.Variable(value=[])

        listbox = tk.Listbox(self, listvariable=var, height=6, selectmode=tk.EXTENDED)

        listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=listbox.yview)

        listbox["yscrollcommand"] = scrollbar.set

        scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)


class LogDisplay(tk.Frame):
    class Handler(logging.Handler):
        def __init__(self, master):
            logging.Handler.__init__(self)
            self.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
            self.widget = master
            self.widget.config(state="disabled")

        def emit(self, record):
            self.widget.config(state="normal")
            self.widget.insert(tk.END, self.format(record) + "\n")
            self.widget.see(tk.END)
            self.widget.config(state="disabled")

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E))

        self.text = tk.Text(self, yscrollcommand=self.scrollbar.set)
        self.text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.scrollbar.config(command=self.text.yview)

        self.logging_handler = LogDisplay.Handler(self.text)


class DrawWindow(tk.Toplevel):
    def __init__(self, master=None, height=300, width=400, values_list=[]):
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

        submit_button = tk.Button(self, text="Submit", command=self.__submit_option)
        submit_button.pack()

        self.__current_coordinate_elements = {}

        self.__values_list = values_list

    def __submit_option(
        self,
    ):  # TODO: Não há necessidade de escreer a label enter coordinates toda vez
        choosed_type = self.__object_type_var.get()

        self.__delete_current_coordinate_options()

        label_coordinates = tk.Label(self, text="Enter Coordinates:")
        label_coordinates.pack()
        self.__current_coordinate_elements["standard"] = label_coordinates

        match choosed_type:
            case "Point":
                self.__add_labels_and_coordinates(["x", "y"])
            case "Line":
                self.__add_labels_and_coordinates(["x1", "y1", "x2", "y2"])
            case "Polygon":
                self.__polygon_coordinates()

    def __point_coordinates(self):
        label_x = tk.Label(self, text="x:")
        label_x.pack()

        x_entry = tk.Entry(self)
        x_entry.pack()

        label_y = tk.Label(self, text="y:")
        label_y.pack()

        y_entry = tk.Entry(self)
        y_entry.pack()

        self.__current_coordinate_elements.append(label_x)
        self.__current_coordinate_elements.append(x_entry)

        self.__current_coordinate_elements.append(label_y)
        self.__current_coordinate_elements.append(y_entry)

        self.__draw_object_button = tk.Button(
            self, text="Draw Object", command=self.__return_values_and_close_window
        )

    def __line_coordinates(self):
        coordinate_labels = ["x1", "y1", "x2", "y2"]

        for coord_label in coordinate_labels:
            label = tk.Label(self, text=f"{coord_label}:")
            label.pack()
            self.__current_coordinate_elements.append(label)

    def __polygon_coordinates(self):
        pass
    
    def __add_labels_and_coordinates(self, labels_list: list[str]):
        self.coordinate_entries = {}

        for coord in labels_list:
            label = tk.Label(self, text=f"{coord}:")
            label.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.__current_coordinate_elements.append(label)
            self.__current_coordinate_elements.append(entry)
            self.coordinate_entries[coord] = entry

    def __delete_current_coordinate_options(self):
        for item in self.__current_coordinate_elements:
            item.destroy()

    def __return_values_and_close_window(self):
        # https://discuss.python.org/t/returning-a-value-from-a-tkinter-popup/14996/2
        for entry in self.__current_coordinate_elements.values():
            self.__values_list.append(entry.get())
        self.destroy()
