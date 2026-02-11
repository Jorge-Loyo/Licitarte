-- Migración 001: Schema inicial de Licitarte
-- Versión: 1.0.0
-- Fecha: 2025-01-15

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    razon_social TEXT,
    cuit TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    organismo_jurisdiccion TEXT,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS tipos_licitacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS licitaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_licitacion TEXT UNIQUE NOT NULL,
    cliente_id INTEGER,
    tipo_licitacion_id INTEGER,
    fecha TEXT NOT NULL,
    fecha_carga TEXT DEFAULT CURRENT_TIMESTAMP,
    oferente_ganador TEXT,
    marca_ganadora TEXT,
    precio_ganador REAL,
    portal_origen TEXT,
    modalidad_entrega TEXT,
    forma_pago TEXT,
    requiere_poliza INTEGER DEFAULT 0,
    monto_poliza REAL,
    observaciones TEXT,
    mantenimiento_oferta TEXT,
    numero_presupuesto INTEGER,
    tipo_adjudicacion TEXT DEFAULT 'Parcial',
    CHECK(length(numero_licitacion) > 0),
    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
    FOREIGN KEY (tipo_licitacion_id) REFERENCES tipos_licitacion (id)
);

CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    licitacion_id INTEGER NOT NULL,
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
    producto_cotizar TEXT DEFAULT 'principal',
    FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_licitacion_numero ON licitaciones(numero_licitacion);
CREATE INDEX IF NOT EXISTS idx_licitacion_cliente ON licitaciones(cliente_id);
CREATE INDEX IF NOT EXISTS idx_producto_licitacion ON productos(licitacion_id);
CREATE INDEX IF NOT EXISTS idx_producto_resultado ON productos(resultado);
