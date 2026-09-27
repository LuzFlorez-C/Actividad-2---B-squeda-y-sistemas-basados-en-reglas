#=================================Clase: motorInferencia=========================================
#Motor de inferencia principal para la toma de desición y filtrado de rutas de tráfico.
#================================================================================================
class MotorInferencia:
    def __init__(self, base_conocimiento):
        self.bc = base_conocimiento

    def costo(self, origen, destino, t_base, linea):
        extra = 0
        datos = self.bc.datos

        # Reglas dinamicas
        if datos.get("Linea_Azul_Bloqueada") and linea == "Linea_Azul":
            extra += 1000  # Bloqueo total, forzar al algoritmo A* a buscar alternativas
            
        if datos.get("Linea_Roja_Bloqueada") and linea == "Linea_Roja":
            extra += 1000  
            
        if datos.get("Trafico_Anillo_Central") and linea == "Linea_Amarilla":
            extra += 15    # Trafico lento
            
        if datos.get("Clima_Lluvia_Fuerte"):
            extra += t_base * 0.5  # Todo tarda 50% mas
            
        return t_base + extra
