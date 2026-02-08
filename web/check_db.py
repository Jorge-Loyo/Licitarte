import sqlite3

conn = sqlite3.connect('../database/licitaciones.db')
cursor = conn.cursor()

# Ver estructura de la tabla
cursor.execute("PRAGMA table_info(productos)")
columns = cursor.fetchall()
print("Columnas de productos:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n" + "="*50 + "\n")

# Ver datos del producto 8
cursor.execute("SELECT * FROM productos WHERE id = 8")
row = cursor.fetchone()
print(f"Producto 8 completo:")
for i, col in enumerate(columns):
    print(f"  {col[1]}: {row[i] if row else 'N/A'}")

conn.close()
