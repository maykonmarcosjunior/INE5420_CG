from src.Objetos.Objeto2D import Objeto2D
from src.Window import Window

'''
obj1
(100, 100),(500, 100),(500, 500)
obj2
(90, 90),(510, 90),(510, 510),(90, 510)
'''
def clip_NLN(line, window):
    def compute_outcode(x, y, window):
        xmin, xmax, ymin, ymax = window
        code = 0
        if x < xmin:
            code |= 1
        elif x > xmax:
            code |= 2
        if y < ymin:
            code |= 4
        elif y > ymax:
            code |= 8
        return code

    def clip_line(p1, p2, window):
        xmin, xmax, ymin, ymax = window
        outcode1 = compute_outcode(*p1, window)
        outcode2 = compute_outcode(*p2, window)
        accept = False

        while True:
            if not (outcode1 | outcode2):
                accept = True
                break
            elif outcode1 & outcode2:
                break
            else:
                x = None
                y = None
                outcode_out = outcode1 if outcode1 else outcode2

                if outcode_out & 1:
                    x = xmin
                    y = p1[1] + (p2[1] - p1[1]) * (xmin - p1[0]) / (p2[0] - p1[0])
                elif outcode_out & 2:
                    x = xmax
                    y = p1[1] + (p2[1] - p1[1]) * (xmax - p1[0]) / (p2[0] - p1[0])
                elif outcode_out & 4:
                    y = ymin
                    x = p1[0] + (p2[0] - p1[0]) * (ymin - p1[1]) / (p2[1] - p1[1])
                elif outcode_out & 8:
                    y = ymax
                    x = p1[0] + (p2[0] - p1[0]) * (ymax - p1[1]) / (p2[1] - p1[1])

                if outcode_out == outcode1:
                    p1 = (x, y)
                    outcode1 = compute_outcode(x, y, window)
                else:
                    p2 = (x, y)
                    outcode2 = compute_outcode(x, y, window)

        if accept:
            return [p1, p2]
        else:
            return []

    clipped_line = clip_line(line[0], line[1], window)
    return clipped_line


window = Window(None, 1, 1)
A = [(-4, 0.5), (-0.1, 2.5)]
B = [(-1.5, 0.0), (0.9, 0.4)]
C = [(-1.5, -1.0), (1.0, 0.5)]
D = [(0.4, -0.2), (2.8, 1.5)]

print("A:", A)
print(window.cohen_sutherland(A))
print(window.liang_barsky(A))
print(clip_NLN(A, (-1, 1, -1, 1)))

print("\nB:", B)
print(window.cohen_sutherland(B))
print(window.liang_barsky(B))
print(clip_NLN(B, (-1, 1, -1, 1)))

print("\nC:", C)
print(window.cohen_sutherland(C))
print(window.liang_barsky(C))
print(clip_NLN(C, (-1, 1, -1, 1)))

print("\nD:", D)
print(window.cohen_sutherland(D))
print(window.liang_barsky(D))
print(clip_NLN(D, (-1, 1, -1, 1)))
