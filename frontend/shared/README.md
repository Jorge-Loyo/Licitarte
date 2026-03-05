# Shared - Recursos Compartidos

## Descripción
Recursos reutilizables por todos los módulos del sistema.

## Estructura

### `/components`
Templates HTML reutilizables:
- `admin-catalogo-row-template.html`
- `admin-cliente-row-template.html`
- `admin-simple-row-template.html`
- `alternativa-item-template.html`
- `producto-item-template.html`

### `/css`
- `style.css` - Estilos globales del sistema

### `/img`
- `Logo_licitarte.png` - Logo de la aplicación

### `/js`
Utilidades JavaScript compartidas:
- `index.js` - Exports centralizados
- `config.js` - Configuración de rutas API
- `validators.js` - Validaciones de formularios
- `theme.js` - Gestión de tema claro/oscuro
- `modales.js` - Gestión de modales
- `template-loader.js` - Carga de templates HTML
- `shared/` - Utilidades adicionales

### `base.html`
Template base con:
- Estructura HTML común
- Sidebar de navegación
- Header
- Footer
- Scripts globales

## Uso

### Importar utilidades
```javascript
import { API_ROUTES, Utils, Validators } from '/shared/js/index.js';
```

### Usar validaciones
```javascript
import { validateForm, ErrorMessages } from '/shared/js/validators.js';

const result = validateForm('myForm', {
  email: [
    { validator: 'required', message: ErrorMessages.required },
    { validator: 'email', message: ErrorMessages.email }
  ]
});
```

### Usar rutas API
```javascript
import { API_ROUTES } from '/shared/js/config.js';

fetch(API_ROUTES.clientes)
  .then(res => res.json())
  .then(data => console.log(data));
```

### Formatear moneda
```javascript
import { Utils } from '/shared/js/index.js';

const formatted = Utils.formatCurrency(1500000); // "$1.50 MILL"
```
