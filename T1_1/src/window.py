import tkinter as tk
import ast  # Importar o módulo ast para avaliar a string como expressão Python
# from src.ViewPort import ViewPort as VP
from src.WindowUtils import ObjectListFrame, DrawWindow
import src.ViewPort as VP


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

        # Frame separator
        separator = tk.Frame(self.__root, relief="sunken", width=4, bd=10)
        separator.pack(fill="y", expand=True)

    def __create_viewport_frame(self):
        self.__viewport_frame = tk.Frame(self.__root)
        self.__viewport_frame.pack(side="right", fill=tk.BOTH, padx=(0, 20))

        # Title: Viewport
        text_frame = tk.Label(
            self.__viewport_frame, text="Viewport", font="System 12 bold", pady=5
        )
        text_frame.pack()

        # Canvas
        self.__viewport = VP.ViewPort(self.__viewport_frame)
        self.__viewport.pack()

    def __create_options_frame(self):
        self.__options_frame = tk.Frame(self.__root)
        self.__options_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(15, 0))

        # Title: Function Menu
        text_frame = tk.Label(
            self.__options_frame, text="Function Menu", font="System 12 bold", pady=5
        )
        text_frame.pack(fill=tk.X, padx=(5, 0))

        # Button: Draw Object
        self.__add_object_button = tk.Button(
            self.__options_frame, text="Draw Object", command=self.get_object
        )
        self.__add_object_button.pack(pady=20)

        # Title and List of objects on the DisplayFile
        # TODO: Fazer a listbox mudar quando um objeto for inserido
        text_objects = tk.Label(self.__options_frame, text="Object List")
        text_objects.pack(fill=tk.X)

        self.__object_list_frame = ObjectListFrame(master=self.__options_frame)
        self.__object_list_frame.pack(fill=tk.X)

        # Zoom buttons
        left_space = 400

        zoom_out_button = tk.Button(
            self.__options_frame, text="-", command=self.__viewport.zoom_out
        )
        zoom_out_button.pack(side=tk.LEFT, pady=(10, left_space))

        zoom_text = tk.Label(self.__options_frame, text="Zoom")
        zoom_text.pack(side=tk.LEFT, padx=30, pady=(10, left_space))

        zoom_in_button = tk.Button(
            self.__options_frame, text="+", command=self.__viewport.zoom_in
        )
        zoom_in_button.pack(side=tk.LEFT, pady=(10, left_space))

    def draw(self, objects: list[VP.Obj2D.Objeto2D]):
        self.__viewport.delete("all")
        for obj in objects:
            coords = []
            print(obj.coordinates)
            for x, y in obj.coordinates:
                vx, vy = self.__viewport.viewport_transform(x, y)
                coords.append(vx)
                coords.append(vy)
            if len(obj.coordinates) == 1:
                self.__viewport.create_oval(
                    coords[0] - 2,
                    coords[1] - 2,
                    coords[0] + 2,
                    coords[1] + 2,
                    fill="black",
                )
            elif len(obj.coordinates) == 2:
                self.__viewport.create_line(coords, fill="black")
            else:
                self.__viewport.create_line(coords, coords[0], coords[1], fill="black")

    def get_object(self) -> list[tuple[float]]:
        try:
            # name, coords = input("digite o objeto: nome - coordenadas\n").split(" - ")
            name, coords = self.__open_draw_window()
            f_coords = self.__string_to_float_tuple_list(coords)
            if len(f_coords) == 1:
                output = VP.P2D.Ponto2D(name, f_coords)
            elif len(f_coords) == 2:
                output = VP.L2D.Linha2D(name, f_coords)
            else:
                output = VP.WF.WireFrame(name, f_coords)
            return output
        except Exception as e:
            print("Error in get_object: ", e)

    def __string_to_float_tuple_list(self, string):
        # Remover parênteses externos e dividir a string em substrings de tuplas
        tuples = string.strip('()').split('), (')

        # Converter cada substring em uma tupla de floats
        tuple_list = []
        for t in tuples:
            tuple_list.append(ast.literal_eval("(" + t + ")"))

        return tuple_list

    def is_active(self):
        return self.__is_active

    def __open_draw_window(self):
        draw_window = DrawWindow(self.__root)
        return draw_window.get_object()
        