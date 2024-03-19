import tkinter as tk

# Classe para representar objetos 2D
class Object2D:
    def __init__(self, name, obj_type, coords):
        self.name = name
        self.type = obj_type
        self.coords = coords

# Classe para o Display File
class DisplayFile:
    def __init__(self, canvas_width, canvas_height):
        self.objects = []
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.viewport = [0, 0, canvas_width, canvas_height]  # left, top, right, bottom
        self.pan_x = 0
        self.pan_y = 0
        self.zoom = 1.0

    def add_object(self, obj):
        self.objects.append(obj)

    def viewport_transform(self, x, y):
        vx = self.viewport[0] + (x - self.pan_x) / self.zoom
        vy = self.viewport[3] - (y - self.pan_y) / self.zoom
        return vx, vy

    def pan(self, dx, dy):
        self.pan_x += dx
        self.pan_y += dy

    def zoom_in(self, factor=1.25):
        self.zoom *= factor

    def zoom_out(self, factor=0.8):
        self.zoom *= factor

    def draw(self, canvas):
        canvas.delete("all")
        for obj in self.objects:
            coords = []
            for x, y in obj.coords:
                vx, vy = self.viewport_transform(x, y)
                coords.append(vx)
                coords.append(vy)
            if obj.type == "point":
                canvas.create_oval(coords[0] - 2, coords[1] - 2, coords[0] + 2, coords[1] + 2, fill="black")
            elif obj.type == "line":
                canvas.create_line(coords, fill="black")
            elif obj.type == "wireframe":
                canvas.create_line(coords, coords[0], coords[1], fill="black")

# Função para criar objetos a partir de entrada do usuário
def create_object():
    name = input("Digite o nome do objeto: ")
    obj_type = input("Digite o tipo de objeto (point, line ou wireframe): ")
    coords = []
    while True:
        coord = input("Digite as coordenadas x, y (ou 'fim' para encerrar): ")
        if coord.lower() == "fim":
            break
        x, y = map(float, coord.split(","))
        coords.append((x, y))
    obj = Object2D(name, obj_type, coords)
    display_file.add_object(obj)
    draw_canvas()

# Função para desenhar a tela
def draw_canvas():
    display_file.draw(canvas)

# Função para lidar com eventos de zoom
def zoom(event):
    if event.delta > 0:
        display_file.zoom_in()
    else:
        display_file.zoom_out()
    draw_canvas()

# Função para lidar com eventos de pan
def pan(event):
    dx = event.x - display_file.canvas_width / 2
    dy = event.y - display_file.canvas_height / 2
    display_file.pan(dx, dy)
    draw_canvas()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Computação Gráfica 2D")

canvas_width = 600
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Criação do Display File
display_file = DisplayFile(canvas_width, canvas_height)

# Vinculação de eventos
canvas.bind("<MouseWheel>", zoom)
canvas.bind("<B1-Motion>", pan)

# Loop principal
create_object()
while True:
    action = input("Digite 'criar' para adicionar um novo objeto, ou 'sair' para encerrar: ")
    if action.lower() == "criar":
        create_object()
    elif action.lower() == "sair":
        break
    elif action.lower() == "zoom in":
        display_file.zoom_in()
        draw_canvas()

root.mainloop()
