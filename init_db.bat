@echo off
echo ========================================
echo   INICIALIZAR BASE DE DATOS POSTGRESQL
echo ========================================
echo.

echo [1/2] Ejecutando migraciones...
cd shared\database
python run_migrations.py

echo.
echo [2/2] Creando usuario admin...
cd ..\..\web
python migrate_usuarios.py

echo.
echo ========================================
echo   BASE DE DATOS INICIALIZADA
echo ========================================
echo.
echo Credenciales admin:
echo   Usuario: admin
echo   Password: admin123
echo.
echo Ahora ejecuta:
echo   python app.py
echo.
pause
