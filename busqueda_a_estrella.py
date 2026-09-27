import math
import heapq

class BusquedaAEstrella:
    def __init__(self, motor, base_conocimiento):
        self.motor = motor
        self.bc = base_conocimiento

    def h(self, n_act, n_dest):
        x1, y1 = self.bc.nodos[n_act]
        x2, y2 = self.bc.nodos[n_dest]
        # Distancia euclidiana
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 1.5

    def buscar(self, inicio, fin):
        cola = []
        heapq.heappush(cola, (0, inicio))
        padres = {}
        
        g = {inicio: 0}
        f = {inicio: self.h(inicio, fin)}
        
        while cola:
            _, actual = heapq.heappop(cola)
            
            if actual == fin:
                return self.ruta_final(padres, actual), g[actual]
                
            for vec, t_base, lin in self.bc.vecinos(actual):
                costo = self.motor.costo(actual, vec, t_base, lin)
                temp_g = g[actual] + costo
                
                if vec not in g or temp_g < g[vec]:
                    padres[vec] = actual
                    g[vec] = temp_g
                    f[vec] = temp_g + self.h(vec, fin)
                    
                    if not any(v == vec for _, v in cola):
                        heapq.heappush(cola, (f[vec], vec))
                        
        return None, 0

    def ruta_final(self, padres, actual):
        ruta = [actual]
        while actual in padres:
            actual = padres[actual]
            ruta.append(actual)
        ruta.reverse()
        return ruta
