###############################################################################
#        Archivo Principal del proyecto para mostrar la interfaz              #
###############################################################################
import customtkinter as ctk
import tkinter as tk
import os
from tkinter import ttk, messagebox
from database import SessionLocal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from crud import cliente_crud
from crud import ingrediente_crud 
from crud import menu_crud
from crud import pedido_crud
from crud import estadisticas_crud  # Debemos crearlo
from graficos import Graficos

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ClienteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante - Clientes")
        self.geometry("1300x900")
        self.session = SessionLocal()

        self.setup_tabs()
        self.setup_clientes_tab()
        self.setup_ingredientes_tab()
        self.setup_menus_tab()
        self.setup_pedidos_tab()
        self.graficos = Graficos(self.estadisticas_tab, self.session)


    def setup_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        self.clientes_tab = self.tabview.add("Clientes")
        self.ingredientes_tab = self.tabview.add("Ingredientes")
        self.menus_tab = self.tabview.add("Menús")
        self.pedidos_tab = self.tabview.add("Pedidos")
        self.estadisticas_tab = self.tabview.add("Estadisticas")


#------------------------------------------------------------CLIENTES-------------------------------------------------------------------#
    #Definimos la pestaña para los clientes y la setiamos
    def setup_clientes_tab(self):
        tab = self.clientes_tab

        # Formulario
        ctk.CTkLabel(tab, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        self.nombre_entry = ctk.CTkEntry(tab, width=200)
        self.nombre_entry.grid(row=0, column=1)

        ctk.CTkLabel(tab, text="Email").grid(row=1, column=0, padx=10, pady=10)
        self.email_entry = ctk.CTkEntry(tab, width=200)
        self.email_entry.grid(row=1, column=1)

        # Botones
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_cliente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar_cliente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_cliente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)

        # Tabla
        self.tree = ttk.Treeview(tab, columns=("ID", "Nombre", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

        tab.grid_rowconfigure(3, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)
        self.refrescar_clientes()

    def refrescar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        clientes = self.session.query(cliente_crud.Cliente).all()
        for c in clientes:
            self.tree.insert("", "end", values=(c.id, c.nombre, c.email))

    def crear_cliente(self):
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()
        if not nombre or not email:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return
        cliente_crud.crear_cliente(self.session, nombre, email)
        self.refrescar_clientes()
        self.limpiar_formulario()

    def actualizar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Selecciona un cliente para actualizar.")
            return
        cliente_id = int(self.tree.item(selected[0])['values'][0])
        nuevo_nombre = self.nombre_entry.get().strip()
        nuevo_email = self.email_entry.get().strip()
        if not nuevo_nombre or not nuevo_email:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return
        cliente_crud.actualizar_cliente(self.session, cliente_id, nuevo_nombre, nuevo_email)
        self.refrescar_clientes()
        self.limpiar_formulario()

    def eliminar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Selecciona un cliente para eliminar.")
            return
        cliente_id = int(self.tree.item(selected[0])['values'][0])
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este cliente?")
        if confirm:
            cliente_crud.eliminar_cliente(self.session, cliente_id)
            self.refrescar_clientes()
            self.limpiar_formulario()

    def limpiar_formulario(self):
        self.nombre_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def seleccionar_cliente(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            _, nombre, email = item["values"]
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, nombre)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, email)

#------------------------------------------------------------INGREDIENTES-------------------------------------------------------------------#
    def setup_ingredientes_tab(self):
        tab = self.ingredientes_tab

        # Color temático (verde suave)
        tab.configure(fg_color="#d6f5d6")

        # Formulario
        ctk.CTkLabel(tab, text="Nombre", text_color="black").grid(row=0, column=0, padx=10, pady=5)
        self.ing_nombre = ctk.CTkEntry(tab, width=200, text_color="white")
        self.ing_nombre.grid(row=0, column=1)

        ctk.CTkLabel(tab, text="Tipo", text_color="black").grid(row=1, column=0, padx=10, pady=5)
        self.ing_tipo = ctk.CTkEntry(tab, width=200, text_color="white")
        self.ing_tipo.grid(row=1, column=1)

        ctk.CTkLabel(tab, text="Cantidad", text_color="black").grid(row=2, column=0, padx=10, pady=5)
        self.ing_cantidad = ctk.CTkEntry(tab, width=200, text_color="white")
        self.ing_cantidad.grid(row=2, column=1)

        ctk.CTkLabel(tab, text="Unidad", text_color="black").grid(row=3, column=0, padx=10, pady=5)
        self.ing_unidad = ctk.CTkEntry(tab, width=200, text_color="white")
        self.ing_unidad.grid(row=3, column=1)

        # Botones
        btn_frame = ctk.CTkFrame(tab, fg_color="#cceacc")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_ingrediente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar_ingrediente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_ingrediente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar_formulario_ingredientes).pack(side="left", padx=5)

        # Tabla
        self.ing_tree = ttk.Treeview(tab, columns=("ID", "Nombre", "Tipo", "Cantidad", "Unidad"), show="headings")
        for col in ("ID", "Nombre", "Tipo", "Cantidad", "Unidad"):
            self.ing_tree.heading(col, text=col)
        self.ing_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        tab.grid_rowconfigure(5, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        self.ing_tree.bind("<<TreeviewSelect>>", self.seleccionar_ingrediente)

        self.refrescar_ingredientes()
    
    def refrescar_ingredientes(self):
        for row in self.ing_tree.get_children():
            self.ing_tree.delete(row)
        ingredientes = ingrediente_crud.listar_ingredientes(self.session)
        for i in ingredientes:
            self.ing_tree.insert("", "end", values=(i.id, i.nombre, i.tipo, i.cantidad, i.unidad_medida))

    def crear_ingrediente(self):
        nombre = self.ing_nombre.get().strip()
        tipo = self.ing_tipo.get().strip()
        cantidad_str = self.ing_cantidad.get().strip()
        unidad = self.ing_unidad.get().strip()

        if not nombre or not tipo or not cantidad_str or not unidad:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        try:
            cantidad = float(cantidad_str)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser un número.")
            return

        ingrediente_crud.crear_ingrediente(self.session, nombre, tipo, cantidad, unidad)
        self.refrescar_ingredientes()
        self.limpiar_formulario_ingredientes()
        self.refrescar_ingredientes_disponibles()


    def actualizar_ingrediente(self):
        selected = self.ing_tree.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Selecciona un ingrediente para actualizar.")
            return

        ingrediente_id = int(self.ing_tree.item(selected[0])['values'][0])
        nombre = self.ing_nombre.get().strip()
        tipo = self.ing_tipo.get().strip()
        cantidad_str = self.ing_cantidad.get().strip()
        unidad = self.ing_unidad.get().strip()

        if not nombre or not tipo or not cantidad_str or not unidad:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        try:
            cantidad = float(cantidad_str)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser un número.")
            return

        ingrediente_crud.actualizar_ingrediente(self.session, ingrediente_id, nombre, tipo, cantidad, unidad)
        self.refrescar_ingredientes()
        self.limpiar_formulario_ingredientes()

    def eliminar_ingrediente(self):
        selected = self.ing_tree.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Selecciona un ingrediente para eliminar.")
            return

        ingrediente_id = int(self.ing_tree.item(selected[0])['values'][0])
        confirm = messagebox.askyesno("Confirmar", "¿Eliminar este ingrediente?")
        if confirm:
            ingrediente_crud.eliminar_ingrediente(self.session, ingrediente_id)
            self.refrescar_ingredientes()
            self.limpiar_formulario_ingredientes()

    def limpiar_formulario_ingredientes(self):
        for entry in [self.ing_nombre, self.ing_tipo, self.ing_cantidad, self.ing_unidad]:
            entry.delete(0, tk.END)
        self.ing_tree.selection_remove(self.ing_tree.selection())

    def seleccionar_ingrediente(self, event):
        selected = self.ing_tree.selection()
        if selected:
            item = self.ing_tree.item(selected[0])
            _, nombre, tipo, cantidad, unidad = item["values"]
            self.ing_nombre.delete(0, tk.END)
            self.ing_nombre.insert(0, nombre)
            self.ing_tipo.delete(0, tk.END)
            self.ing_tipo.insert(0, tipo)
            self.ing_cantidad.delete(0, tk.END)
            self.ing_cantidad.insert(0, str(cantidad))
            self.ing_unidad.delete(0, tk.END)
            self.ing_unidad.insert(0, unidad)

#------------------------------------------------------------MENUS---------------------------------------------------------------------------#
    def setup_menus_tab(self):
        tab = self.menus_tab
        tab.configure(fg_color="#fff5cc") 

        # Campos nombre, descripción y precio
        ctk.CTkLabel(tab, text="Nombre", text_color="black").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.menu_nombre = ctk.CTkEntry(tab, width=250, text_color="white")
        self.menu_nombre.grid(row=0, column=1, pady=5, sticky="w")

        ctk.CTkLabel(tab, text="Descripción", text_color="black").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.menu_descripcion = ctk.CTkEntry(tab, width=250, text_color="white")
        self.menu_descripcion.grid(row=1, column=1, pady=5, sticky="w")

        ctk.CTkLabel(tab, text="Precio", text_color="black").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.menu_precio = ctk.CTkEntry(tab, width=100, text_color="white")
        self.menu_precio.grid(row=2, column=1, pady=5, sticky="w")

        # Ingredientes disponibles
        ctk.CTkLabel(tab, text="Ingrediente", text_color="black").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.ingrediente_combo = ctk.CTkComboBox(tab, width=200)
        self.ingrediente_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(tab, text="Cantidad", text_color="black").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.cantidad_entry = ctk.CTkEntry(tab, width=100, text_color="white")
        self.cantidad_entry.grid(row=4, column=1, pady=5, sticky="w")

        ctk.CTkButton(tab, text="Agregar Ingrediente", command=self.agregar_ingrediente_menu).grid(row=5, column=1, sticky="w", pady=5)

        # Tabla de ingredientes añadidos al menú
        self.ingredientes_menu = []
        self.tabla_ing_menu = ttk.Treeview(tab, columns=("ID", "Nombre", "Cantidad"), show="headings", height=4)
        for col in ("ID", "Nombre", "Cantidad"):
            self.tabla_ing_menu.heading(col, text=col)
        self.tabla_ing_menu.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        # Botones menú
        btn_frame = ctk.CTkFrame(tab, fg_color="#ffe4a1")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Crear Menú", command=self.crear_menu).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Editar Menú", command=self.editar_menu).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar_menu).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Menú", command=self.eliminar_menu).pack(side="left", padx=5)

        # Tabla de menús existentes
        self.tabla_menus = ttk.Treeview(tab, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings", height=6)
        self.tabla_menus.bind("<<TreeviewSelect>>", self.cargar_menu_seleccionado)

        for col in ("ID", "Nombre", "Descripción", "Precio"):
            self.tabla_menus.heading(col, text=col)
        self.tabla_menus.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        tab.grid_rowconfigure(8, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        self.refrescar_ingredientes_disponibles()
        self.refrescar_menus()


    def refrescar_ingredientes_disponibles(self):
        ingredientes = ingrediente_crud.listar_ingredientes(self.session)
        self.lista_ingredientes = {f"{i.nombre} ({i.unidad_medida})": i.id for i in ingredientes}
        self.ingrediente_combo.configure(values=list(self.lista_ingredientes.keys()))
        if ingredientes:
            self.ingrediente_combo.set(list(self.lista_ingredientes.keys())[0])

    def agregar_ingrediente_menu(self):
        nombre_combo = self.ingrediente_combo.get()
        cantidad = self.cantidad_entry.get().strip()

        if not nombre_combo or not cantidad:
            messagebox.showwarning("Campos vacíos", "Selecciona un ingrediente y especifica cantidad.")
            return

        try:
            cantidad = float(cantidad)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Debe ser un número.")
            return

        ing_id = self.lista_ingredientes[nombre_combo]
        self.ingredientes_menu.append((ing_id, cantidad))
        self.tabla_ing_menu.insert("", "end", values=(ing_id, nombre_combo, cantidad))
        self.cantidad_entry.delete(0, tk.END)

    def crear_menu(self):
        nombre = self.menu_nombre.get().strip()
        descripcion = self.menu_descripcion.get().strip()
        precio_str = self.menu_precio.get().strip()

        if not nombre or not descripcion or not precio_str or not self.ingredientes_menu:
            messagebox.showwarning("Datos incompletos", "Completa todos los campos, incluyendo el precio.")
            return

        try:
            precio = float(precio_str)
            if precio <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Precio inválido", "Ingresa un precio válido mayor a cero.")
            return

        exito = menu_crud.crear_menu(self.session, nombre, descripcion, self.ingredientes_menu, precio)
        if not exito:
            messagebox.showerror("Duplicado", f"Ya existe un menú llamado '{nombre}'.")
            return

        self.limpiar_menu()
        self.refrescar_menus()
        self.refrescar_menus_disponibles()


    def refrescar_menus(self):
        for i in self.tabla_menus.get_children():
            self.tabla_menus.delete(i)
        menus = menu_crud.listar_menus(self.session)
        for m in menus:
            self.tabla_menus.insert("", "end", values=(m.id, m.nombre, m.descripcion, "$"+str(m.precio)))

    def limpiar_menu(self):
        self.menu_nombre.delete(0, tk.END)
        self.menu_descripcion.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.ingredientes_menu = []
        for item in self.tabla_ing_menu.get_children():
            self.tabla_ing_menu.delete(item)

    def eliminar_menu(self):
        selected = self.tabla_menus.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Selecciona un menú para eliminar.")
            return

        menu_id = int(self.tabla_menus.item(selected[0])["values"][0])
        confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar este menú?")
        if confirm:
            menu_crud.eliminar_menu(self.session, menu_id)
            self.refrescar_menus()

    def cargar_menu_seleccionado(self, event):
        selected = self.tabla_menus.selection()
        if not selected:
            return

        values = self.tabla_menus.item(selected[0])["values"]
        self.menu_nombre.delete(0, tk.END)
        self.menu_nombre.insert(0, values[1])

        self.menu_descripcion.delete(0, tk.END)
        self.menu_descripcion.insert(0, values[2])

        self.menu_precio.delete(0, tk.END)
        self.menu_precio.insert(0, values[3].replace("$", ""))

        # Cargar ingredientes asociados
        from crud import menu_crud
        menu_id = values[0]
        ingredientes = menu_crud.obtener_ingredientes_de_menu(self.session, menu_id)

        self.ingredientes_menu.clear()
        for item in self.tabla_ing_menu.get_children():
            self.tabla_ing_menu.delete(item)

        for ing in ingredientes:
            nombre_combo = f"{ing.ingrediente.nombre} ({ing.ingrediente.unidad_medida})"
            self.ingredientes_menu.append((ing.ingrediente_id, ing.cantidad))
            self.tabla_ing_menu.insert("", "end", values=(ing.ingrediente_id, nombre_combo, ing.cantidad))

    def editar_menu(self):
        selected = self.tabla_menus.selection()
        if not selected:
            messagebox.showwarning("Sin selección", "Debes seleccionar un menú para editar.")
            return

        menu_id = self.tabla_menus.item(selected[0])["values"][0]

        nombre = self.menu_nombre.get().strip()
        descripcion = self.menu_descripcion.get().strip()
        precio_str = self.menu_precio.get().strip()

        if not nombre or not descripcion or not precio_str or not self.ingredientes_menu:
            messagebox.showwarning("Datos incompletos", "Completa todos los campos, incluyendo ingredientes.")
            return

        try:
            precio = float(precio_str)
            if precio <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Precio inválido", "Ingresa un precio mayor a 0.")
            return

        from crud import menu_crud
        exito = menu_crud.editar_menu(self.session, menu_id, nombre, descripcion, self.ingredientes_menu, precio)

        if exito:
            messagebox.showinfo("Éxito", "Menú actualizado correctamente.")
            self.limpiar_menu()
            self.refrescar_menus()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el menú.")

#------------------------------------------------------------PEDIDOS-------------------------------------------------------------------#
    def setup_pedidos_tab(self):
        tab = self.pedidos_tab
        tab.configure(fg_color="#dceeff")

        # ---------- FORMULARIO ----------
        ctk.CTkLabel(tab, text="Cliente", text_color="black").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.pedido_cliente_combo = ctk.CTkComboBox(tab, width=250)
        self.pedido_cliente_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkButton(tab, text="🔄 Actualizar Clientes", command=self.refrescar_clientes_disponibles).grid(row=0, column=2, padx=5)

        ctk.CTkLabel(tab, text="Menú", text_color="black").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.pedido_menu_combo = ctk.CTkComboBox(tab, width=250)
        self.pedido_menu_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(tab, text="Cantidad", text_color="black").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.pedido_cantidad_entry = ctk.CTkEntry(tab, width=100)
        self.pedido_cantidad_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkButton(tab, text="Agregar al Pedido", command=self.agregar_menu_al_pedido).grid(row=3, column=1, pady=10, sticky="w")

        # ---------- TABLA ----------
        self.pedido_items = []
        self.pedido_tabla = ttk.Treeview(tab, columns=("ID", "Menú", "Cantidad"), show="headings", height=6)
        for col in ("ID", "Menú", "Cantidad"):
            self.pedido_tabla.heading(col, text=col)
        self.pedido_tabla.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # ---------- TOTAL ----------
        self.pedido_total_label = ctk.CTkLabel(tab, text="Total: $0", text_color="black", font=("Arial", 16))
        self.pedido_total_label.grid(row=5, column=0, columnspan=3, pady=5)

        # ---------- BOTÓN CONFIRMAR ----------
        ctk.CTkButton(tab, text="Confirmar Pedido", command=self.confirmar_pedido).grid(row=6, column=0, columnspan=3, pady=10)

        # ---------- BOTÓN GENERAR BOLETA ---------
        ctk.CTkButton(tab, text="🧾 Generar Boleta", command=self.generar_boleta).grid(row=11, column=0, columnspan=3, pady=10)

        # ---------- CONFIGURACIÓN GRID ----------
        tab.grid_rowconfigure(4, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        # ---------- CARGA DE DATOS ----------
        self.refrescar_clientes_disponibles()
        self.refrescar_menus_disponibles()

        # ---------- HISTORIAL DE PEDIDOS ----------
        ctk.CTkLabel(tab, text="Historial de Pedidos", text_color="black", font=("Arial", 16)).grid(
            row=7, column=0, columnspan=3, pady=(20, 5)
        )

        self.historial_tabla = ttk.Treeview(tab, columns=("ID", "Cliente", "Fecha", "Total"), show="headings", height=5)
        for col in ("ID", "Cliente", "Fecha", "Total"):
            self.historial_tabla.heading(col, text=col)
            self.historial_tabla.column(col, anchor="center")

        self.historial_tabla.grid(row=8, column=0, columnspan=3, padx=10, sticky="nsew")
        self.historial_tabla.bind("<<TreeviewSelect>>", self.mostrar_detalles_pedido)

        # ---------- DETALLE DE PEDIDO SELECCIONADO ----------
        ctk.CTkLabel(tab, text="Detalle del Pedido", text_color="black", font=("Arial", 14)).grid(
            row=9, column=0, columnspan=3, pady=(10, 5)
        )

        self.detalle_tabla = ttk.Treeview(tab, columns=("Menú", "Cantidad"), show="headings", height=4)
        for col in ("Menú", "Cantidad"):
            self.detalle_tabla.heading(col, text=col)
            self.detalle_tabla.column(col, anchor="center")

        self.detalle_tabla.grid(row=10, column=0, columnspan=3, padx=10, sticky="nsew")

        self.cargar_historial_pedidos()

    
    def refrescar_clientes_disponibles(self):
        clientes = cliente_crud.listar_clientes(self.session) or []
        self.clientes_dict = {f"{c.nombre} ({c.email})": c.id for c in clientes}
        opciones = list(self.clientes_dict.keys())

        self.pedido_cliente_combo.configure(values=opciones)

        if opciones:
            self.pedido_cliente_combo.set(opciones[0])
    
    def refrescar_menus_disponibles(self):
        menus = menu_crud.listar_menus(self.session)
        self.menus_dict = {m.nombre: m.id for m in menus}
        self.pedido_menu_combo.configure(values=list(self.menus_dict.keys()))
        if menus:
            self.pedido_menu_combo.set(list(self.menus_dict.keys())[0])
    
    def agregar_menu_al_pedido(self):
        nombre = self.pedido_menu_combo.get()
        cantidad = self.pedido_cantidad_entry.get().strip()
        if not nombre or not cantidad:
            messagebox.showwarning("Campos vacíos", "Selecciona menú y cantidad.")
            return
        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Debe ser un número entero.")
            return
    
        menu_id = self.menus_dict[nombre]
        self.pedido_items.append((menu_id, cantidad))
        self.pedido_tabla.insert("", "end", values=(menu_id, nombre, cantidad))
    
        total_actual = sum(
            self.session.query(menu_crud.Menu).get(mid).precio * int(cant)
            for mid, cant in self.pedido_items
        )
        self.pedido_total_label.configure(text=f"Total: ${total_actual}")
    
        self.pedido_cantidad_entry.delete(0, tk.END)
    
    def confirmar_pedido(self):
        if not self.pedido_items:
            messagebox.showwarning("Vacío", "No has agregado menús al pedido.")
            return
    
        cliente_nombre = self.pedido_cliente_combo.get()
        cliente_id = self.clientes_dict.get(cliente_nombre)
        if not cliente_id:
            messagebox.showerror("Cliente inválido", "Selecciona un cliente válido.")
            return
    
        from crud import pedido_crud
        pedido_id = pedido_crud.crear_pedido(self.session, cliente_id, self.pedido_items)
    
        messagebox.showinfo("Éxito", f"Pedido registrado con ID {pedido_id} ✅")

        for i in self.pedido_tabla.get_children():
            self.pedido_tabla.delete(i)
        self.pedido_items.clear()
        self.pedido_total_label.configure(text="Total: $0")
        self.cargar_historial_pedidos()
        self.refrescar_ingredientes()



    def cargar_historial_pedidos(self):
        from crud import pedido_crud
        self.historial_tabla.delete(*self.historial_tabla.get_children())

        pedidos = pedido_crud.listar_pedidos(self.session)
        for p in pedidos:
            self.historial_tabla.insert("", "end", values=(p.id, p.cliente.nombre, p.fecha.strftime("%Y-%m-%d %H:%M"), f"${p.total:.0f}"))

    def mostrar_detalles_pedido(self, event):
        from crud import pedido_crud
        selected = self.historial_tabla.selection()
        if not selected:
            return
        pedido_id = int(self.historial_tabla.item(selected[0])['values'][0])

        detalles = pedido_crud.obtener_detalle_pedido(self.session, pedido_id)

        self.detalle_tabla.delete(*self.detalle_tabla.get_children())
        for d in detalles:
            self.detalle_tabla.insert("", "end", values=(d.menu.nombre, d.cantidad))

    def generar_boleta(self):
        selected = self.historial_tabla.selection()
        if not selected:
            messagebox.showwarning("Selecciona un pedido", "Debes seleccionar un pedido del historial para generar su boleta.")
            return
    
        pedido_id = int(self.historial_tabla.item(selected[0])["values"][0])
        from crud import pedido_crud
    
        pedido = self.session.query(pedido_crud.Pedido).get(pedido_id)
        detalles = pedido_crud.obtener_detalle_pedido(self.session, pedido_id)
    
        nombre_archivo = f"boleta_pedido_{pedido_id}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(f"--- BOLETA DE PEDIDO #{pedido_id} ---\n")
            f.write(f"Cliente: {pedido.cliente.nombre} ({pedido.cliente.email})\n")
            f.write(f"Fecha: {pedido.fecha.strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{'-'*35}\n")
            f.write(f"{'Menú':20} {'Cant.':>5} {'Precio':>8}\n")
            f.write(f"{'-'*35}\n")
    
            for d in detalles:
                nombre = d.menu.nombre
                cantidad = d.cantidad
                precio = d.menu.precio
                f.write(f"{nombre:20} {cantidad:>5} ${precio:>7.0f}\n")
    
            f.write(f"{'-'*35}\n")
            f.write(f"TOTAL: ${pedido.total:.0f}\n")
    
        os.startfile(nombre_archivo)
    
        messagebox.showinfo("Boleta generada", f"Boleta guardada como '{nombre_archivo}'")



if __name__ == "__main__":
    app = ClienteApp()
    app.mainloop()
