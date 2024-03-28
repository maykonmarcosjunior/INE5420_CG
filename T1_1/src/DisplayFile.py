import tkinter as tk
from src.Objetos import Objeto2D as Obj2D
from src.TransformationUtils import TransformationsMenu


class DisplayFile:
    def __init__(self, root, transformations_function: callable):
        self.__objects = []
        self.__frame = DisplayFileFrame(root, transformations_function)
        self.__frame.pack(side=tk.TOP)

    def add_object(self, new_object: Obj2D.Objeto2D) -> None:
        if new_object not in self.__objects and isinstance(new_object, Obj2D.Objeto2D):
            self.__objects.append(new_object)
            self.__frame.add_new_object(new_object)

    def remove_object(self, obj: Obj2D.Objeto2D) -> None:
        if obj in self.__objects:
            self.__objects.remove(obj)

    @property
    def objects(self) -> list[Obj2D.Objeto2D]:
        return self.__objects

class DisplayFileFrame(tk.Frame):
    def __init__(self, master=None, transformations_function: callable=None):
        super().__init__(master)

        self.__transformations_function = transformations_function

        self.__current_index = -1
        var = tk.Variable(value=[])

        tk.Label(self, text="Object List", font="System 12 bold").pack(fill=tk.X)

        self.__listbox_frame = tk.Frame(self)
        self.__listbox = tk.Listbox(
            self.__listbox_frame, listvariable=var, height=10, selectmode=tk.EXTENDED
        )
        self.__listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = tk.Scrollbar(
            self.__listbox_frame, orient=tk.VERTICAL, command=self.__listbox.yview
        )
        self.__listbox["yscrollcommand"] = scrollbar.set
        scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        self.__listbox_frame.pack()

        self.__listbox.bind("<<ListboxSelect>>", self.__on_object_select)
        self.__transf_hidden_button = tk.Button(
            self, text="Transform Object", command=self.__show_transf_menu
        )
        self.__is_button_hidden = True

        self.__selected_item_name = None
        self.__selected_item_index = None

    def add_new_object(self, new_object: Obj2D.Objeto2D) -> None:
        self.__listbox.insert(
            self.__get_index(), f"{new_object.name} ({new_object.obj_type})"
        )

    def __get_index(self) -> int:
        self.__current_index += 1
        return self.__current_index

    def __on_object_select(self, event) -> None:
        selection_exists = bool(self.__listbox.curselection())

        if selection_exists and self.__is_button_hidden:
            self.__selected_item_index = self.__listbox.curselection()[0]
            self.__selected_item_name = self.__listbox.get(self.__selected_item_index)

            self.__transf_hidden_button.pack(pady=10)
            self.__is_button_hidden = False

        elif selection_exists:
            self.__selected_item_index = self.__listbox.curselection()[0]
            self.__selected_item_name = self.__listbox.get(self.__selected_item_index)

        elif not selection_exists and not self.__is_button_hidden:
            self.__transf_hidden_button.pack_forget()
            self.__is_button_hidden = True

    def __show_transf_menu(self) -> None:
        transf_menu = TransformationsMenu(self.__selected_item_name, master=self)
        transforms = transf_menu.show_window()
        self.__transformations_function(self.__selected_item_index, transforms)
