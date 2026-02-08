import customtkinter as ctk
from tkinter import ttk

class VentanaAyuda(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Manual de Usuario - Licitarte")
        self.geometry("900x700")
        self.configure(fg_color="#1a1a1a")
        
        header = ctk.CTkFrame(self, fg_color="#4dd0e1", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="📖 Manual de Usuario", font=("Arial", 24, "bold"),
                    text_color="black").pack(pady=25)
        
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        sidebar = ctk.CTkFrame(main_container, width=200, fg_color="#2b2b2b")
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        ctk.CTkLabel(sidebar, text="Secciones", font=("Arial", 16, "bold"),
                    text_color="#4dd0e1").pack(pady=15)
        
        self.content_frame = ctk.CTkScrollableFrame(main_container, fg_color="#2b2b2b")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        secciones = [
            ("🏠 Inicio", self.mostrar_inicio),
            ("➕ Nueva Licitación", self.mostrar_ingreso),
            ("📋 Gestión", self.mostrar_gestion),
            ("📊 Dashboard", self.mostrar_dashboard),
            ("🔧 Consejos", self.mostrar_consejos),
        ]
        
        for texto, comando in secciones:
            ctk.CTkButton(sidebar, text=texto, command=comando, fg_color="transparent",
                         hover_color="#4dd0e1", anchor="w", height=40).pack(fill="x", padx=5, pady=2)
        
        ctk.CTkButton(self, text="Cerrar", command=self.destroy,
                     fg_color="#666666", hover_color="#555555").pack(pady=10)
        
        self.mostrar_inicio()
    
    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def agregar_titulo(self, texto):
        ctk.CTkLabel(self.content_frame, text=texto, font=("Arial", 20, "bold"),
                    text_color="#4dd0e1", anchor="w").pack(pady=(10, 5), padx=10, fill="x")
    
    def agregar_subtitulo(self, texto):
        ctk.CTkLabel(self.content_frame, text=texto, font=("Arial", 16, "bold"),
                    text_color="white", anchor="w").pack(pady=(15, 5), padx=10, fill="x")
    
    def agregar_texto(self, texto):
        ctk.CTkLabel(self.content_frame, text=texto, font=("Arial", 12),
                    text_color="#cccccc", anchor="w", wraplength=600, justify="left").pack(pady=2, padx=20, fill="x")
    
    def mostrar_inicio(self):
        self.limpiar_contenido()
        self.agregar_titulo("Bienvenido a Licitarte")
        
        self.agregar_texto("Licitarte es una aplicación profesional para gestionar licitaciones farmacéuticas.")
        self.agregar_texto("")
        
        self.agregar_subtitulo("✨ Características Principales")
        self.agregar_texto("• Registrar licitaciones con múltiples productos")
        self.agregar_texto("• Gestionar y editar información de licitaciones")
        self.agregar_texto("• Dashboard con estadísticas en tiempo real")
        self.agregar_texto("• Consultar histórico de precios y ganadores")
        self.agregar_texto("• Modo claro y oscuro")
        self.agregar_texto("")
        
        self.agregar_subtitulo("🚀 Inicio Rápido")
        self.agregar_texto("1. Use el menú lateral para navegar entre módulos")
        self.agregar_texto("2. Comience creando una nueva licitación")
        self.agregar_texto("3. Agregue productos dinámicamente")
        self.agregar_texto("4. Consulte estadísticas en el Dashboard")
    
    def mostrar_ingreso(self):
        self.limpiar_contenido()
        self.agregar_titulo("➕ Nueva Licitación")
        
        self.agregar_subtitulo("Campos de Licitación")
        self.agregar_texto("• N° Licitación: Número único identificador (obligatorio)")
        self.agregar_texto("• Fecha: Formato YYYY-MM-DD (obligatorio)")
        self.agregar_texto("• Lab. Ganador: Laboratorio ganador general (opcional)")
        self.agregar_texto("")
        
        self.agregar_subtitulo("Campos de Producto")
        self.agregar_texto("• Ítem/Producto: Nombre del producto (obligatorio)")
        self.agregar_texto("• Cantidad: Unidades licitadas, debe ser mayor a 0 (obligatorio)")
        self.agregar_texto("• Precio Ofertado: Precio que usted ofreció (obligatorio)")
        self.agregar_texto("• Resultado: Adjudicado / Parcial / No Adjudicado (obligatorio)")
        self.agregar_texto("• Lab. Ganador: Laboratorio que ganó el ítem (opcional)")
        self.agregar_texto("")
        
        self.agregar_subtitulo("📝 Pasos para Registrar")
        self.agregar_texto("1. Complete los datos de la licitación")
        self.agregar_texto("2. Agregue productos con el botón '+ Agregar Producto'")
        self.agregar_texto("3. Complete información de cada producto")
        self.agregar_texto("4. Use el botón '✕' para eliminar productos no deseados")
        self.agregar_texto("5. Clic en 'Guardar Licitación'")
        self.agregar_texto("")
        
        self.agregar_subtitulo("💡 Nota Importante")
        self.agregar_texto("Si marca un producto como 'Adjudicado', el precio ganador se completará automáticamente con su precio ofertado.")
    
    def mostrar_gestion(self):
        self.limpiar_contenido()
        self.agregar_titulo("📋 Gestión de Licitaciones")
        
        self.agregar_subtitulo("Funciones Disponibles")
        self.agregar_texto("• Ver todas las licitaciones registradas")
        self.agregar_texto("• Buscar por N° de licitación o laboratorio")
        self.agregar_texto("• Ver detalle de productos de cada licitación")
        self.agregar_texto("• Editar información de productos")
        self.agregar_texto("• Eliminar licitaciones completas")
        self.agregar_texto("")
        
        self.agregar_subtitulo("🔍 Búsqueda")
        self.agregar_texto("Use el campo de búsqueda para filtrar licitaciones en tiempo real.")
        self.agregar_texto("Puede buscar por número de licitación o nombre de laboratorio.")
        self.agregar_texto("")
        
        self.agregar_subtitulo("📝 Ver y Editar Detalle")
        self.agregar_texto("1. Doble clic en una licitación, o")
        self.agregar_texto("2. Seleccionar y clic en 'Ver Detalle'")
        self.agregar_texto("3. Se abrirá ventana con todos los productos")
        self.agregar_texto("4. Seleccione un producto y clic en 'Editar Producto'")
        self.agregar_texto("5. Modifique los campos necesarios")
        self.agregar_texto("6. Guarde los cambios")
        self.agregar_texto("")
        
        self.agregar_subtitulo("⚠️ Eliminar Licitación")
        self.agregar_texto("ADVERTENCIA: Esta acción elimina la licitación y TODOS sus productos permanentemente.")
        self.agregar_texto("1. Seleccione la licitación")
        self.agregar_texto("2. Clic en 'Eliminar'")
        self.agregar_texto("3. Confirme la acción")
    
    def mostrar_dashboard(self):
        self.limpiar_contenido()
        self.agregar_titulo("📊 Dashboard - Análisis")
        
        self.agregar_subtitulo("Tarjetas de Estadísticas")
        self.agregar_texto("• Total Licitaciones: Todas las licitaciones registradas")
        self.agregar_texto("• Licitaciones Ganadas: Con al menos un producto adjudicado")
        self.agregar_texto("• Total Unidades: Suma de cantidades de todos los productos")
        self.agregar_texto("• Precio Promedio Ponderado: Promedio de precios ganados considerando cantidades")
        self.agregar_texto("")
        
        self.agregar_subtitulo("🔍 Histórico de Producto")
        self.agregar_texto("Consulte información de la última vez que ganó un producto:")
        self.agregar_texto("1. Escriba el nombre del producto (o parte de él)")
        self.agregar_texto("2. Clic en 'Buscar'")
        self.agregar_texto("3. Verá: N° Licitación, Precio Ganador, Laboratorio y Fecha")
        self.agregar_texto("")
        
        self.agregar_subtitulo("📋 Tabla de Productos Adjudicados")
        self.agregar_texto("Muestra todos los productos que ha ganado con:")
        self.agregar_texto("• N° de Licitación")
        self.agregar_texto("• Nombre del producto")
        self.agregar_texto("• Cantidad adjudicada")
        self.agregar_texto("• Precio ofertado")
        self.agregar_texto("• Fecha de adjudicación")
        self.agregar_texto("")
        
        self.agregar_subtitulo("🔄 Actualizar Datos")
        self.agregar_texto("Use el botón '🔄 Actualizar' para refrescar las estadísticas después de hacer cambios.")
    
    def mostrar_consejos(self):
        self.limpiar_contenido()
        self.agregar_titulo("🔧 Consejos y Mejores Prácticas")
        
        self.agregar_subtitulo("📝 Ingreso de Datos")
        self.agregar_texto("• Use formato de fecha consistente: YYYY-MM-DD")
        self.agregar_texto("• Escriba nombres de productos de forma clara y consistente")
        self.agregar_texto("• Verifique cantidades y precios antes de guardar")
        self.agregar_texto("• Use nombres completos de laboratorios")
        self.agregar_texto("")
        
        self.agregar_subtitulo("💾 Respaldo de Datos")
        self.agregar_texto("IMPORTANTE: Haga respaldos periódicos de su información")
        self.agregar_texto("1. Copie el archivo 'database/licitaciones.db'")
        self.agregar_texto("2. Guárdelo en ubicación segura (USB, nube)")
        self.agregar_texto("3. Etiquete con fecha: licitaciones_backup_2024-01-15.db")
        self.agregar_texto("4. Mantenga múltiples versiones")
        self.agregar_texto("")
        
        self.agregar_subtitulo("🎨 Personalización")
        self.agregar_texto("• Use el switch 'Modo Claro' en el menú para cambiar el tema")
        self.agregar_texto("• El tema se aplica a toda la aplicación instantáneamente")
        self.agregar_texto("")
        
        self.agregar_subtitulo("⚡ Atajos y Trucos")
        self.agregar_texto("• Doble clic en licitación = Ver detalle rápido")
        self.agregar_texto("• Búsqueda en tiempo real en Gestión")
        self.agregar_texto("• Histórico acepta búsquedas parciales")
        self.agregar_texto("• Resultado 'Adjudicado' autocompleta precio ganador")
        self.agregar_texto("")
        
        self.agregar_subtitulo("⚠️ Errores Comunes")
        self.agregar_texto("• 'N° licitación ya existe': Use un número diferente")
        self.agregar_texto("• 'Cantidad debe ser mayor a 0': Ingrese números positivos")
        self.agregar_texto("• 'Complete todos los campos': Verifique campos obligatorios")
        self.agregar_texto("")
        
        self.agregar_subtitulo("📞 Soporte")
        self.agregar_texto("Si tiene problemas o sugerencias, contacte al desarrollador.")
