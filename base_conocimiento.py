class BaseConocimiento:
    def __init__(self):
        # Topologia estilo Metro: red densa y mallada con conexiones ortogonales y diagonales
        self.nodos = {
            # Linea Azul (Eje Central Horizontal Y=10)
            "Azul_Oeste": (2, 10),
            "Azul_Interseccion_1": (6, 10),
            "Central": (10, 10),
            "Azul_Interseccion_2": (14, 10),
            "Azul_Este": (18, 10),

            # Linea Roja (Eje Central Vertical X=10)
            "Roja_Norte": (10, 18),
            "Roja_Interseccion_1": (10, 14),
            "Roja_Interseccion_2": (10, 6),
            "Roja_Sur": (10, 2),

            # Linea Verde (Diagonal Principal Suroeste a Noreste)
            "Verde_Suroeste": (2, 2),
            "Anillo_Suroeste": (6, 6),
            "Anillo_Noreste": (14, 14),
            "Verde_Noreste": (18, 18),

            # Linea Amarilla (Anillo Central)
            "Anillo_Noroeste": (6, 14),
            "Anillo_Sureste": (14, 6),

            # Linea Naranja (Transversal Norte Y=14)
            "Naranja_Oeste": (2, 14),
            "Naranja_Este": (18, 14),
            
            # Linea Morada (Transversal Sur Y=6)
            "Morada_Oeste": (2, 6),
            "Morada_Este": (18, 6),
            
            # Extras para agregar complejidad (Nodos flotantes intermedios)
            "Cruce_Diagonal_Oeste": (6, 12),
            "Cruce_Diagonal_Este": (14, 12)
        }

        # Conexiones (Origen, Destino, Tiempo Base, Linea)
        self.rutas = [
            # Linea Azul
            ("Azul_Oeste", "Azul_Interseccion_1", 4, "Linea_Azul"),
            ("Azul_Interseccion_1", "Central", 4, "Linea_Azul"),
            ("Central", "Azul_Interseccion_2", 4, "Linea_Azul"),
            ("Azul_Interseccion_2", "Azul_Este", 4, "Linea_Azul"),

            # Linea Roja
            ("Roja_Norte", "Roja_Interseccion_1", 4, "Linea_Roja"),
            ("Roja_Interseccion_1", "Central", 4, "Linea_Roja"),
            ("Central", "Roja_Interseccion_2", 4, "Linea_Roja"),
            ("Roja_Interseccion_2", "Roja_Sur", 4, "Linea_Roja"),

            # Linea Verde
            ("Verde_Suroeste", "Anillo_Suroeste", 5, "Linea_Verde"),
            ("Anillo_Suroeste", "Central", 5, "Linea_Verde"),
            ("Central", "Anillo_Noreste", 5, "Linea_Verde"),
            ("Anillo_Noreste", "Verde_Noreste", 5, "Linea_Verde"),

            # Linea Amarilla (Anillo Central)
            ("Anillo_Suroeste", "Anillo_Noroeste", 8, "Linea_Amarilla"),
            ("Anillo_Noroeste", "Anillo_Noreste", 8, "Linea_Amarilla"),
            ("Anillo_Noreste", "Anillo_Sureste", 8, "Linea_Amarilla"),
            ("Anillo_Sureste", "Anillo_Suroeste", 8, "Linea_Amarilla"),

            # Linea Naranja
            ("Naranja_Oeste", "Anillo_Noroeste", 4, "Linea_Naranja"),
            ("Anillo_Noroeste", "Roja_Interseccion_1", 4, "Linea_Naranja"),
            ("Roja_Interseccion_1", "Anillo_Noreste", 4, "Linea_Naranja"),
            ("Anillo_Noreste", "Naranja_Este", 4, "Linea_Naranja"),

            # Linea Morada
            ("Morada_Oeste", "Anillo_Suroeste", 4, "Linea_Morada"),
            ("Anillo_Suroeste", "Roja_Interseccion_2", 4, "Linea_Morada"),
            ("Roja_Interseccion_2", "Anillo_Sureste", 4, "Linea_Morada"),
            ("Anillo_Sureste", "Morada_Este", 4, "Linea_Morada"),
            
            # Conexiones Diagonales Extra para complejidad
            ("Azul_Interseccion_1", "Cruce_Diagonal_Oeste", 3, "Linea_Extra"),
            ("Cruce_Diagonal_Oeste", "Anillo_Noroeste", 3, "Linea_Extra"),
            ("Azul_Interseccion_2", "Cruce_Diagonal_Este", 3, "Linea_Extra"),
            ("Cruce_Diagonal_Este", "Anillo_Noreste", 3, "Linea_Extra")
        ]

        # Hechos para el motor de inferencia (Controlables por UI)
        self.datos = {
            "Linea_Azul_Bloqueada": False,
            "Linea_Roja_Bloqueada": False,
            "Trafico_Anillo_Central": False,
            "Clima_Lluvia_Fuerte": False
        }

    def vecinos(self, n):
        v = []
        for ini, fin, t, lin in self.rutas:
            if ini == n:
                v.append((fin, t, lin))
            elif fin == n:
                v.append((ini, t, lin))
        return v