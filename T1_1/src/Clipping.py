class Clipping:
    @classmethod
    def sutherland_hodgman(cls, polygon: list[tuple[float]], world_limits: list[int]) -> list[tuple[float]]:
        # Função para verificar se um ponto 'p' está dentro de uma aresta 'edge'
        def inside(p, edge):
            # Usa o produto vetorial para determinar se o ponto está à esquerda
            # da aresta quando esta é percorrida no sentido anti-horário.
            edge_0, edge_1 = edge
            x0, y0 = edge_0
            x1, y1 = edge_1
            x, y = p
            '''
            O produto vetorial entre dois vetores 2D,
            (a, b) e (c, d) é dado pela fórmula: a * d - b * c.
            Se o resultado do produto vetorial for positivo,
            - significa que o vetor (c, d) está à esquerda do vetor (a, b).
            Se o resultado for negativo,
            - significa que o vetor (c, d) está à direita do vetor (a, b).
            Se o resultado for zero,
            - significa que os vetores são colineares.
            '''
            return (x1 - x0) * (y - y0) > (y1 - y0) * (x - x0)

        def compute_intersection(p1, p2, edge):
            # Função para calcular a interseção de uma aresta 'edge' com a linha formada por 'p1' e 'p2'
            # Usando o método de determinantes para encontrar o ponto de interseção
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = edge[0]
            x4, y4 = edge[1]

            """
            Determinante:
                O determinante de uma matriz 2x2 [a, b; c, d] é dado pela fórmula: a * d - b * c.
                O determinante é usado para verificar se duas linhas são paralelas.
                Se o determinante for zero, significa que as linhas são paralelas ou coincidentes.
            Fórmula da Interseção:
                Se as linhas não forem paralelas, é possível calcular o ponto de interseção.
                A fórmula para calcular o ponto de interseção é derivada de um sistema de equações lineares.
                O ponto de interseção é calculado usando a fórmula:
                    (x1 + t * (x2 - x1), y1 + t * (y2 - y1)),
                onde 't' é um parâmetro que determina a posição
                do ponto de interseção ao longo da linha formada por 'p1' e 'p2'.
            """

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                # As linhas são paralelas ou coincidentes
                return None
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return x, y

        # Cria uma cópia do polígono original para modificar
        clipped_polygon = polygon[:]
        
        window_points = [
                    (world_limits[0], world_limits[1]),
                    (world_limits[2], world_limits[1]),
                    (world_limits[2], world_limits[3]),
                    (world_limits[0], world_limits[3])
                  ]
        window = [(window_points[i], window_points[(i + 1) % 4]) for i in range(4)]

        for edge in window:
            new_polygon = []
            if not clipped_polygon:
                break
            prev_point = clipped_polygon[-1]

            for point in clipped_polygon:
                if inside(point, edge):
                    if not inside(prev_point, edge):
                        intersection = compute_intersection(prev_point, point, edge)
                        if intersection:
                            new_polygon.append(intersection)
                    new_polygon.append(point)
                elif inside(prev_point, edge):
                    intersection = compute_intersection(prev_point, point, edge)
                    if intersection:
                        new_polygon.append(intersection)
                prev_point = point

            clipped_polygon = new_polygon
        return clipped_polygon

    @classmethod
    def liang_barsky(cls, coords: list[tuple[float]], world_limits: list[int]) -> list[tuple[float]]:
        clipped_coords = []
        p1, p2 = coords
        Xw_min, Yw_min, Xw_max, Yw_max = world_limits
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        p = [-dx, dx, -dy, dy]
        q = [p1[0] - Xw_min, Xw_max - p1[0], p1[1] - Yw_min, Yw_max - p1[1]]
        u1 = 0
        u2 = 1
        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return []
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, u)
                else:
                    u2 = min(u2, u)
        if u1 < u2:
            clipped_coords = [(p1[0] + u1 * dx, p1[1] + u1 * dy), (p1[0] + u2 * dx, p1[1] + u2 * dy)]
        return clipped_coords
    
    @classmethod
    def __compute_outcode(self, x: float, y: float, world_limits: list[int]) -> int:
        xmin, ymin, xmax, ymax = world_limits
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
    
    @classmethod
    def cohen_sutherland(cls, coords: list[tuple[float]], world_limits: list[int]) -> list[tuple[float]]:
        p1, p2 = coords
        Xw_min, Yw_min, Xw_max, Yw_max = world_limits

        if p1[0] > p2[0]:
            p1, p2 = p2, p1

        RC1 = cls.__compute_outcode(*p1, world_limits)
        RC2 = cls.__compute_outcode(*p2, world_limits)

        RC0 = RC1 | RC2
        if RC0 == 0:
            return coords

        RC = RC1 & RC2
        if RC != 0:
            print("Line outside window")
            return []

        clipped_coords = [p1, p2]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == dy == 0:
            x, y = p1
            if Xw_min <= x <= Xw_max and Yw_min <= y <= Yw_max:
                return [(x, y)]
            else:
                return []
        elif dx == 0:
            x = p1[0]
            y1 = max((min(p1[1], Yw_max)), Yw_min)
            y2 = max((min(p2[1], Yw_max)), Yw_min)
            return [(x, y1), (x, y2)]
        elif dy == 0:
            y = p1[1]
            x1 = max((min(p1[0], Xw_max)), Xw_min)
            x2 = max((min(p2[0], Xw_max)), Xw_min)
            return [(x1, y), (x2, y)]
        m = dy / dx
        yE = m * (Xw_min - p1[0]) + p1[1]
        yD = m * (Xw_max - p1[0]) + p1[1]
        xT = (Yw_max - p1[1]) / m + p1[0]
        xF = (Yw_min - p1[1]) / m + p1[0]
        pX_min = pX_max = pY_min = pY_max = None
        if (RC0 & 1) and (Yw_min <= yE <= Yw_max):
            pX_min = (Xw_min, yE)
            clipped_coords[0] = pX_min
        elif (RC0 & 2) and (Yw_min <= yD <= Yw_max):
            pX_max = (Xw_max, yD)
            clipped_coords[1] = pX_max
        if (RC0 & 4) and (Xw_min <= xF <= Xw_max):
            pY_min = (xF, Yw_min)
            if xT > xF:
                clipped_coords[0] = pY_min
            else:
                clipped_coords[1] = pY_min
        elif (RC0 & 8) and (Xw_min <= xT <= Xw_max):
            pY_max = (xT, Yw_max)
            if xT > xF:
                clipped_coords[1] = pY_max
            else:
                clipped_coords[0] = pY_max
        if clipped_coords == [p1, p2]:
            clipped_coords = []
        clipped_coords = [tuple(float(i) for i in j) for j in clipped_coords]
        return clipped_coords

    @classmethod
    def nicholl_lee_nicholl(cls, line: list[tuple[float]], world_limits: list[int]) -> list[tuple[float]]:
        p1, p2 = line
        xmin, ymin, xmax, ymax = world_limits
        outcode1 = cls.__compute_outcode(*p1, world_limits)
        outcode2 = cls.__compute_outcode(*p2, world_limits)
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
                    outcode1 = cls.__compute_outcode(x, y, world_limits)
                else:
                    p2 = (x, y)
                    outcode2 = cls.__compute_outcode(x, y, world_limits)

        if accept:
            return [tuple(float(i) for i in j) for j in [p1, p2]]
        else:
            return []
