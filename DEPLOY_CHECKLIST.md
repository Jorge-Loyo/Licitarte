# ✅ CHECKLIST PARA DEPLOY A PRODUCCIÓN

## 🚨 CRÍTICO - Hacer ANTES de commit

### 1. Seguridad
- [ ] **REGENERAR SECRET_KEY** - La actual está comprometida en git
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- [ ] Configurar SECRET_KEY en Render como variable de entorno
- [ ] Verificar que `web/.env` NO está en git: `git status`
- [ ] Confirmar `.gitignore` actualizado

### 2. Base de Datos
- [ ] Configurar PostgreSQL en Render (automático)
- [ ] Agregar `psycopg2-binary` a requirements.txt para producción
- [ ] Verificar que migraciones funcionan con PostgreSQL
- [ ] Backup de datos SQLite si hay datos importantes

### 3. Configuración Render
- [ ] Crear cuenta en Render.com
- [ ] Conectar repositorio GitHub
- [ ] Configurar variables de entorno:
  ```
  SECRET_KEY=<nueva_clave_generada>
  FLASK_ENV=production
  DATABASE_URL=<render_lo_configura_automaticamente>
  ```
- [ ] Build Command: `pip install -r web/requirements.txt`
- [ ] Start Command: `cd web && gunicorn app:app`

### 4. Testing
- [ ] Ejecutar tests localmente: `pytest`
- [ ] Verificar cobertura: `pytest --cov`
- [ ] Probar endpoints críticos manualmente
- [ ] Verificar que app inicia: `python web/app.py`

### 5. Documentación
- [ ] README actualizado con instrucciones de deploy
- [ ] Variables de entorno documentadas
- [ ] Proceso de migraciones documentado

---

## 📋 COMANDOS PARA DEPLOY

### Preparar Repositorio
```bash
# 1. Actualizar .gitignore
git add .gitignore

# 2. Agregar archivos nuevos (SIN .env)
git add Doc/ database/migrations/ web/config.py web/schemas/ web/tests/ web/utils/
git add web/.env.example web/pytest.ini web/requirements.txt

# 3. Agregar cambios en archivos existentes
git add web/app.py database/db_manager.py

# 4. Commit
git commit -m "feat: Implementar fundamentos para producción

- Configuración por entornos (dev/prod)
- Sistema de logging con rotación
- Migraciones versionadas
- Validaciones Pydantic
- Tests con pytest (28% coverage)
- Corrección HTTP status codes (100% compliance)
- Preparado para PostgreSQL en producción"

# 5. Push
git push origin main
```

### Configurar en Render
1. Ir a https://render.com
2. New → Web Service
3. Conectar repositorio
4. Configurar:
   - **Name:** licitarte
   - **Environment:** Python 3
   - **Build Command:** `pip install -r web/requirements.txt`
   - **Start Command:** `cd web && gunicorn app:app`
5. Agregar PostgreSQL (automático)
6. Variables de entorno:
   - `SECRET_KEY`: <nueva_clave>
   - `FLASK_ENV`: production
7. Deploy

---

## ⚠️ PROBLEMAS CONOCIDOS A RESOLVER

### 1. PostgreSQL vs SQLite
**Problema:** Código usa SQLite en desarrollo, PostgreSQL en producción
**Solución:** Ya implementado en `db_manager.py` con `USE_POSTGRES`

### 2. Migraciones
**Problema:** Sistema de migraciones manual
**Solución:** Ejecutar `python database/migrations/migrate.py` en primer deploy

### 3. Archivos Estáticos
**Problema:** Flask sirve estáticos en desarrollo
**Solución:** Render sirve automáticamente desde `/static`

### 4. Logs
**Problema:** Logs en archivo local
**Solución:** Render captura stdout/stderr automáticamente

---

## 🎯 DESPUÉS DEL DEPLOY

### Verificar
- [ ] App responde en URL de Render
- [ ] Base de datos PostgreSQL conectada
- [ ] Endpoints funcionan correctamente
- [ ] Logs visibles en Render dashboard
- [ ] No hay errores 500

### Monitoreo
- [ ] Configurar alertas en Render
- [ ] Revisar logs diariamente primera semana
- [ ] Monitorear uso de base de datos

### Siguiente Fase
- [ ] Implementar CI/CD con GitHub Actions
- [ ] Agregar más tests (objetivo 60%)
- [ ] Documentar API con Swagger
- [ ] Implementar rate limiting

---

## 🆘 ROLLBACK

Si algo falla:
```bash
# Revertir último commit
git revert HEAD
git push origin main

# O volver a versión anterior
git reset --hard <commit_anterior>
git push origin main --force
```

En Render:
- Manual Deploy → Seleccionar commit anterior

---

## 📞 SOPORTE

- Render Docs: https://render.com/docs
- Flask Deployment: https://flask.palletsprojects.com/en/3.0.x/deploying/
- PostgreSQL: https://www.postgresql.org/docs/

---

**IMPORTANTE:** NO hacer commit hasta completar checklist de seguridad
