import tkinter as tk
from src.Objetos import Objeto2D as Obj2D

class DisplayFile:
    def __init__(self, root):
        self.__objects = []
        self.__frame = DisplayFileFrame(root)
        self.__frame.pack(fill=tk.X)

    def add_object(self, new_object:Obj2D.Objeto2D):
        if new_object not in self.__objects and isinstance(new_object, Obj2D.Objeto2D):
            self.__objects.append(new_object)
            self.__frame.add_new_object(new_object)

    def remove_object(self, object:Obj2D.Objeto2D):
        if object in self.__objects:
            self.__objects.remove(object)
       
    @property     
    def objects(self) -> list[Obj2D.Objeto2D]:
        return self.__objects


class DisplayFileFrame(tk.Frame):
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
        
    def __get_index(self) -> int: # TODO: ajeitar
        self.__current_index += 1
        return self.__current_index
