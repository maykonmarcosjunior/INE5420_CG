class Clipper:
    def __init__(self, world_limits_type:str="SCN",
                 algorithm_line:str="L-B",
                 algorithm_polygon:str="S-H") -> None:

        self.__clipping_algorithm_line = algorithm_line
        self.__clipping_algorithm_polygon = algorithm_polygon

        self.__Xw_min = -1
        self.__Yw_min = -1
        self.__Xw_max  = 1
        self.__Yw_max = 1
        self.set_window(world_limits_type)


    def clip_point(self, coords: tuple[float]) -> tuple[float]:
        c_x = self.__Xw_min <= coords[0] <= self.__Xw_max
        c_y = self.__Yw_min <= coords[1] <= self.__Yw_max
        return coords if c_x and c_y else None


    def clip_line(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        if self.__clipping_algorithm_line == "L-B":
            return self.liang_barsky(coords)
        elif self.__clipping_algorithm_line == "C-S":
            return self.cohen_sutherland(coords)
        elif self.__clipping_algorithm_line == "N-L-N":
            return self.nicholl_lee_nicholl(coords)
        else:
            print("Invalid clipping algorithm")
            return []


    def clip_polygon(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        if self.__clipping_algorithm_polygon == "S-H":
            return self.sutherland_hodgman(coords)
        else:
            print("Invalid clipping algorithm")
            return []


    def clip_curve(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        clipped_coords = []
        for j in range(len(coords) - 1):
            clipped_coords += self.clip_line([coords[j], coords[j + 1]])
        return clipped_coords


    # Função para verificar se um ponto 'p' está dentro de uma aresta 'edge'
    def __inside(self, p, edge):
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


    # Função para calcular a interseção de uma aresta 'edge' com a linha formada por 'p1' e 'p2'
    def __compute_intersection(self, p1, p2, edge):
        # Usando o método de determinantes para encontrar o ponto de interseção
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = edge[0]
        x4, y4 = edge[1]


        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        # Se o determinante for zero, significa que as linhas são paralelas ou coincidentes.
        if den == 0:
            return None
        """
        Fórmula da Interseção:
            Se as linhas não forem paralelas, é possível calcular o ponto de interseção.
            A fórmula para calcular o ponto de interseção é derivada de um sistema de equações lineares.
            O ponto de interseção é calculado usando a fórmula:
                (x1 + t * (x2 - x1), y1 + t * (y2 - y1)),
            onde 't' é um parâmetro que determina a posição
            do ponto de interseção ao longo da linha formada
            por 'p1' e 'p2'.
        """
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return x, y


    def __compute_outcode(self, x: float, y: float) -> int:
        code = 0
        if x < self.__Xw_min:
            code |= 1
        elif x > self.__Xw_max:
            code |= 2
        if y < self.__Yw_min:
            code |= 4
        elif y > self.__Yw_max:
            code |= 8
        return code


    def sutherland_hodgman(self, polygon: list[tuple[float]]) -> list[tuple[float]]:
        # Cria uma cópia do polígono original para modificar
        clipped_polygon = polygon[:]
        
        window_points = [
                    (self.__Xw_min, self.__Yw_min),
                    (self.__Xw_max, self.__Yw_min),
                    (self.__Xw_max, self.__Yw_max),
                    (self.__Xw_min, self.__Yw_max)
                  ]
        window = [(window_points[i], window_points[(i + 1) % 4]) for i in range(4)]

        for edge in window:
            new_polygon = []
            if not clipped_polygon:
                break
            prev_point = clipped_polygon[-1]

            for point in clipped_polygon:
                if self.__inside(point, edge):
                    if not self.__inside(prev_point, edge):
                        intersection = self.__compute_intersection(prev_point, point, edge)
                        if intersection:
                            new_polygon.append(intersection)
                    new_polygon.append(point)
                elif self.__inside(prev_point, edge):
                    intersection = self.__compute_intersection(prev_point, point, edge)
                    if intersection:
                        new_polygon.append(intersection)
                prev_point = point

            clipped_polygon = new_polygon
        return clipped_polygon

    def liang_barsky(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        clipped_coords = []
        p1, p2 = coords
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        p = [-dx, dx, -dy, dy]
        q = [
             p1[0] - self.__Xw_min,
             self.__Xw_max - p1[0],
             p1[1] - self.__Yw_min,
             self.__Yw_max - p1[1]
            ]
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
            clipped_coords = [
                              (p1[0] + u1 * dx, p1[1] + u1 * dy),
                              (p1[0] + u2 * dx, p1[1] + u2 * dy)
                             ]
        return clipped_coords
    
    def cohen_sutherland(self, coords: list[tuple[float]]) -> list[tuple[float]]:
        p1, p2 = coords

        if p1[0] > p2[0]:
            p1, p2 = p2, p1

        RC1 = self.__compute_outcode(*p1)
        RC2 = self.__compute_outcode(*p2)

        RC0 = RC1 | RC2
        if RC0 == 0:
            return coords

        RC = RC1 & RC2
        if RC != 0:
            return []

        clipped_coords = [p1, p2]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == dy == 0:
            return self.clip_point(p1)
        elif dx == 0:
            x = p1[0]
            y1 = max((min(p1[1], self.__Yw_max)), self.__Yw_min)
            y2 = max((min(p2[1], self.__Yw_max)), self.__Yw_min)
            return [(x, y1), (x, y2)]
        elif dy == 0:
            y = p1[1]
            x1 = max((min(p1[0], self.__Xw_max)), self.__Xw_min)
            x2 = max((min(p2[0], self.__Xw_max)), self.__Xw_min)
            return [(x1, y), (x2, y)]
        m = dy / dx
        yE = m * (self.__Xw_min - p1[0]) + p1[1]
        yD = m * (self.__Xw_max - p1[0]) + p1[1]
        xT = (self.__Yw_max - p1[1]) / m + p1[0]
        xF = (self.__Yw_min - p1[1]) / m + p1[0]
        pX_min = pX_max = pY_min = pY_max = None
        if (RC0 & 1) and (self.__Yw_min <= yE <= self.__Yw_max):
            pX_min = (self.__Xw_min, yE)
            clipped_coords[0] = pX_min
        elif (RC0 & 2) and (self.__Yw_min <= yD <= self.__Yw_max):
            pX_max = (self.__Xw_max, yD)
            clipped_coords[1] = pX_max
        if (RC0 & 4) and (self.__Xw_min <= xF <= self.__Xw_max):
            pY_min = (xF, self.__Yw_min)
            if xT > xF:
                clipped_coords[0] = pY_min
            else:
                clipped_coords[1] = pY_min
        elif (RC0 & 8) and (self.__Xw_min <= xT <= self.__Xw_max):
            pY_max = (xT, self.__Yw_max)
            if xT > xF:
                clipped_coords[1] = pY_max
            else:
                clipped_coords[0] = pY_max
        if clipped_coords == [p1, p2]:
            clipped_coords = []
        clipped_coords = [tuple(float(i) for i in j) for j in clipped_coords]
        return clipped_coords

    def nicholl_lee_nicholl(self, line: list[tuple[float]]) -> list[tuple[float]]:
        p1, p2 = line
        outcode1 = self.__compute_outcode(*p1)
        outcode2 = self.__compute_outcode(*p2)
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
                    x = self.__Xw_min
                    y = p1[1] + (p2[1] - p1[1]) * (x - p1[0]) / (p2[0] - p1[0])
                elif outcode_out & 2:
                    x = self.__Xw_max
                    y = p1[1] + (p2[1] - p1[1]) * (x - p1[0]) / (p2[0] - p1[0])
                elif outcode_out & 4:
                    y = self.__Yw_min
                    x = p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1])
                elif outcode_out & 8:
                    y = self.__Yw_max
                    x = p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1])

                if outcode_out == outcode1:
                    p1 = (x, y)
                    outcode1 = self.__compute_outcode(x, y)
                else:
                    p2 = (x, y)
                    outcode2 = self.__compute_outcode(x, y)

        if accept:
            return [tuple(float(i) for i in j) for j in [p1, p2]]
        else:
            return []

    @property
    def Xw_min(self) -> int:
        return self.__Xw_min

    @property
    def Yw_min(self) -> int:
        return self.__Yw_min
    
    @property
    def Xw_max(self) -> int:
        return self.__Xw_max
    
    @property
    def Yw_max(self) -> int:
        return self.__Yw_max


    def set_window(self, limit_type:str="SCN") -> None:
        if limit_type == "SCN":
            self.__Xw_min, self.__Yw_min, self.__Xw_max, self.__Yw_max = [-1, -1, 1, 1]
        elif limit_type == "NDC":
            self.__Xw_min, self.__Yw_min, self.__Xw_max, self.__Yw_max = [0, 0, 1, 1]
        elif limit_type == "DC":
            self.__Xw_min, self.__Yw_min, self.__Xw_max, self.__Yw_max = [0, 0, 800, 600]
        else:
            print("Invalid limit type")


    def set_clipping_algorithm(self, algorithm: str) -> None:
        if algorithm in ["C-S", "L-B", "N-L-N"]:
            print("Clipping Algorithm Changed:", algorithm)
            self.__clipping_algorithm_line = algorithm
        elif algorithm in ["S-H", "NDC", "DC"]:
            print("Clipping Algorithm Changed:", "S-H")
            self.__clipping_algorithm_polygon = "S-H"
