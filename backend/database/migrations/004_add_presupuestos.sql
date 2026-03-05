-- Migración 004: Presupuestos y alternativas
-- Versión: 1.2.0
-- Fecha: 2025-01-30

CREATE TABLE IF NOT EXISTS presupuestos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    licitacion_id INTEGER NOT NULL,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (licitacion_id) REFERENCES licitaciones(id)
);

CREATE TABLE IF NOT EXISTS alternativas_productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    marca TEXT NOT NULL,
    presentacion TEXT NOT NULL,
    laboratorio TEXT,
    costo_unitario REAL,
    margen_porcentaje REAL,
    precio_ofertado REAL,
    observaciones TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ofertas_productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    oferente TEXT NOT NULL,
    laboratorio TEXT NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);
