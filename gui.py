import tkinter as tk
from tkinter import ttk, messagebox
import math
from base_conocimiento import BaseConocimiento
from motor_inferencia import MotorInferencia
from busqueda_a_estrella import BusquedaAEstrella

class AppSistemaTransporte(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Inteligente de Rutas - Red Compleja de Metro")
        self.geometry("1100x750")
        self.minsize(900, 600)
        self.configure(bg="#F4F6F9")

        self.bc = BaseConocimiento()
        self.motor = MotorInferencia(self.bc)
        self.buscador = BusquedaAEstrella(self.motor, self.bc)

        self.colores_lineas = {
            "Linea_Azul": "#2563EB",
            "Linea_Roja": "#DC2626",
            "Linea_Verde": "#059669",
            "Linea_Amarilla": "#D97706",
            "Linea_Naranja": "#F97316",
            "Linea_Morada": "#7C3AED",
            "Linea_Extra": "#64748B"
        }

        self.vars_hechos = {}
        
        self._configurar_estilos()
        self._construir_layout()
        self._dibujar_red_base()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TLabel", background="#F4F6F9", font=("Helvetica", 10))
        estilo.configure("Header.TLabel", font=("Helvetica", 13, "bold"), foreground="#1E293B")
        estilo.configure("TCombobox", padding=5)
        estilo.configure("Accent.TButton", background="#1E293B", foreground="#FFFFFF", font=("Helvetica", 10, "bold"), padding=8)
        estilo.map("Accent.TButton", background=[("active", "#334155")])
        estilo.configure("TCheckbutton", background="#FFFFFF", font=("Helvetica", 9))

    def _construir_layout(self):
        panel_lateral = tk.Frame(self, bg="#FFFFFF", width=340, padx=20, pady=20, relief=tk.RIDGE, bd=1)
        panel_lateral.pack(side=tk.LEFT, fill=tk.Y)
        panel_lateral.pack_propagate(False)

        ttk.Label(panel_lateral, text="Navegación del Sistema", style="Header.TLabel").pack(anchor="w", pady=(0, 15))

        ttk.Label(panel_lateral, text="Origen:").pack(anchor="w", pady=(5, 2))
        self.cb_origen = ttk.Combobox(panel_lateral, values=list(self.bc.nodos.keys()), state="readonly")
        self.cb_origen.pack(fill=tk.X, pady=(0, 10))
        self.cb_origen.set("Naranja_Oeste")

        ttk.Label(panel_lateral, text="Destino:").pack(anchor="w", pady=(5, 2))
        self.cb_destino = ttk.Combobox(panel_lateral, values=list(self.bc.nodos.keys()), state="readonly")
        self.cb_destino.pack(fill=tk.X, pady=(0, 15))
        self.cb_destino.set("Morada_Este")

        ttk.Label(panel_lateral, text="Simulación de Incidentes (IA):", font=("Helvetica", 10, "bold"), background="#FFFFFF").pack(anchor="w", pady=(15, 5))
        
        for hecho in self.bc.datos.keys():
            var = tk.BooleanVar(value=self.bc.datos[hecho])
            self.vars_hechos[hecho] = var
            # Usar replace para limpiar el nombre en la interfaz
            texto = hecho.replace("_", " ")
            cb = ttk.Checkbutton(panel_lateral, text=texto, variable=var, command=self._actualizar_hechos)
            cb.pack(anchor="w", pady=2)

        btn_calcular = ttk.Button(panel_lateral, text="Encontrar Mejor Ruta", style="Accent.TButton", command=self.ejecutar_busqueda)
        btn_calcular.pack(fill=tk.X, pady=(20, 20))

        self.txt_resultados = tk.Text(panel_lateral, height=12, bg="#F8FAFC", fg="#0F172A", relief=tk.SOLID, bd=1, font=("Courier", 9), padx=8, pady=8)
        self.txt_resultados.pack(fill=tk.BOTH, expand=True)
        self.txt_resultados.insert(tk.END, "Configura la ruta e incidentes.")
        self.txt_resultados.config(state=tk.DISABLED)

        contenedor_mapa = tk.Frame(self, bg="#F4F6F9", padx=15, pady=15)
        contenedor_mapa.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(contenedor_mapa, text="Mapa Cartográfico de Transporte", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.canvas = tk.Canvas(contenedor_mapa, bg="#FFFFFF", relief=tk.SOLID, bd=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _actualizar_hechos(self):
        for hecho, var in self.vars_hechos.items():
            self.bc.datos[hecho] = var.get()

    def _transformar_coords(self, x, y):
        ancho = self.canvas.winfo_width() or 800
        alto = self.canvas.winfo_height() or 600
        
        coords = self.bc.nodos.values()
        max_x = max(c[0] for c in coords)
        min_x = min(c[0] for c in coords)
        max_y = max(c[1] for c in coords)
        min_y = min(c[1] for c in coords)
        
        rango_x = max_x - min_x if max_x > min_x else 1
        rango_y = max_y - min_y if max_y > min_y else 1
        
        margin_x, margin_y = 70, 70
        escala_x = (ancho - 2 * margin_x) / rango_x
        escala_y = (alto - 2 * margin_y) / rango_y
        
        px = margin_x + (x - min_x) * escala_x
        py = alto - (margin_y + (y - min_y) * escala_y)
        return px, py

    def _dibujar_red_base(self, ruta_activa=None):
        self.canvas.delete("all")
        self.update_idletasks()

        if ruta_activa is None:
            ruta_activa = []

        aristas_optimas = set()
        for i in range(len(ruta_activa) - 1):
            aristas_optimas.add((ruta_activa[i], ruta_activa[i+1]))
            aristas_optimas.add((ruta_activa[i+1], ruta_activa[i]))

        # Dibujar sombras de lineas bloqueadas
        for origen, destino, tiempo, linea in self.bc.rutas:
            x1, y1 = self._transformar_coords(*self.bc.nodos[origen])
            x2, y2 = self._transformar_coords(*self.bc.nodos[destino])
            
            es_activa = (origen, destino) in aristas_optimas
            
            # Estilo Metro
            color = "#10B981" if es_activa else self.colores_lineas.get(linea, "#94A3B8")
            grosor = 8 if es_activa else 5
            
            if self.bc.datos.get(f"{linea}_Bloqueada", False) and not es_activa:
                color = "#CBD5E1" # Linea muerta/inactiva visualmente
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor, capstyle=tk.ROUND, dash=(4, 4))
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor, capstyle=tk.ROUND)

        # Dibujar Nodos estilo Metro (Blanco con borde del color de la linea o negro)
        r = 8
        for nombre, coord in self.bc.nodos.items():
            cx, cy = self._transformar_coords(*coord)
            es_nodo_activo = nombre in ruta_activa
            
            color_fondo = "#FFFFFF"
            borde = "#10B981" if es_nodo_activo else "#334155"
            grosor_borde = 4 if es_nodo_activo else 2

            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color_fondo, outline=borde, width=grosor_borde)
            
            # Posicionar el texto alternando un poco para que no se traslapen
            offset_y = 15
            if "Norte" in nombre: offset_y = -15
            self.canvas.create_text(cx, cy + offset_y, text=nombre, font=("Helvetica", 8, "bold" if es_nodo_activo else "normal"), fill="#0F172A")

    def ejecutar_busqueda(self):
        self._actualizar_hechos()
        origen = self.cb_origen.get()
        destino = self.cb_destino.get()

        if origen == destino:
            messagebox.showinfo("Atencion", "El origen y el destino deben ser diferentes.")
            return

        camino, tiempo_total = self.buscador.buscar(origen, destino)

        if not camino:
            messagebox.showerror("Sin Ruta", "Debido a los bloqueos, es imposible llegar al destino.")
            return

        self._dibujar_red_base(ruta_activa=camino)

        self.txt_resultados.config(state=tk.NORMAL)
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.insert(tk.END, ">> RUTA OPTIMA <<\n\n")
        self.txt_resultados.insert(tk.END, f"Tiempo: {tiempo_total:.1f} min\n")
        self.txt_resultados.insert(tk.END, f"Saltos: {len(camino)}\n\n")
        
        for idx, paso in enumerate(camino, 1):
            self.txt_resultados.insert(tk.END, f" {idx}. {paso}\n")

        self.txt_resultados.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = AppSistemaTransporte()
    app.mainloop()
