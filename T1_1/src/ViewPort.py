import tkinter as tk


class ViewPort:
    def __init__(self, master=None, width_=600, height_=400, bg_="white"):
        self.__border_size = 10

        self.__canvas = tk.Canvas(master, width=width_ + 2 * self.__border_size, height=height_ + 2 * self.__border_size, bg=bg_)

        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))

        self.__canvas.pack()

        self.__width = width_
        self.__height = height_
        
        self.draw_outer_frame()

    def delete(self, object_name="all") -> None:
        self.__canvas.delete(object_name)

    def draw_outer_frame(self) -> None:
        self.__canvas.create_rectangle(self.__border_size, self.__border_size, self.__width + self.__border_size, self.__height + self.__border_size, outline="red")

    def draw_oval(self, x: float, y: float, color: str, width) -> None:
        xc, yc = self.viewport_transform(x, y)
        x0, y0 = xc - width, yc - width
        x1, y1 = xc + width, yc + width
        self.__canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)

    def draw_line(self, p0:(float), p1:(float), color: str, width: float) -> None:
        x0, y0 = self.viewport_transform(*p0)
        x1, y1 = self.viewport_transform(*p1)
        self.__canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def draw_polygon(self, points: list[tuple[float]], color: str, width:float, fill = False) -> None:
        points = [self.viewport_transform(*point) for point in points]
        bg = color if fill else ""
        self.__canvas.create_polygon(points, fill=bg, outline=color, width=width)
    
    def viewport_transform(self, x: float, y: float) -> list[float]:
        vx = (x + 1) / 2 * self.__width + self.__border_size
        vy = (1 - (y + 1) / 2) * self.__height + self.__border_size
        return [vx, vy]
