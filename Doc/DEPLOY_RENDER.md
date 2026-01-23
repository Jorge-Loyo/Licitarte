# 🚀 GUÍA DE DESPLIEGUE EN RENDER

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Repositorio Git (GitHub, GitLab o Bitbucket)
- Código de Licitarte Web

---

## 🔧 Preparación del Proyecto

### 1. Estructura de Archivos

Asegúrate de tener:
```
Licitarte/
├── web/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
├── database/
│   └── db_manager.py
├── Procfile
└── runtime.txt
```

### 2. Verificar Archivos de Configuración

**Procfile:**
```
web: cd web && gunicorn app:app
```

**runtime.txt:**
```
python-3.11.0
```

**web/requirements.txt:**
```
Flask==3.0.0
gunicorn==21.2.0
```

---

## 📤 Subir a GitHub

### 1. Inicializar Repositorio

```bash
cd C:\git\Licitarte
git init
git add .
git commit -m "Initial commit - Licitarte Web"
```

### 2. Crear Repositorio en GitHub

1. Ir a https://github.com/new
2. Nombre: `licitarte-web`
3. Descripción: "Aplicación web para gestión de licitaciones farmacéuticas"
4. Público o Privado (según preferencia)
5. Crear repositorio

### 3. Conectar y Subir

```bash
git remote add origin https://github.com/TU_USUARIO/licitarte-web.git
git branch -M main
git push -u origin main
```

---

## 🌐 Desplegar en Render

### Paso 1: Crear Nuevo Web Service

1. Ir a https://dashboard.render.com
2. Clic en "New +"
3. Seleccionar "Web Service"

### Paso 2: Conectar Repositorio

1. Conectar tu cuenta de GitHub
2. Seleccionar repositorio `licitarte-web`
3. Clic en "Connect"

### Paso 3: Configurar el Servicio

**Configuración Básica:**
- **Name:** `licitarte-web`
- **Region:** Seleccionar más cercana (ej: Oregon, USA)
- **Branch:** `main`
- **Root Directory:** (dejar vacío)
- **Runtime:** Python 3
- **Build Command:** `pip install -r web/requirements.txt`
- **Start Command:** `cd web && gunicorn app:app`

**Plan:**
- Seleccionar "Free" (para pruebas)
- O "Starter" ($7/mes) para producción

### Paso 4: Variables de Entorno (Opcional)

Si necesitas configurar variables:
- Clic en "Advanced"
- Agregar variables de entorno:
  - `PYTHON_VERSION`: `3.11.0`
  - `SECRET_KEY`: (generar clave segura)

### Paso 5: Desplegar

1. Clic en "Create Web Service"
2. Render comenzará a construir y desplegar
3. Esperar 5-10 minutos

---

## ✅ Verificar Despliegue

### 1. Estado del Servicio

En el dashboard de Render verás:
- 🟢 **Live** - Servicio funcionando
- 🔴 **Failed** - Error en despliegue
- 🟡 **Building** - Construyendo

### 2. URL de la Aplicación

Tu aplicación estará disponible en:
```
https://licitarte-web.onrender.com
```

### 3. Probar Funcionalidades

- ✅ Dashboard carga correctamente
- ✅ Crear nueva licitación
- ✅ Ver gestión
- ✅ Cambiar tema claro/oscuro

---

## 🔧 Solución de Problemas

### Error: "Application failed to start"

**Solución:**
1. Verificar logs en Render Dashboard
2. Revisar que `Procfile` esté correcto
3. Verificar `requirements.txt`

### Error: "Module not found"

**Solución:**
```bash
# Actualizar requirements.txt
pip freeze > web/requirements.txt
git add .
git commit -m "Update requirements"
git push
```

### Base de Datos No Persiste

**Problema:** Render Free tier no persiste archivos

**Solución:**
1. Usar PostgreSQL de Render (gratis)
2. O actualizar a plan Starter
3. O usar servicio externo de BD

---

## 🔄 Actualizar la Aplicación

### 1. Hacer Cambios Localmente

```bash
# Editar archivos
# Probar localmente
python web/app.py
```

### 2. Subir Cambios

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

### 3. Despliegue Automático

Render detectará los cambios y redesplegar automáticamente.

---

## 📊 Monitoreo

### Logs en Tiempo Real

En Render Dashboard:
1. Seleccionar tu servicio
2. Ir a "Logs"
3. Ver logs en tiempo real

### Métricas

- CPU Usage
- Memory Usage
- Request Count
- Response Time

---

## 💾 Base de Datos en Producción

### Opción 1: PostgreSQL en Render (Recomendado)

1. Crear PostgreSQL Database en Render
2. Obtener URL de conexión
3. Actualizar `db_manager.py` para usar PostgreSQL
4. Instalar `psycopg2`:
   ```
   pip install psycopg2-binary
   ```

### Opción 2: SQLite con Volumen Persistente

1. Actualizar a plan Starter
2. Configurar disco persistente
3. Montar en `/opt/render/project/database`

---

## 🔒 Seguridad

### 1. Variables de Entorno

Nunca subir claves secretas al repositorio:
```python
# En app.py
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
```

### 2. HTTPS

Render proporciona HTTPS automáticamente.

### 3. Dominio Personalizado (Opcional)

1. Ir a Settings > Custom Domain
2. Agregar tu dominio
3. Configurar DNS según instrucciones

---

## 💰 Costos

### Plan Free
- ✅ Gratis
- ⚠️ Se duerme después de 15 min de inactividad
- ⚠️ 750 horas/mes
- ⚠️ No persiste archivos

### Plan Starter ($7/mes)
- ✅ Siempre activo
- ✅ Disco persistente
- ✅ Mejor rendimiento

---

## 📝 Comandos Útiles

### Ejecutar Localmente

```bash
cd C:\git\Licitarte\web
python app.py
# Abrir: http://localhost:5000
```

### Ver Logs de Render

```bash
# Desde Render CLI (opcional)
render logs -s licitarte-web
```

### Reiniciar Servicio

En Render Dashboard:
1. Manual Deploy > Clear build cache & deploy

---

## 🎯 Checklist de Despliegue

- [ ] Código subido a GitHub
- [ ] Procfile configurado
- [ ] requirements.txt actualizado
- [ ] Servicio creado en Render
- [ ] Build exitoso
- [ ] Aplicación accesible
- [ ] Todas las funciones probadas
- [ ] Base de datos funcionando
- [ ] Tema claro/oscuro funciona
- [ ] Responsive en móvil

---

## 📞 Soporte

**Documentación Render:**
https://render.com/docs

**Comunidad:**
https://community.render.com

---

## 🎉 ¡Listo!

Tu aplicación Licitarte ahora está en línea y accesible desde cualquier lugar.

**URL:** https://licitarte-web.onrender.com

**Comparte el enlace con tus usuarios.**
