import customtkinter as ctk
from tkinter import messagebox, ttk

class ModuloGestion(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="#1a1a1a")
        self.db = db_manager
        self.setup_ui()
        self.cargar_licitaciones()
    
    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="#2b2b2b")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header, text="Gestión de Licitaciones", font=("Arial", 24, "bold"), 
                    text_color="#4dd0e1").pack(side="left", padx=20, pady=10)
        
        ctk.CTkButton(header, text="🔄 Actualizar", command=self.cargar_licitaciones,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(side="right", padx=10)
        
        search_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Buscar:", text_color="white").pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(search_frame, width=300, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.cargar_licitaciones())
        
        table_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1a1a1a", foreground="white", 
                       fieldbackground="#1a1a1a", borderwidth=0)
        style.configure("Treeview.Heading", background="#4dd0e1", foreground="black", 
                       font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", "#4dd0e1")])
        
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Número", "Fecha", "Lab. Ganador"), 
                                show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Número", text="N° Licitación")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Lab. Ganador", text="Laboratorio Ganador")
        
        self.tree.column("ID", width=50)
        self.tree.column("Número", width=200)
        self.tree.column("Fecha", width=150)
        self.tree.column("Lab. Ganador", width=250)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.ver_detalle)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Ver Detalle", command=self.ver_detalle,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_licitacion,
                     fg_color="#ff5252", hover_color="#ff1744").pack(side="left", padx=10)
    
    def cargar_licitaciones(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        licitaciones = self.db.obtener_licitaciones()
        search_term = self.search_entry.get().lower()
        
        for lic in licitaciones:
            if search_term in str(lic[1]).lower() or search_term in str(lic[3]).lower():
                self.tree.insert("", "end", values=lic)
    
    def ver_detalle(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una licitación")
            return
        
        item = self.tree.item(selected[0])
        licitacion_id = item['values'][0]
        
        VentanaDetalle(self, self.db, licitacion_id, self.cargar_licitaciones)
    
    def eliminar_licitacion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una licitación")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar esta licitación?"):
            item = self.tree.item(selected[0])
            licitacion_id = item['values'][0]
            self.db.eliminar_licitacion(licitacion_id)
            self.cargar_licitaciones()

class VentanaDetalle(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, licitacion_id, callback):
        super().__init__(parent)
        self.db = db_manager
        self.licitacion_id = licitacion_id
        self.callback = callback
        
        self.title("Detalle de Licitación")
        self.geometry("1000x600")
        self.configure(fg_color="#1a1a1a")
        
        ctk.CTkLabel(self, text="Productos de la Licitación", font=("Arial", 20, "bold"), 
                    text_color="#4dd0e1").pack(pady=20)
        
        table_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Ítem", "Cantidad", "Precio Ofertado", 
                                "Resultado", "Precio Ganador", "Lab. Ganador"), show="headings")
        
        for col in ("ID", "Ítem", "Cantidad", "Precio Ofertado", "Resultado", "Precio Ganador", "Lab. Ganador"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.cargar_productos()
        
        ctk.CTkButton(self, text="Editar Producto", command=self.editar_producto,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(pady=10)
        ctk.CTkButton(self, text="Cerrar", command=self.destroy,
                     fg_color="#666666", hover_color="#555555").pack(pady=5)
    
    def cargar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.db.obtener_productos_licitacion(self.licitacion_id)
        for prod in productos:
            self.tree.insert("", "end", values=prod)
    
    def editar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        item = self.tree.item(selected[0])
        VentanaEditarProducto(self, self.db, item['values'], self.cargar_productos)

class VentanaEditarProducto(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, producto_data, callback):
        super().__init__(parent)
        self.db = db_manager
        self.producto_id = producto_data[0]
        self.callback = callback
        
        self.title("Editar Producto")
        self.geometry("500x450")
        self.configure(fg_color="#1a1a1a")
        
        form = ctk.CTkFrame(self, fg_color="#2b2b2b")
        form.pack(padx=30, pady=30, fill="both", expand=True)
        
        fields = [
            ("Ítem/Producto:", producto_data[2]),
            ("Cantidad:", producto_data[3]),
            ("Precio Ofertado:", producto_data[4]),
        ]
        
        self.entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(form, text=label, text_color="white").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry = ctk.CTkEntry(form, width=250, fg_color="#1a1a1a", border_color="#4dd0e1")
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[label] = entry
        
        ctk.CTkLabel(form, text="Resultado:", text_color="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.resultado_combo = ctk.CTkComboBox(form, values=["Adjudicado", "Parcial", "No Adjudicado"],
                                              width=250, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.resultado_combo.set(producto_data[5])
        self.resultado_combo.grid(row=3, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form, text="Precio Ganador:", text_color="white").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.precio_ganador_entry = ctk.CTkEntry(form, width=250, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.precio_ganador_entry.insert(0, str(producto_data[6] or ""))
        self.precio_ganador_entry.grid(row=4, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form, text="Lab. Ganador:", text_color="white").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.lab_entry = ctk.CTkEntry(form, width=250, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.lab_entry.insert(0, str(producto_data[7] or ""))
        self.lab_entry.grid(row=5, column=1, padx=10, pady=10)
        
        ctk.CTkButton(self, text="Guardar", command=self.guardar,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(pady=10)
    
    def guardar(self):
        try:
            item = self.entries["Ítem/Producto:"].get().strip()
            cantidad_str = self.entries["Cantidad:"].get().strip()
            precio_str = self.entries["Precio Ofertado:"].get().strip()
            
            if not item or not cantidad_str or not precio_str:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            try:
                cantidad = int(cantidad_str)
                precio = float(precio_str)
                if cantidad <= 0 or precio < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Cantidad y precio deben ser números válidos")
                return
            
            resultado = self.resultado_combo.get()
            precio_ganador_str = self.precio_ganador_entry.get().strip()
            precio_ganador = float(precio_ganador_str) if precio_ganador_str else None
            lab_ganador = self.lab_entry.get().strip()
            
            self.db.actualizar_producto(self.producto_id, item, cantidad, precio, resultado, precio_ganador, lab_ganador)
            messagebox.showinfo("Éxito", "Producto actualizado")
            self.callback()
            self.destroy()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
