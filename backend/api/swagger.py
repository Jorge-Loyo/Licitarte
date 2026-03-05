"""Configuración de Swagger/OpenAPI para documentación de API"""
from flask_swagger_ui import get_swaggerui_blueprint

# Configuración de Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

def setup_swagger(app):
    """Configura Swagger UI en la aplicación Flask"""
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Licitarte API",
            'docExpansion': 'list',
            'defaultModelsExpandDepth': 3
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Ruta para servir el JSON de Swagger
    @app.route('/api/swagger.json')
    def swagger_json():
        from flask import jsonify
        return jsonify(get_swagger_spec())

def get_swagger_spec():
    """Retorna la especificación OpenAPI 3.0"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Licitarte API",
            "description": "API para gestión de licitaciones farmacéuticas",
            "version": "1.0.0",
            "contact": {
                "name": "Licitarte",
                "email": "soporte@licitarte.com"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5000",
                "description": "Servidor de desarrollo"
            }
        ],
        "tags": [
            {"name": "Auth", "description": "Autenticación y sesiones"},
            {"name": "Licitaciones", "description": "Gestión de licitaciones"},
            {"name": "Productos", "description": "Productos de licitaciones"},
            {"name": "Catálogos", "description": "Catálogos maestros"},
            {"name": "Estadísticas", "description": "Métricas y reportes"}
        ],
        "paths": {
            "/api/auth/login": {
                "post": {
                    "tags": ["Auth"],
                    "summary": "Login de usuario",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["username", "password"],
                                    "properties": {
                                        "username": {"type": "string", "example": "admin"},
                                        "password": {"type": "string", "example": "password123"},
                                        "remember": {"type": "boolean", "default": False}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login exitoso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/LoginResponse"
                                    }
                                }
                            }
                        },
                        "401": {"description": "Credenciales inválidas"}
                    }
                }
            },
            "/api/licitaciones": {
                "get": {
                    "tags": ["Licitaciones"],
                    "summary": "Listar todas las licitaciones",
                    "security": [{"cookieAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Lista de licitaciones",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Licitacion"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Licitaciones"],
                    "summary": "Crear nueva licitación",
                    "security": [{"cookieAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LicitacionCreate"}
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Licitación creada"},
                        "400": {"description": "Datos inválidos"}
                    }
                }
            },
            "/api/clientes": {
                "get": {
                    "tags": ["Catálogos"],
                    "summary": "Listar clientes",
                    "security": [{"cookieAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Lista de clientes",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Cliente"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/estadisticas": {
                "get": {
                    "tags": ["Estadísticas"],
                    "summary": "Obtener estadísticas generales",
                    "security": [{"cookieAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Estadísticas del dashboard",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Estadisticas"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "cookieAuth": {
                    "type": "apiKey",
                    "in": "cookie",
                    "name": "session"
                }
            },
            "schemas": {
                "LoginResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "username": {"type": "string"},
                                        "email": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "Licitacion": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "numero": {"type": "string"},
                        "fecha": {"type": "string", "format": "date"},
                        "cliente": {"type": "string"},
                        "tipo_licitacion": {"type": "string"},
                        "total_cotizado": {"type": "number"},
                        "ganancia": {"type": "string"}
                    }
                },
                "LicitacionCreate": {
                    "type": "object",
                    "required": ["numero", "fecha"],
                    "properties": {
                        "numero": {"type": "string"},
                        "fecha": {"type": "string", "format": "date"},
                        "cliente_id": {"type": "integer"},
                        "tipo_licitacion_id": {"type": "integer"},
                        "productos": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ProductoCreate"}
                        }
                    }
                },
                "ProductoCreate": {
                    "type": "object",
                    "required": ["monodroga", "marca", "presentacion", "cantidad", "precio"],
                    "properties": {
                        "monodroga": {"type": "string"},
                        "marca": {"type": "string"},
                        "presentacion": {"type": "string"},
                        "cantidad": {"type": "integer", "minimum": 1},
                        "precio": {"type": "number", "minimum": 0}
                    }
                },
                "Cliente": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "nombre": {"type": "string"},
                        "razon_social": {"type": "string"},
                        "cuit": {"type": "string"},
                        "email": {"type": "string"}
                    }
                },
                "Estadisticas": {
                    "type": "object",
                    "properties": {
                        "unidades_cotizadas": {"type": "integer"},
                        "unidades_ganadas": {"type": "integer"},
                        "total_cotizado": {"type": "number"},
                        "total_ganado": {"type": "number"}
                    }
                }
            }
        }
    }
