# 📦 GUÍA DE DISTRIBUCIÓN - LICITARTE

## 🔨 CREAR EJECUTABLE

### Paso 1: Generar el ejecutable

Ejecuta el archivo:
```
build_exe.bat
```

Esto creará:
- `dist/Licitarte.exe` - Ejecutable principal
- `dist/_internal/` - Archivos necesarios

### Paso 2: Verificar

El ejecutable estará en la carpeta `dist/`

---

## 📤 PREPARAR PARA DISTRIBUCIÓN

### Opción 1: Carpeta Portable (Recomendado)

1. **Copiar contenido de `dist/` a una nueva carpeta:**
   ```
   Licitarte_v1.0_Portable/
   ├── Licitarte.exe
   ├── _internal/
   ├── Img/
   └── LEEME.txt
   ```

2. **Crear archivo LEEME.txt:**
   ```
   LICITARTE v1.0 - Versión Portable
   
   INSTRUCCIONES:
   1. Ejecutar Licitarte.exe
   2. La base de datos se creará automáticamente
   3. No requiere instalación
   
   REQUISITOS:
   - Windows 10/11
   - No requiere Python instalado
   ```

3. **Comprimir en ZIP:**
   - Clic derecho en la carpeta
   - Enviar a > Carpeta comprimida
   - Nombre: `Licitarte_v1.0_Portable.zip`

---

### Opción 2: Instalador

1. **Copiar archivos necesarios:**
   ```
   Licitarte_Instalador/
   ├── Licitarte.exe
   ├── _internal/
   ├── Img/
   └── installer.bat
   ```

2. **Comprimir en ZIP:**
   - Nombre: `Licitarte_v1.0_Instalador.zip`

3. **Instrucciones para el usuario:**
   - Descomprimir el ZIP
   - Clic derecho en `installer.bat`
   - Ejecutar como administrador
   - Seguir instrucciones en pantalla

---

## 📋 CHECKLIST DE DISTRIBUCIÓN

Antes de distribuir, verificar:

- [ ] El ejecutable abre correctamente
- [ ] El logo se muestra
- [ ] Se puede crear una licitación
- [ ] Se puede editar y eliminar
- [ ] El dashboard muestra estadísticas
- [ ] El cambio de tema funciona
- [ ] La base de datos se crea automáticamente
- [ ] No hay errores en consola

---

## 🎯 MÉTODOS DE DISTRIBUCIÓN

### 1. Email
- Adjuntar el ZIP (tamaño aprox. 30-50 MB)
- Incluir instrucciones básicas

### 2. Google Drive / OneDrive
- Subir el ZIP
- Compartir enlace

### 3. USB
- Copiar carpeta portable directamente
- Usuario puede ejecutar sin instalar

### 4. Servidor Web
- Subir a servidor
- Proporcionar enlace de descarga

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No se encuentra el archivo"
**Solución:** Asegurarse de copiar toda la carpeta `_internal/`

### Error: "Falta DLL"
**Solución:** Incluir Visual C++ Redistributable en la distribución

### El logo no aparece
**Solución:** Verificar que la carpeta `Img/` esté incluida

---

## 📊 TAMAÑOS APROXIMADOS

- Ejecutable solo: ~15 MB
- Con dependencias (_internal): ~40 MB
- ZIP completo: ~25 MB (comprimido)

---

## 🔄 ACTUALIZAR VERSIÓN

Para crear nueva versión:

1. Modificar código fuente
2. Actualizar número de versión en `main.py`
3. Ejecutar `build_exe.bat`
4. Crear nuevo ZIP con nuevo número de versión
5. Distribuir

---

## 📝 NOTAS IMPORTANTES

- ✅ El ejecutable NO requiere Python instalado
- ✅ Funciona en Windows 10/11 (64-bit)
- ✅ La base de datos se crea automáticamente
- ✅ Es portable (no modifica el registro)
- ⚠️ Antivirus puede dar falso positivo (normal con PyInstaller)
- ⚠️ Primera ejecución puede tardar unos segundos

---

## 🛡️ FIRMA DIGITAL (Opcional)

Para evitar advertencias de Windows:

1. Obtener certificado de firma de código
2. Firmar el ejecutable:
   ```
   signtool sign /f certificado.pfx /p password Licitarte.exe
   ```

---

## 📞 SOPORTE

Si los usuarios reportan problemas:

1. Verificar versión de Windows
2. Verificar permisos de escritura
3. Verificar antivirus no bloquea
4. Solicitar captura de pantalla del error
