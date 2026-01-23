# 🚀 Licitarte v1.0.0 - Inicio Rápido

## ⚡ Instalación en 5 Minutos

### 1️⃣ Clonar Repositorio
```bash
git clone https://github.com/Jorge-Loyo/Licitarte.git
cd Licitarte
```

### 2️⃣ Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3️⃣ Instalar Dependencias
```bash
cd web
pip install -r requirements.txt
```

### 4️⃣ Ejecutar Aplicación
```bash
python app.py
```

### 5️⃣ Abrir Navegador
```
http://localhost:5000
```

---

## 🎯 Primeros Pasos

### 1. Crear un Cliente
1. Ir a **Administración**
2. Tab **Clientes**
3. Clic en **+ Nuevo Cliente**
4. Completar datos y guardar

### 2. Crear una Licitación
1. Ir a **Nueva Licitación**
2. Seleccionar cliente
3. Completar N° y fecha
4. Agregar productos
5. Guardar

### 3. Ver Resultados
1. Ir a **Gestión** para ver licitaciones
2. Ir a **Dashboard** para ver estadísticas

---

## 📚 Documentación

- [README.md](README.md) - Documentación completa
- [INSTALL.md](INSTALL.md) - Guía de instalación detallada
- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios
- [Ayuda en la app] - Manual de usuario integrado

---

## 🆘 Ayuda Rápida

### Problema: Puerto 5000 ocupado
```bash
# Cambiar puerto
set PORT=5001  # Windows
python app.py
```

### Problema: Módulo no encontrado
```bash
pip install -r requirements.txt
```

### Problema: Base de datos
```bash
# Verificar carpeta database existe
mkdir database
```

---

## 🌐 Despliegue a Producción

Ver [DEPLOY.md](Doc/DEPLOY.md) para instrucciones completas.

**Resumen**:
1. Crear cuenta en Render.com
2. Crear PostgreSQL Database
3. Crear Web Service
4. Configurar variables de entorno
5. Desplegar

---

## ✅ Versión 1.0.0

**Estado**: ✅ Producción Ready  
**Fecha**: Enero 2025  
**Autor**: Jorge

---

**¡Listo para usar!** 🎉
