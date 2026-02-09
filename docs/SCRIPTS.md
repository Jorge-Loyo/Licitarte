# Scripts de Utilidad - Licitarte

## Scripts Disponibles

### Raíz del Proyecto

#### `start.bat`
Inicia la aplicación web verificando que PostgreSQL Docker esté corriendo.
```bash
start.bat
```

#### `run_web.bat`
Instala dependencias e inicia el servidor Flask directamente.
```bash
run_web.bat
```

#### `migrate.bat`
Ejecuta las migraciones de base de datos.
```bash
migrate.bat
```

### Desktop

#### `desktop/build_exe.bat`
Genera el ejecutable de la aplicación desktop con PyInstaller.
```bash
cd desktop
build_exe.bat
```

## Uso Recomendado

**Para desarrollo web:**
1. Asegúrate de que Docker esté corriendo
2. Ejecuta `start.bat` para iniciar la aplicación

**Para migraciones:**
1. Ejecuta `migrate.bat` cuando necesites actualizar el esquema de BD

**Para generar ejecutable desktop:**
1. Ve a la carpeta `desktop/`
2. Ejecuta `build_exe.bat`
