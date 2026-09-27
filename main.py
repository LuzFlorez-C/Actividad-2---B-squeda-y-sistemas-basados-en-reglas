from base_conocimiento import BaseConocimiento
from motor_inferencia import MotorInferencia
from busqueda_a_estrella import BusquedaAEstrella

def main():
    bc = BaseConocimiento()
    motor = MotorInferencia(bc)
    buscador = BusquedaAEstrella(motor, bc)

    print("=" * 60)
    print("SISTEMA INTELIGENTE DE RUTAS - TRANSPORTE MASIVO")
    print("=" * 60)
    print("Estaciones disponibles:")
    for idx, est in enumerate(bc.nodos.keys(), 1):
        print(f"{idx}. {est}")
    print("-" * 60)

    ini = input("Ingrese la estación de Origen: ").strip()
    fin = input("Ingrese la estación de Destino: ").strip()

    if ini not in bc.nodos or fin not in bc.nodos:
        print("\n[!] Error: Una o ambas estaciones ingresadas no existen en la base de hechos.")
        return

    ruta, t_est = buscador.buscar(ini, fin)

    if ruta:
        print("\n>>> RUTA ÓPTIMA ENCONTRADA <<<")
        print("Trayecto:", " -> ".join(ruta))
        print(f"Costo Total Estimado (Tiempo + Transbordos): {t_est:.1f} minutos")
    else:
        print("\n[X] No existe una ruta posible entre los puntos seleccionados.")

if __name__ == "__main__":
    main()