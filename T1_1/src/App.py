import src.DisplayFile as DF
import src.WindowUtils as W_U
import src.Window as WW
from src.Objetos import Objeto2D as Obj2D, Ponto2D as P2D, Linha2D as L2D, WireFrame as WF
from src.OBJFileUtils import OBJParser as OBJP, OBJGenerator as OBJG

import tkinter as tk
from tkinter import messagebox
import ast  # Importar o módulo ast para avaliar a string como expressão Python


class App:
    def __init__(self, title="Window", width=960, height=720):
        self.__root = tk.Tk()

        self.__left_frame = tk.Frame(self.__root)
        self.__left_frame.pack(side=tk.LEFT, padx=(80, 0), fill=tk.X)

        self.__display_file = DF.DisplayFile(self.__left_frame, self.__apply_transformations)
        self.__root.title(title)
        self.__root.geometry(f"{width}x{height}")
        self.__root.resizable(False, False)

        self.__window = WW.Window(self.__root, 740, 740)

        self.__options_frame = None

        self.__create_options_frame()

        self.__world_width = 1000
        self.__world_height = 1000

        # Frame separator
        tk.Frame(self.__root, relief="sunken", width=4, bd=10).pack(
            fill=tk.Y, expand=True
        )
        self.__root.mainloop()

    def __create_options_frame(self):
        self.__options_frame = W_U.OptionsFrame(self.__left_frame)
        self.__options_frame.pack(fill=tk.BOTH)

        self.__options_frame.add_button(button_text="Draw Object", function=self.__get_object, parent="object", pady=10)
        self.__options_frame.add_label(label_text="Import/export .obj files", parent="object", bold=True, pady=(10, 0))
        self.__options_frame.add_button(button_text="Import .obj file", parent="object", function=self.__parse_obj)
        self.__options_frame.add_button(button_text="Export .obj file", parent="object", function=self.__generate_obj)

        # Window Zoom
        self.__options_frame.add_button(button_text="-", function=lambda: self.__zoom_window("out"), parent="zoom", side=tk.LEFT, pady=10)
        self.__options_frame.add_label(label_text="Zoom", parent="zoom", side=tk.LEFT, padx=30, pady=10, bold=True)
        self.__options_frame.add_button(button_text="+", function=lambda: self.__zoom_window("in"), parent="zoom", side=tk.LEFT, pady=10)

        # Window Navigation
        self.__options_frame.add_label(label_text="Navigation", parent="nav", bold=True)

        self.__options_frame.add_button(button_text="Up", function=lambda: self.__pan_window("y", 10), parent="nav", side=tk.LEFT)
        self.__options_frame.add_button(button_text="Down", function=lambda: self.__pan_window("y", -10), parent="nav", side=tk.LEFT)
        self.__options_frame.add_button(button_text="Right", function=lambda: self.__pan_window("x", 10), parent="nav", side=tk.LEFT)
        self.__options_frame.add_button(button_text="Left", function=lambda: self.__pan_window("x", -10), parent="nav",side=tk.LEFT)

        # Window Rotation
        self.__options_frame.add_label(label_text="Rotate Window", parent="rotation", bold=True)
        self.__options_frame.add_label(label_text="Angle (in degrees):", parent="rotation")
        self.__options_frame.add_entry(parent="rotation", var_name="angle")
        self.__options_frame.add_button(button_text="Rotate", function=self.__rotate_window, parent="rotation")
        
        # Clipping
        self.__options_frame.add_label(label_text="Change Clipping Method", parent="clipping", bold=True)
        self.__options_frame.add_button(button_text="Cohen Sutherland", function=lambda: self.__set_clipping_algorithm("C-S"), parent="clipping")
        self.__options_frame.add_button(button_text="Liang Barsky", function=lambda: self.__set_clipping_algorithm("L-B"), parent="clipping")
        

    def __get_object(self) -> list[tuple[float]]:
        try:
            name, coords, color = self.__open_draw_window()
            if name is None or coords is None or not name.strip() or not coords.strip():
                messagebox.showinfo("Information", "The object was not created. Name and coordinates are required.")
                return
            f_coords = self.__string_to_float_tuple_list(coords)
            output = self.__create_object(name, f_coords, color)
            self.__update_display_file(output)
            return output

        except Exception as e:
            messagebox.showinfo("Input Error", "Invalid input. Please try again.")
            print("Error in get_object: ", e)

    def __create_object(self, name, coords, color) -> Obj2D:
        if len(coords) == 1:
            output = P2D.Ponto2D(name, coords, color=color)
        elif len(coords) == 2:
            output = L2D.Linha2D(name, coords, color=color)
        else:
            output = WF.WireFrame(name, coords, color=color)

        return output

    def __string_to_float_tuple_list(self, string):
        # Remover parênteses externos e dividir a string em substrings de tuplas
        tuples = string.strip("()").split("),(")
        # Converter cada substring em uma tupla de floats
        tuple_list = []
        for t in tuples:
            tuple_list.append(ast.literal_eval("(" + t + ")"))

        return tuple_list

    def __open_draw_window(self):
        self.__draw_window = W_U.DrawWindow(self.__root)
        name, coords, color = self.__draw_window.show_window()
        return name, coords, color

    def __draw_all_objects(self):
        self.__window.delete("all")
        self.__window.draw_viewport_outer_frame()
        
        for obj in self.__display_file.objects:
            self.__window.draw_object(obj)
            
    def __apply_transformations(self, object_index: int, transformations: list):
        obj = self.__display_file.objects[object_index]
        obj.apply_transformations(transformations=transformations)
        self.__draw_all_objects()

    def __update_display_file(self, new_object: Obj2D.Objeto2D):
        self.__display_file.add_object(new_object)
        self.__draw_all_objects()

    def __pan_window(self, axis: str, amount: int):
        if axis == 'x':
            self.__window.pan_x(amount)
        elif axis == 'y':
            self.__window.pan_y(amount)
        self.__window.set_normalization_matrix()
        self.__draw_all_objects()

    def __zoom_window(self, zoom_type: str):
        if zoom_type == 'in':
            self.__window.zoom_in()
        elif zoom_type == 'out':
            self.__window.zoom_out()
        self.__window.set_normalization_matrix()
        self.__draw_all_objects()

    def __rotate_window(self, var_parent="rotation", var_name="angle"):
        angle = self.__options_frame.get_var_value(parent=var_parent, var_name=var_name, var_type=float)
        if angle is None:
            messagebox.showinfo("Information", "The angle value is not of expected type (float).")
            return
        self.__window.set_normalization_matrix(angle)
        self.__draw_all_objects()

    def __parse_obj(self) -> None:
        parser = OBJP()
        objects = parser.objects

        # Convert the list of lists of 3D coordinates in a list of tuples of 2D coordinates
        for value in objects.values():
            value["coordinates"] = [(coord[0], coord[1]) for coord in value["coordinates"]]

        for name, value in objects.items():
            self.__display_file.add_object(self.__create_object(name, value["coordinates"], value["color"]))

        self.__draw_all_objects()


    def __generate_obj(self) -> None:
        OBJG(self.__display_file.objects)
        
    def __set_clipping_algorithm(self, algorithm: str="C-S") -> None:
        self.__window.set_clipping_algorithm(algorithm)
