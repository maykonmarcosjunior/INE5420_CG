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
surface1
(100, 100, 700),(500, 100, 700),(100, 500, 700),(1000, 1000, 700);(150, 100, 700),(550, 100, 700),(150, 500, 700),(1050, 1000, 700);(200, 100, 700),(600, 100, 700),(200, 500, 700),(1100, 1000, 700);(250, 100, 700),(650, 100, 700),(250, 500, 700),(1150, 1000, 700)
surface2
(300, 100, 700),(700, 100, 700),(300, 500, 700),(1200, 1000, 700);(350, 100, 700),(750, 100, 700),(350, 500, 700),(1250, 1000, 700);(400, 100, 700),(800, 100, 700),(400, 500, 700),(1300, 1000, 700);(450, 100, 700),(850, 100, 700),(450, 500, 700),(1350, 1000, 700)
surface3
(500, 100, 700),(900, 100, 700),(500, 500, 700),(1400, 1000, 700);(550, 100, 700),(950, 100, 700),(550, 500, 700),(1450, 1000, 700);(600, 100, 700),(1000, 100, 700),(600, 500, 700),(1500, 1000, 700);(650, 100, 700),(1050, 100, 700),(650, 500, 700),(1550, 1000, 700)
surface4
(700, 100, 700),(1100, 100, 700),(700, 500, 700),(1600, 1000, 700);(750, 100, 700),(1150, 100, 700),(750, 500, 700),(1650, 1000, 700);(800, 100, 700),(1200, 100, 700),(800, 500, 700),(1700, 1000, 700);(850, 100, 700),(1250, 100, 700),(850, 500, 700),(1750, 1000, 700)
superficie1
(100, 100, 700),(500, 100, 700),(100, 500, 700),(1000, 1000, 700);(150, 100, 700),(550, 100, 700),(150, 500, 700),(1050, 1000, 700);(200, 100, 700),(600, 100, 700),(200, 500, 700),(1100, 1000, 700);(250, 100, 700),(650, 100, 700),(250, 500, 700),(1150, 1000, 700);(200, 100, 700),(600, 100, 700),(200, 500, 700),(1100, 1000, 700);(250, 100, 700),(650, 100, 700),(250, 500, 700),(1150, 1000, 700);(300, 100, 700),(700, 100, 700),(300, 500, 700),(1200, 1000, 700);(350, 100, 700),(750, 100, 700),(350, 500, 700),(1250, 1000, 700);(200, 100, 700),(600, 100, 700),(200, 500, 700),(1100, 1000, 700);(250, 100, 700),(650, 100, 700),(250, 500, 700),(1150, 1000, 700);(400, 100, 700),(800, 100, 700),(400, 500, 700),(1300, 1000, 700);(450, 100, 700),(850, 100, 700),(450, 500, 700),(1350, 1000, 700);(400, 100, 700),(800, 100, 700),(400, 500, 700),(1300, 1000, 700);(450, 100, 700),(850, 100, 700),(450, 500, 700),(1350, 1000, 700);(500, 100, 700),(1100, 100, 700),(500, 500, 700),(1400, 1000, 700);(550, 100, 700),(950, 100, 700),(550, 500, 700),(1450, 1000, 700)
superficie2
(0, 0, 650),(0, 0, 750),(0, 0, 850),(0, 0, 950);(100, 100, 650),(100, 100, 750),(100, 100, 850),(100, 100, 950);(300, 0, 650),(300, 0, 750),(300, 0, 850),(300, 0, 950);(150, -100, 650),(150, -100, 750),(150, -100, 850),(150, -100, 950)
superficie3
(0, 0, 650),(0, 100, 650),(0, 200, 650),(0, 300, 650);(100, 0, 650),(100, 100, 750),(100, 200, 750),(100, 300, 650);(200, 0, 650),(200, 100, 750),(200, 200, 750),(200, 300, 650);(300, 0, 650),(300, 100, 650),(300, 200, 650),(300, 300, 650)
superficie4
(-100, 300, 700),(0, 300, 700),(100, 300, 700),(200, 300, 700);(-100, 300, 800),(0, -200, 800),(100, -200, 800),(200, 300, 800);(-100, 300, 900),(0, -200, 900),(100, -200, 900),(200, 300, 900);(-100, 300, 1000),(0, 300, 1000),(100, 300, 1000),(200, 300, 1000)
'''

from src.Objetos.Objeto3D import Objeto3D, ObjectType

print(list(ObjectType.__members__.values()))
print(list(ObjectType.__members__))
print([i.name for i in list(ObjectType.__members__.values())])
