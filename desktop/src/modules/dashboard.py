import customtkinter as ctk
from tkinter import ttk, messagebox

class ModuloDashboard(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="#1a1a1a")
        self.db = db_manager
        self.setup_ui()
        self.actualizar_estadisticas()
    
    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="#2b2b2b")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header, text="Dashboard - Análisis de Licitaciones", font=("Arial", 24, "bold"), 
                    text_color="#4dd0e1").pack(side="left", padx=20, pady=10)
        
        ctk.CTkButton(header, text="🔄 Actualizar", command=self.actualizar_estadisticas,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(side="right", padx=10)
        
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=10)
        
        self.stat_cards = []
        stats_info = [
            ("Total Licitaciones", "total_licitaciones", "#4dd0e1"),
            ("Licitaciones Ganadas", "licitaciones_ganadas", "#66bb6a"),
            ("Total Unidades", "total_unidades", "#ffa726"),
            ("Precio Promedio Ponderado", "precio_promedio_ponderado", "#ab47bc")
        ]
        
        for i, (titulo, key, color) in enumerate(stats_info):
            card = self.crear_stat_card(stats_container, titulo, "0", color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            self.stat_cards.append((card, key))
            stats_container.grid_columnconfigure(i, weight=1)
        
        historico_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        historico_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(historico_frame, text="Histórico de Producto", font=("Arial", 18, "bold"), 
                    text_color="#4dd0e1").pack(pady=10)
        
        search_frame = ctk.CTkFrame(historico_frame, fg_color="transparent")
        search_frame.pack(pady=10)
        
        ctk.CTkLabel(search_frame, text="Buscar Producto:", text_color="white").pack(side="left", padx=10)
        self.producto_entry = ctk.CTkEntry(search_frame, width=300, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.producto_entry.pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="Buscar", command=self.buscar_historico,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(side="left", padx=10)
        
        self.historico_label = ctk.CTkLabel(historico_frame, text="", text_color="white", 
                                           font=("Arial", 14), wraplength=800, justify="left")
        self.historico_label.pack(pady=20, padx=20)
        
        productos_ganados_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        productos_ganados_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(productos_ganados_frame, text="Productos Adjudicados", font=("Arial", 18, "bold"), 
                    text_color="#4dd0e1").pack(pady=10)
        
        table_frame = ctk.CTkFrame(productos_ganados_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(table_frame, columns=("Licitación", "Producto", "Cantidad", 
                                "Precio Ofertado", "Fecha"), show="headings", height=10)
        
        for col in ("Licitación", "Producto", "Cantidad", "Precio Ofertado", "Fecha"):
            self.tree.heading(col, text=col)
        
        self.tree.column("Licitación", width=150)
        self.tree.column("Producto", width=250)
        self.tree.column("Cantidad", width=100)
        self.tree.column("Precio Ofertado", width=150)
        self.tree.column("Fecha", width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_stat_card(self, parent, titulo, valor, color):
        card = ctk.CTkFrame(parent, fg_color="#2b2b2b", border_width=2, border_color=color)
        
        ctk.CTkLabel(card, text=titulo, font=("Arial", 14), text_color="white").pack(pady=(15, 5))
        valor_label = ctk.CTkLabel(card, text=valor, font=("Arial", 28, "bold"), text_color=color)
        valor_label.pack(pady=(5, 15))
        
        card.valor_label = valor_label
        return card
    
    def actualizar_estadisticas(self):
        stats = self.db.obtener_estadisticas()
        
        for card, key in self.stat_cards:
            valor = stats[key]
            if key == "precio_promedio_ponderado":
                card.valor_label.configure(text=f"${valor:,.2f}")
            else:
                card.valor_label.configure(text=f"{int(valor):,}")
        
        self.cargar_productos_ganados()
    
    def cargar_productos_ganados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT l.numero_licitacion, p.item_producto, p.cantidad, p.precio_ofertado, l.fecha
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    WHERE p.resultado = 'Adjudicado'
                    ORDER BY l.fecha DESC
                """)
                productos = cursor.fetchall()
            
            for prod in productos:
                self.tree.insert("", "end", values=(prod[0], prod[1], prod[2], f"${prod[3]:,.2f}", prod[4]))
        except Exception as e:
            print(f"Error al cargar productos: {e}")
    
    def buscar_historico(self):
        producto = self.producto_entry.get().strip()
        if not producto:
            self.historico_label.configure(text="Ingrese un nombre de producto")
            return
        
        resultado = self.db.obtener_historico_producto(producto)
        
        if resultado:
            precio, lab, fecha, num_lic = resultado
            texto = f"Última licitación ganada del producto '{producto}':\n\n"
            texto += f"• N° Licitación: {num_lic}\n"
            texto += f"• Precio Ganador: ${precio:,.2f}\n"
            texto += f"• Laboratorio Ganador: {lab}\n"
            texto += f"• Fecha: {fecha}"
            self.historico_label.configure(text=texto)
        else:
            self.historico_label.configure(text=f"No se encontró historial para '{producto}'")
