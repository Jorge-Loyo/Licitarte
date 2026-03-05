@echo off
echo Iniciando Licitarte...
echo.

cd /d "%~dp0"

if not exist ".env" (
    echo Copiando .env.example a .env...
    copy .env.example .env
)

echo Activando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo "Base de datos ya existe en licitarte-postgres (puerto 5433)"

echo.
echo Iniciando aplicacion Flask...
cd backend
python app.py

pause
