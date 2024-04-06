import tkinter as tk


class ViewPort:
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):

        self.__canvas = tk.Canvas(master, width=width_ + 20, height=height_ + 20, bg=bg_)

        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))

        self.__canvas.pack()

        self.__width = width_
        self.__height = height_
        
        self.draw_outer_frame()

    def delete(self, object_name="all") -> None:
        self.__canvas.delete(object_name)

    def draw_outer_frame(self) -> None:
        self.__canvas.create_rectangle(10, 10, self.__width + 10, self.__height + 10, outline="red")

    def draw_oval(self, x0: float, y0: float, x1: float, y1: float, color: str) -> None:
        self.__canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)

    def draw_line(self, x0: float, y0: float, x1: float, y1: float, color: str, width: float) -> None:
        self.__canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def viewport_transform(self, x: float, y: float) -> list[float]:
        vx = (x + 1) / (2) * self.__width + 10
        vy = (1 - (y + 1) / (2)) * self.__height + 10

        return [vx, vy]
