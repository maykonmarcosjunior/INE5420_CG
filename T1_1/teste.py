from src.Objetos.Objeto2D import Objeto2D

obj1 = Objeto2D('obj1', [(0, 1), (1, 2), (2, 3)], 'Wireframe')

print('original:', obj1)
print('centro geométrico:', obj1.geometric_center())

print('\nteste 1')
obj1.translation(1, 1)
print('transladado:', obj1)
obj1.translation(-1, -1)
print('desfeito:', obj1)

print('\nteste 2')
obj1.enlargement(2)
print('aumentado:', obj1)
obj1.enlargement(0.5)
print('desfeito:', obj1)

print('\nteste 3')
obj1.simple_rotation(0.5)
print('rotação simples:', obj1)
obj1.simple_rotation(-0.5)
print('desfeito:', obj1)


print('\nteste 4')
obj1.rotation(0.5, (1, 1))
print('rotação em torno de (1, 1):', obj1)
obj1.rotation(-0.5, (1, 1))
print('desfeito:', obj1)

print('\nteste 5')
obj1.center_rotation(0.5)
print('rotação em torno do centro geométrico:', obj1)
obj1.center_rotation(-0.5)
print('desfeito:', obj1)
