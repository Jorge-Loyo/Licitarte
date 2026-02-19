@echo off
echo Agregando columna porcentaje_poliza...
echo.

cd web
py -c "import os; import psycopg; from urllib.parse import urlparse; db_url = os.getenv('DATABASE_URL'); result = urlparse(db_url); conn = psycopg.connect(dbname=result.path[1:], user=result.username, password=result.password, host=result.hostname, port=result.port); cursor = conn.cursor(); cursor.execute('ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS porcentaje_poliza REAL'); conn.commit(); print('Columna agregada exitosamente'); cursor.close(); conn.close()"

echo.
echo Listo! Reinicia la aplicacion.
pause
