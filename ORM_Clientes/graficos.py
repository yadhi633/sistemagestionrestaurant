import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from crud import estadisticas_crud

class Graficos:
    def __init__(self, parent_tab, session):
        self.session = session
        self.tab = parent_tab
        self.grafico_frame = None
        self.setup_estadisticas_tab()

    def setup_estadisticas_tab(self):
        tab = self.tab
        tab.configure(fg_color="#f0f8ff")  # Azul muy claro

        ctk.CTkLabel(tab, text="Estadísticas de Pedidos", font=("Arial", 18), text_color="black").pack(pady=10)

        botones_frame = ctk.CTkFrame(tab)
        botones_frame.pack(pady=10)

        ctk.CTkButton(botones_frame, text="Top Menús Más Pedidos", command=self.graficar_menus_mas_pedidos).pack(side="left", padx=5)
        ctk.CTkButton(botones_frame, text="Pedidos por Cliente", command=self.graficar_pedidos_por_cliente).pack(side="left", padx=5)
        ctk.CTkButton(botones_frame, text="Gasto Total por Cliente", command=self.graficar_gasto_por_cliente).pack(side="left", padx=5)

        self.grafico_frame = ctk.CTkFrame(tab)
        self.grafico_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def graficar_menus_mas_pedidos(self):
        datos = estadisticas_crud.obtener_top_menus(self.session)
        nombres = [d[0] for d in datos]
        cantidades = [d[1] for d in datos]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(nombres, cantidades, color="#4a90e2")
        ax.set_title("Top Menús Más Pedidos")
        ax.set_ylabel("Cantidad Pedida")
        ax.set_xlabel("Menú")

        self.mostrar_grafico(fig)

    def graficar_pedidos_por_cliente(self):
        datos = estadisticas_crud.obtener_pedidos_por_cliente(self.session)
        nombres = [d[0] for d in datos]
        cantidades = [d[1] for d in datos]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(nombres, cantidades, color="#f39c12")
        ax.set_title("Cantidad de Pedidos por Cliente")
        ax.set_ylabel("Pedidos")
        ax.set_xlabel("Cliente")

        self.mostrar_grafico(fig)

    def graficar_gasto_por_cliente(self):
        datos = estadisticas_crud.obtener_gasto_total_por_cliente(self.session)
        nombres = [d[0] for d in datos]
        totales = [d[1] for d in datos]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(nombres, totales, color="#27ae60")
        ax.set_title("Gasto Total por Cliente")
        ax.set_ylabel("Monto $")
        ax.set_xlabel("Cliente")

        self.mostrar_grafico(fig)

    def mostrar_grafico(self, fig):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
