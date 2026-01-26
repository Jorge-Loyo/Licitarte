"""
Script para migrar datos de la base antigua a la nueva
"""
import sqlite3
import shutil
import os

# Rutas
db_vieja = 'licitaciones_backup.db'
db_nueva = 'licitaciones.db'

# Hacer backup de la nueva
shutil.copy(db_nueva, 'licitaciones_nueva_backup.db')

print("=== MIGRANDO DATOS ===\n")

# Conectar a ambas bases
conn_vieja = sqlite3.connect(db_vieja)
conn_nueva = sqlite3.connect(db_nueva)

cursor_vieja = conn_vieja.cursor()
cursor_nueva = conn_nueva.cursor()

# Migrar clientes
print("1. Migrando clientes...")
cursor_vieja.execute("SELECT * FROM clientes")
clientes = cursor_vieja.fetchall()
for c in clientes:
    try:
        cursor_nueva.execute("INSERT OR IGNORE INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           c + (None, None, None) if len(c) == 8 else c)
    except:
        pass
print(f"   {len(clientes)} clientes migrados")

# Migrar oferentes
print("2. Migrando oferentes...")
cursor_vieja.execute("SELECT * FROM oferentes")
oferentes = cursor_vieja.fetchall()
for o in oferentes:
    try:
        cursor_nueva.execute("INSERT OR IGNORE INTO oferentes VALUES (?, ?, ?)", o)
    except:
        pass
print(f"   {len(oferentes)} oferentes migrados")

# Migrar marcas
print("3. Migrando marcas...")
cursor_vieja.execute("SELECT * FROM marcas")
marcas = cursor_vieja.fetchall()
for m in marcas:
    try:
        cursor_nueva.execute("INSERT OR IGNORE INTO marcas VALUES (?, ?, ?)", m)
    except:
        pass
print(f"   {len(marcas)} marcas migradas")

# Migrar tipos_licitacion
print("4. Migrando tipos de licitación...")
cursor_vieja.execute("SELECT * FROM tipos_licitacion")
tipos = cursor_vieja.fetchall()
for t in tipos:
    try:
        cursor_nueva.execute("INSERT OR IGNORE INTO tipos_licitacion VALUES (?, ?, ?)", t)
    except:
        pass
print(f"   {len(tipos)} tipos migrados")

# Migrar licitaciones
print("5. Migrando licitaciones...")
cursor_vieja.execute("SELECT * FROM licitaciones")
licitaciones = cursor_vieja.fetchall()
for l in licitaciones:
    try:
        # Agregar campos nuevos con valores NULL
        valores = list(l) + [None, None, None, False, None, None]
        cursor_nueva.execute("INSERT OR IGNORE INTO licitaciones VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           valores[:14])
    except Exception as e:
        print(f"   Error en licitación {l[0]}: {e}")
print(f"   {len(licitaciones)} licitaciones migradas")

# Migrar productos
print("6. Migrando productos...")
cursor_vieja.execute("SELECT * FROM productos")
productos = cursor_vieja.fetchall()
for p in productos:
    try:
        # Agregar campos nuevos con valores NULL
        valores = list(p) + [None] * 11  # Agregar 11 campos nuevos
        cursor_nueva.execute("INSERT OR IGNORE INTO productos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           valores[:23])
    except Exception as e:
        print(f"   Error en producto {p[0]}: {e}")
print(f"   {len(productos)} productos migrados")

# Migrar catálogo celty
print("7. Migrando catálogo...")
cursor_vieja.execute("SELECT * FROM celty")
catalogo = cursor_vieja.fetchall()
for c in catalogo:
    try:
        valores = list(c) + [None] if len(c) == 9 else c
        cursor_nueva.execute("INSERT OR IGNORE INTO celty VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           valores[:10])
    except:
        pass
print(f"   {len(catalogo)} productos del catálogo migrados")

# Guardar cambios
conn_nueva.commit()
conn_vieja.close()
conn_nueva.close()

print("\n=== MIGRACIÓN COMPLETADA ===")
print("\nBackup de la nueva base guardado en: licitaciones_nueva_backup.db")
