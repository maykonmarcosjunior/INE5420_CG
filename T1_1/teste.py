from src.Objetos.Objeto2D import Objeto2D

'''
obj1
(100, 100),(500, 100),(500, 500)
'''

obj1 = Objeto2D('obj1', [(0, 1), (1, 2), (2, 3)], 'Wireframe')

print('original:', obj1)
print('centro geométrico:', obj1.geometric_center())

print('\nteste 1')
obj1.translation(1, 1)
print('transladado:', obj1)
obj1.translation(-1, -1)
print('desfeito:', obj1)

print('\nteste 2')
obj1.scaling(2, 2)
print('aumentado:', obj1)
obj1.scaling(0.5, 0.5)
print('desfeito:', obj1)

print('\nteste 3')
obj1.rotation("RotationType.world_center", 30)
print('rotação simples:', obj1)
obj1.rotation("RotationType.world_center", -30)
print('desfeito:', obj1)


print('\nteste 4')
obj1.rotation("RotationType.any_point", 30, 1.0, 1.0)
print('rotação em torno de (1, 1):', obj1)
obj1.rotation("RotationType.any_point", -30, 1.0, 1.0)
print('desfeito:', obj1)

print('\nteste 5')
obj1.rotation("RotationType.object_center", 30)
print('rotação em torno do centro geométrico:', obj1)
obj1.rotation("RotationType.object_center", -30)
print('desfeito:', obj1)
