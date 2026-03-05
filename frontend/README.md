# Frontend Modular - Licitarte

## Estructura

```
frontend/
├── modules/                    # Módulos de la aplicación
│   ├── administracion/        # Gestión de datos maestros
│   ├── dashboard/            # Panel principal con estadísticas
│   ├── ingreso/              # Nueva licitación
│   ├── gestion/              # Listado de licitaciones
│   ├── metricas/             # Análisis y reportes
│   ├── documentacion/        # Documentación del sistema
│   ├── ayuda/                # Centro de ayuda
│   ├── polizas/              # Gestión de pólizas
│   ├── presupuesto/          # Generación de presupuestos
│   ├── editar-licitacion/    # Edición de licitaciones
│   ├── resultado-licitacion/ # Resultados y adjudicación
│   └── login/                # Autenticación
└── shared/                    # Recursos compartidos
    ├── components/           # Templates HTML reutilizables
    ├── css/                  # Estilos globales
    ├── img/                  # Imágenes
    ├── js/                   # JavaScript compartido
    │   ├── index.js         # Exports centralizados
    │   ├── config.js        # Rutas API
    │   ├── validators.js    # Validaciones
    │   ├── theme.js         # Tema claro/oscuro
    │   ├── modales.js       # Gestión de modales
    │   └── template-loader.js
    └── base.html            # Template base
```

## Principios

### 1. Cada módulo es autónomo
- Contiene su HTML, JS y submódulos relacionados
- Fácil de localizar y mantener
- README propio con documentación

### 2. Recursos compartidos centralizados
- `shared/` contiene todo lo reutilizable
- Evita duplicación de código
- Utilidades comunes accesibles desde cualquier módulo

### 3. Rutas actualizadas
- Backend sirve desde `modules/`
- Componentes accesibles desde `/shared/components/`
- Static files desde `/shared/`

## Uso

### Importar utilidades compartidas
```javascript
import { API_ROUTES, Utils, Validators } from '/shared/js/index.js';

// Usar rutas API
const response = await fetch(API_ROUTES.clientes);

// Formatear moneda
const precio = Utils.formatCurrency(1500000); // "$1.50 MILL"

// Mostrar notificación
Utils.showNotification('Guardado exitoso', 'success');
```

### Validar formularios
```javascript
import { validateForm, ErrorMessages } from '/shared/js/validators.js';

const result = validateForm('clienteForm', {
  clienteNombre: [
    { validator: 'required', message: ErrorMessages.required },
    { validator: 'minLength', message: ErrorMessages.minLength(3), params: [3] }
  ],
  clienteEmail: [
    { validator: 'email', message: ErrorMessages.email }
  ],
  clienteCuit: [
    { validator: 'cuit', message: ErrorMessages.cuit }
  ]
});

if (!result.valid) {
  console.log('Errores:', result.errors);
}
```

### Agregar nuevo módulo
1. Crear carpeta en `modules/nombre-modulo/`
2. Agregar `nombre-modulo.html` y `nombre-modulo.js`
3. Crear `README.md` documentando el módulo
4. Actualizar ruta en `backend/app.py`
5. Agregar enlace en `shared/base.html` (sidebar)

### Agregar componente compartido
1. Crear en `shared/components/nombre-componente.html`
2. Usar desde cualquier módulo con `template-loader.js`

## Características

### ✅ Validaciones centralizadas
- Email, CUIT, teléfono
- Campos requeridos
- Rangos numéricos
- Fechas
- Longitud de texto

### ✅ Utilidades comunes
- Formateo de moneda
- Formateo de fechas
- Debounce para búsquedas
- Notificaciones toast
- Fetch con manejo de errores

### ✅ Configuración centralizada
- Todas las rutas API en un solo archivo
- Fácil mantenimiento
- Autocompletado en IDE

### ✅ Documentación por módulo
- Cada módulo tiene su README
- Describe funcionalidades
- Lista dependencias
- Documenta API endpoints

## Convenciones

### Nombres de archivos
- HTML: `nombre-modulo.html`
- JS: `nombre-modulo.js`
- CSS (opcional): `nombre-modulo.css`

### Estructura de módulo
```
modulo/
├── README.md              # Documentación
├── modulo.html           # Vista
├── modulo.js             # Lógica principal
├── modulo.css (opcional) # Estilos específicos
└── submodulos/           # Submódulos si es necesario
```

### Imports
```javascript
// Utilidades compartidas
import { Utils, API_ROUTES } from '/shared/js/index.js';

// Submódulos relativos
import { funcion } from './submodulo/archivo.js';
```

## Migración desde estructura anterior

✅ **Completado:**
- Archivos HTML movidos a `modules/`
- Archivos JS movidos con sus módulos
- Recursos compartidos en `shared/`
- Rutas actualizadas en backend
- Templates base actualizados
- Validaciones centralizadas creadas
- Configuración de rutas creada
- Documentación por módulo creada
