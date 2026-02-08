-- Migración 003: Usuarios y autenticación
-- Versión: 1.3.0
-- Fecha: 2025-02-08

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    activo INTEGER DEFAULT 1,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Usuario admin por defecto (password: admin123)
INSERT OR IGNORE INTO usuarios (username, email, password_hash) 
VALUES ('admin', 'admin@licitarte.com', 'scrypt:32768:8:1$xQzKjYvN8fGHLmPq$8a9b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f');
