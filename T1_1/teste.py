'''
obj1
(100, 100),(500, 100),(500, 500)
obj2D
(90, 90),(510, 90),(510, 510),(90, 510)
curve1
(100, 100, 700),(500, 100, 700),(500, 500, 700),(100, 500, 700),(1000, 1000, 700)
obj3Da
(90, 90, 100),(510, 90, 100),(510, 510, 100),(90, 510, 100),(90, 90, 100),(90, 90, 1420),(510, 90, 1420),(510, 90, 100),(510, 90, 1420),(510, 510, 1420),(510, 510, 100),(510, 510, 1420),(90, 510, 1420),(90, 510, 100),(90, 510, 1420),(90, 90, 1420)
obj3Db
(-100, -100, 700),(100, -100, 700),(100, 100, 700),(-100, 100, 700),(-100, -100, 700),(-100, -100, 2000),(100, -100, 2000),(100, -100, 700),(100, -100, 2000),(100, 100, 2000),(100, 100, 700),(100, 100, 2000),(-100, 100, 2000),(-100, 100, 700),(-100, 100, 2000),(-100, -100, 2000)
bicurve1
(100, 100, 700),(500, 100, 700),(100, 500, 700),(1000, 1000, 700);(150, 100, 700),(550, 100, 700),(150, 500, 700),(1050, 1000, 700);(200, 100, 700),(600, 100, 700),(200, 500, 700),(1100, 1000, 700);(250, 100, 700),(650, 100, 700),(250, 500, 700),(1150, 1000, 700)
bicurve2
(300, 100, 700),(700, 100, 700),(300, 500, 700),(1200, 1000, 700);(350, 100, 700),(750, 100, 700),(350, 500, 700),(1250, 1000, 700);(400, 100, 700),(800, 100, 700),(400, 500, 700),(1300, 1000, 700);(450, 100, 700),(850, 100, 700),(450, 500, 700),(1350, 1000, 700)
bicurve3
(500, 100, 700),(900, 100, 700),(500, 500, 700),(1400, 1000, 700);(550, 100, 700),(950, 100, 700),(550, 500, 700),(1450, 1000, 700);(600, 100, 700),(1000, 100, 700),(600, 500, 700),(1500, 1000, 700);(650, 100, 700),(1050, 100, 700),(650, 500, 700),(1550, 1000, 700)
'''

from src.Objetos.Objeto3D import Objeto3D, ObjectType

print(list(ObjectType.__members__.values()))
print(list(ObjectType.__members__))
print([i.name for i in list(ObjectType.__members__.values())])
