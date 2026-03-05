# Módulo Login

## Descripción
Autenticación de usuarios en el sistema.

## Archivos
- `login.html` - Formulario de login

## Funcionalidades
- ✅ Login con usuario/contraseña
- ✅ Recordar sesión
- ✅ Recuperar contraseña
- ✅ Validación de credenciales

## Seguridad
- Contraseñas hasheadas
- Sesiones con Flask-Login
- Rate limiting
- CSRF protection

## API Endpoints
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `POST /api/auth/reset-password`
