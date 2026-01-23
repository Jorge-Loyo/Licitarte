import customtkinter as ctk
from database.db_manager import DatabaseManager
from modules.ingreso import ModuloIngreso
from modules.gestion import ModuloGestion
from modules.dashboard import ModuloDashboard
from modules.ayuda import VentanaAyuda
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LicitarteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Licitarte - Gestión de Licitaciones Farmacéuticas")
        self.geometry("1400x800")
        self.modo_actual = "dark"
        self.actualizar_colores()
        
        self.db = DatabaseManager()
        
        if os.path.exists("Img/Logo_licitarte.png"):
            self.iconbitmap(default="Img/Logo_licitarte.png")
        
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="#4dd0e1", height=120)
        logo_frame.pack(fill="x", pady=(0, 20))
        
        if os.path.exists("Img/Logo_licitarte.png"):
            logo_img = ctk.CTkImage(Image.open("Img/Logo_licitarte.png"), size=(80, 80))
            ctk.CTkLabel(logo_frame, image=logo_img, text="").pack(pady=(10, 5))
        
        ctk.CTkLabel(logo_frame, text="LICITARTE", font=("Arial", 20, "bold"), 
                    text_color="black").pack(pady=(0, 10))
        
        self.menu_buttons = []
        
        menus = [
            ("📊 Dashboard", self.mostrar_dashboard),
            ("➕ Nueva Licitación", self.mostrar_ingreso),
            ("📋 Gestión", self.mostrar_gestion),
            ("❓ Ayuda", self.mostrar_ayuda),
        ]
        
        for texto, comando in menus:
            btn = ctk.CTkButton(
                self.sidebar,
                text=texto,
                command=comando,
                fg_color="transparent",
                hover_color="#4dd0e1",
                anchor="w",
                height=50,
                font=("Arial", 14)
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.menu_buttons.append(btn)
        
        ctk.CTkLabel(self.sidebar, text="", height=20).pack(expand=True)
        
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(side="bottom", fill="x", pady=10)
        
        self.theme_switch = ctk.CTkSwitch(footer, text="Modo Claro", command=self.cambiar_tema,
                                         font=("Arial", 12))
        self.theme_switch.pack(pady=5)
        
        ctk.CTkLabel(footer, text="v1.0", text_color="#666666", font=("Arial", 10)).pack(pady=5)
        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        self.current_module = None
        self.mostrar_dashboard()
    
    def limpiar_contenido(self):
        if self.current_module:
            self.current_module.destroy()
    
    def actualizar_colores(self):
        if self.modo_actual == "dark":
            self.configure(fg_color="#1a1a1a")
            self.colores = {
                'bg': '#1a1a1a',
                'sidebar': '#2b2b2b',
                'text': 'white',
                'card': '#2b2b2b'
            }
        else:
            self.configure(fg_color="#f0f0f0")
            self.colores = {
                'bg': '#f0f0f0',
                'sidebar': '#e0e0e0',
                'text': 'black',
                'card': '#ffffff'
            }
    
    def cambiar_tema(self):
        self.modo_actual = "light" if self.theme_switch.get() else "dark"
        ctk.set_appearance_mode(self.modo_actual)
        self.actualizar_colores()
        
        self.sidebar.configure(fg_color=self.colores['sidebar'])
        self.content_frame.configure(fg_color=self.colores['bg'])
        
        if self.current_module:
            modulo_actual = type(self.current_module).__name__
            if "Dashboard" in modulo_actual:
                self.mostrar_dashboard()
            elif "Ingreso" in modulo_actual:
                self.mostrar_ingreso()
            elif "Gestion" in modulo_actual:
                self.mostrar_gestion()
    
    def activar_boton(self, index):
        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                btn.configure(fg_color="#4dd0e1", text_color="black")
            else:
                btn.configure(fg_color="transparent")
    
    def mostrar_dashboard(self):
        self.limpiar_contenido()
        self.activar_boton(0)
        self.current_module = ModuloDashboard(self.content_frame, self.db)
        self.current_module.pack(fill="both", expand=True)
    
    def mostrar_ingreso(self):
        self.limpiar_contenido()
        self.activar_boton(1)
        self.current_module = ModuloIngreso(self.content_frame, self.db)
        self.current_module.pack(fill="both", expand=True)
    
    def mostrar_gestion(self):
        self.limpiar_contenido()
        self.activar_boton(2)
        self.current_module = ModuloGestion(self.content_frame, self.db)
        self.current_module.pack(fill="both", expand=True)
    
    def mostrar_ayuda(self):
        VentanaAyuda(self)

if __name__ == "__main__":
    app = LicitarteApp()
    app.mainloop()
