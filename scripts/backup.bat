@echo off
echo Creando backup de la base de datos...
set FECHA=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set FECHA=%FECHA: =0%
docker exec licitarte-postgres pg_dump -U licitarte licitarte_db > Data\backups\backup_%FECHA%.sql
echo Backup creado: Data\backups\backup_%FECHA%.sql
pause
