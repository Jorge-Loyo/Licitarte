@echo off
echo Importando datos a Render PostgreSQL...
echo.
echo IMPORTANTE: Necesitas la DATABASE_URL de Render
echo Formato: postgresql://user:password@host:port/database
echo.
set /p DATABASE_URL="Pega aqui la DATABASE_URL de Render: "
echo.
echo Importando...
psql "%DATABASE_URL%" < export_medicamentos.sql
echo.
echo Listo!
pause
