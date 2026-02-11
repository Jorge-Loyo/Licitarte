#!/usr/bin/env python
"""Script para inicializar la base de datos en Render"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def init_db():
    print("Inicializando base de datos...")
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            # Crear tabla usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    activo BOOLEAN DEFAULT TRUE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insertar usuario admin (password: admin123)
            cursor.execute("""
                INSERT INTO usuarios (username, email, password_hash) 
                VALUES ('admin', 'admin@licitarte.com', 'scrypt:32768:8:1$xQzKjYvN8fGHLmPq$8a9b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f')
                ON CONFLICT (username) DO NOTHING
            """)
            
            # Crear tablas básicas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT UNIQUE NOT NULL,
                    razon_social TEXT,
                    cuit TEXT,
                    direccion TEXT,
                    telefono TEXT,
                    email TEXT,
                    organismo_jurisdiccion TEXT,
                    activo BOOLEAN DEFAULT TRUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tipos_licitacion (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT UNIQUE NOT NULL,
                    activo BOOLEAN DEFAULT TRUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS licitaciones (
                    id SERIAL PRIMARY KEY,
                    numero_licitacion TEXT UNIQUE NOT NULL,
                    cliente_id INTEGER REFERENCES clientes(id),
                    tipo_licitacion_id INTEGER REFERENCES tipos_licitacion(id),
                    fecha DATE NOT NULL,
                    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    oferente_ganador TEXT,
                    marca_ganadora TEXT,
                    precio_ganador REAL,
                    portal_origen TEXT,
                    modalidad_entrega TEXT,
                    forma_pago TEXT,
                    requiere_poliza BOOLEAN DEFAULT FALSE,
                    monto_poliza REAL,
                    observaciones TEXT,
                    mantenimiento_oferta TEXT,
                    numero_presupuesto INTEGER,
                    tipo_adjudicacion TEXT DEFAULT 'Parcial'
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id SERIAL PRIMARY KEY,
                    licitacion_id INTEGER NOT NULL REFERENCES licitaciones(id) ON DELETE CASCADE,
                    monodroga TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    presentacion TEXT NOT NULL,
                    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                    precio_ofertado REAL NOT NULL CHECK(precio_ofertado >= 0),
                    resultado TEXT NOT NULL CHECK(resultado IN ('Adjudicado', 'Parcial', 'No Adjudicado')),
                    precio_ganador REAL CHECK(precio_ganador >= 0),
                    oferente_ganador TEXT,
                    marca_ofrecida TEXT,
                    marca_ganadora TEXT,
                    motivo_perdida TEXT,
                    numero_renglon TEXT,
                    costo_unitario REAL,
                    margen_porcentaje REAL,
                    observaciones TEXT,
                    producto_cotizar TEXT DEFAULT 'principal'
                )
            """)
            
            conn.commit()
            print("✅ Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db()
