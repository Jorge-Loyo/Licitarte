@echo off
echo ========================================
echo   LICITARTE WEB - Servidor Local
echo ========================================
echo.

cd web

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando servidor...
echo.
echo Aplicacion disponible en: http://localhost:5000
echo Presiona Ctrl+C para detener
echo.

python app.py
