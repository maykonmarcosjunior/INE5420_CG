import tkinter as tk
from src.ViewPort import ViewPort as VP

class Window:
    def __init__(self, title="Window", width=960, height=720):
        self.__is_active = True

        self.__root = tk.Tk()
        
        self.__root.title(title)
        self.__root.geometry(f"{width}x{height}")
        self.__root.resizable(False, False)
        
        self.__viewport = None
        
        self.__viewport_frame = None
        self.__options_frame = None
        
        self.__create_viewport_frame()
        self.__create_options_frame()
        
        self.__root.mainloop()

    def __create_viewport_frame(self):
        self.__viewport_frame = tk.Frame(self.__root)
        self.__viewport_frame.pack(side="right")
        
        text_frame = tk.Label(self.__viewport_frame, text="Viewport")
        text_frame.pack()
        
        self.__viewport = VP(self.__viewport_frame)
        self.__viewport.pack()
        
        # TODO: Create the log display (under the viewport)
        
    def __create_options_frame(self):
        self.__options_frame = tk.Frame(self.__root)
        self.__options_frame.pack(side="left")
        
        # Mostrar:
        # - Setas para dar zoom
        
        # Button to add an object
        self.__add_object_button = tk.Button(self.__options_frame, text="Draw Object", command=self.__open_draw_window)
        self.__add_object_button.pack()
        
        # List of objects on the DisplayFile
        # TODO: Fazer a listbox mudar quando um objeto for inserido
        object_list_var = tk.Variables(value=[])
        
        self.__objects_listbox = tk.ListBox(self.__options_frame, listvariable=object_list_var, height=10)
        self.__objects_listbox.pack()
        objects_scrollbar = tk.Scrollbar(self.__options_frame, orient=tk.VERTICAL, command=self.__objects_listbox.yview)
        
        self.__objects_listbox["yscrollcommand"] = objects_scrollbar.set
        objects_scrollbar.pack() # talvez precisa ajustar o lado, se va expandir
        
        # Zoom buttons
        zoom_text = tk.Label(self.__options_frame, text="Zoom")
        zoom_text.pack()
        
        zoom_out_button = tk.Button(self.__options_frame, text="-", command=self.__viewport.zoom_out())
        zoom_out_button.pack(side=tk.LEFT)
        
        zoom_in_button = tk.Button(self.__options_frame, text="+", command=self.__viewport.zoom_in())
        zoom_in_button.pack(side=tk.RIGHT)
        

    def draw(self, objects: list):
        self.__viewport.delete("all")
        for obj in objects:
            coords = []
            for x, y in obj.coords:
                vx, vy = self.__viewport.viewport_transform(x, y)
                coords.append(vx)
                coords.append(vy)
            if obj.type == "point":
                self.__viewport.create_oval(coords[0] - 2, coords[1] - 2, coords[0] + 2, coords[1] + 2, fill="black")
            elif obj.type == "line":
                self.__viewport.create_line(coords, fill="black")
            elif obj.type == "wireframe":
                self.__viewport.create_line(coords, coords[0], coords[1], fill="black")

    def get_object(self):
        pass

    def is_active(self):
        return self.__is_active

