from src.Objetos.Objeto2D import Objeto2D
from src.Window import Window

'''
obj1
(100, 100),(500, 100),(500, 500)
obj2
(90, 90),(510, 90),(510, 510),(90, 510)
'''

window = Window(None, 1, 1)
A = [(-4, 0.5), (-0.1, 2.5)]
B = [(-1.5, 0.0), (0.9, 0.4)]
C = [(-1.5, -1.0), (1.0, 0.5)]
D = [(0.4, -0.2), (2.8, 1.5)]

print("A:", A)
print(window._Window__cohen_sutherland(A))
print(window._Window__liang_barsky(A))
print(window._Window__nicholl_lee_nicholl(A))

print("\nB:", B)
print(window._Window__cohen_sutherland(B))
print(window._Window__liang_barsky(B))
print(window._Window__nicholl_lee_nicholl(B))

print("\nC:", C)
print(window._Window__cohen_sutherland(C))
print(window._Window__liang_barsky(C))
print(window._Window__nicholl_lee_nicholl(C))

print("\nD:", D)
print(window._Window__cohen_sutherland(D))
print(window._Window__liang_barsky(D))
print(window._Window__nicholl_lee_nicholl(D))

# Exemplo de uso:
polygon = [(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]  # Polígono a ser clipado
clipped_polygon = window._Window__sutherland_hodgman(polygon)
print("\n\nPolígono clipado:", clipped_polygon)
# Output esperado: [(0.5, 1.0), (0.5, 0.5), (1.0, 0.5), (1.0, 1.0)]
