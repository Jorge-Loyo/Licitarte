-- Migración 002: Catálogos configurables
-- Versión: 1.1.0
-- Fecha: 2025-01-26

CREATE TABLE IF NOT EXISTS portales_origen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS modalidades_entrega (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS formas_pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS motivos_perdida (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS mantenimientos_oferta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

-- Datos por defecto
INSERT OR IGNORE INTO portales_origen (nombre) VALUES ('Comprar'), ('BAC'), ('Otro');
INSERT OR IGNORE INTO modalidades_entrega (nombre) VALUES ('Única'), ('Múltiple'), ('Programada');
INSERT OR IGNORE INTO formas_pago (nombre) VALUES ('Contado'), ('30 días'), ('60 días');
INSERT OR IGNORE INTO organismos_jurisdiccion (nombre) VALUES ('Nacional'), ('Provincial'), ('Municipal'), ('CABA'), ('Privado');
INSERT OR IGNORE INTO motivos_perdida (nombre) VALUES ('Precio más alto'), ('Marca no priorizada'), ('No cumplía especificación'), ('Error administrativo'), ('Otro');
