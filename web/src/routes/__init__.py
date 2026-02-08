"""Rutas de la aplicación"""
from flask import Blueprint

def register_routes(app):
    """Registra todos los blueprints de rutas"""
    from .licitaciones import bp as licitaciones_bp
    from .productos import bp as productos_bp
    from .catalogos import bp as catalogos_bp
    from .estadisticas import bp as estadisticas_bp
    
    app.register_blueprint(licitaciones_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(estadisticas_bp)
