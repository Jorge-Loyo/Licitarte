import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sqlite3

class ModuloIngreso(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color="#1a1a1a")
        self.db = db_manager
        self.productos_widgets = []
        self.setup_ui()
    
    def setup_ui(self):
        ctk.CTkLabel(self, text="Nueva Licitación", font=("Arial", 24, "bold"), 
                    text_color="#4dd0e1").pack(pady=20)
        
        form_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        form_frame.pack(padx=30, pady=10, fill="x")
        
        ctk.CTkLabel(form_frame, text="N° Licitación:", text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.numero_entry = ctk.CTkEntry(form_frame, width=300, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.numero_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Fecha:", text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.fecha_entry = ctk.CTkEntry(form_frame, width=300, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.fecha_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Lab. Ganador:", text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.lab_entry = ctk.CTkEntry(form_frame, width=300, fg_color="#1a1a1a", border_color="#4dd0e1")
        self.lab_entry.grid(row=2, column=1, padx=10, pady=10)
        
        productos_header = ctk.CTkFrame(self, fg_color="#2b2b2b")
        productos_header.pack(padx=30, pady=(20, 5), fill="x")
        ctk.CTkLabel(productos_header, text="Productos", font=("Arial", 18, "bold"), 
                    text_color="#4dd0e1").pack(side="left", padx=10, pady=10)
        ctk.CTkButton(productos_header, text="+ Agregar Producto", command=self.agregar_producto_widget,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da").pack(side="right", padx=10, pady=10)
        
        self.productos_container = ctk.CTkScrollableFrame(self, fg_color="#1a1a1a", height=300)
        self.productos_container.pack(padx=30, pady=10, fill="both", expand=True)
        
        self.agregar_producto_widget()
        
        ctk.CTkButton(self, text="Guardar Licitación", command=self.guardar_licitacion,
                     fg_color="#4dd0e1", text_color="black", hover_color="#26c6da", 
                     font=("Arial", 16, "bold"), height=40).pack(pady=20)
    
    def agregar_producto_widget(self):
        producto_frame = ctk.CTkFrame(self.productos_container, fg_color="#2b2b2b")
        producto_frame.pack(padx=5, pady=5, fill="x")
        
        row1 = ctk.CTkFrame(producto_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Ítem/Producto:", text_color="white", width=100).pack(side="left", padx=5)
        item_entry = ctk.CTkEntry(row1, width=250, fg_color="#1a1a1a", border_color="#4dd0e1")
        item_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Cantidad:", text_color="white", width=80).pack(side="left", padx=5)
        cantidad_entry = ctk.CTkEntry(row1, width=100, fg_color="#1a1a1a", border_color="#4dd0e1")
        cantidad_entry.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(producto_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Precio Ofertado:", text_color="white", width=100).pack(side="left", padx=5)
        precio_entry = ctk.CTkEntry(row2, width=100, fg_color="#1a1a1a", border_color="#4dd0e1")
        precio_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Resultado:", text_color="white", width=80).pack(side="left", padx=5)
        resultado_combo = ctk.CTkComboBox(row2, values=["Adjudicado", "Parcial", "No Adjudicado"],
                                         width=150, fg_color="#1a1a1a", border_color="#4dd0e1", button_color="#4dd0e1")
        resultado_combo.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Lab. Ganador:", text_color="white", width=100).pack(side="left", padx=5)
        lab_ganador_entry = ctk.CTkEntry(row2, width=150, fg_color="#1a1a1a", border_color="#4dd0e1")
        lab_ganador_entry.pack(side="left", padx=5)
        
        btn_eliminar = ctk.CTkButton(producto_frame, text="✕", width=30, command=lambda: self.eliminar_producto_widget(producto_frame),
                                     fg_color="#ff5252", hover_color="#ff1744")
        btn_eliminar.pack(pady=5)
        
        self.productos_widgets.append({
            'frame': producto_frame,
            'item': item_entry,
            'cantidad': cantidad_entry,
            'precio': precio_entry,
            'resultado': resultado_combo,
            'lab_ganador': lab_ganador_entry
        })
    
    def eliminar_producto_widget(self, frame):
        self.productos_widgets = [p for p in self.productos_widgets if p['frame'] != frame]
        frame.destroy()
    
    def guardar_licitacion(self):
        numero = self.numero_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        lab_ganador = self.lab_entry.get().strip()
        
        if not numero or not fecha:
            messagebox.showerror("Error", "Complete los campos obligatorios")
            return
        
        if not self.productos_widgets:
            messagebox.showerror("Error", "Agregue al menos un producto")
            return
        
        try:
            productos_validos = []
            for producto in self.productos_widgets:
                item = producto['item'].get().strip()
                cantidad_str = producto['cantidad'].get().strip()
                precio_str = producto['precio'].get().strip()
                
                if not item or not cantidad_str or not precio_str:
                    messagebox.showerror("Error", "Complete todos los campos de productos")
                    return
                
                try:
                    cantidad = int(cantidad_str)
                    precio = float(precio_str)
                    if cantidad <= 0 or precio < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Error", "Cantidad y precio deben ser números válidos")
                    return
                
                resultado = producto['resultado'].get()
                lab_gan = producto['lab_ganador'].get().strip()
                productos_validos.append((item, cantidad, precio, resultado, lab_gan))
            
            licitacion_id = self.db.crear_licitacion(numero, fecha, lab_ganador)
            
            for item, cantidad, precio, resultado, lab_gan in productos_validos:
                self.db.agregar_producto(licitacion_id, item, cantidad, precio, resultado, None, lab_gan)
            
            messagebox.showinfo("Éxito", "Licitación guardada correctamente")
            self.limpiar_formulario()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El número de licitación ya existe")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        self.numero_entry.delete(0, 'end')
        self.fecha_entry.delete(0, 'end')
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.lab_entry.delete(0, 'end')
        
        for producto in self.productos_widgets:
            producto['frame'].destroy()
        self.productos_widgets.clear()
        self.agregar_producto_widget()
