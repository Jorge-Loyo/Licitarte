"""Rutas de la aplicación"""
from flask import Blueprint

def register_routes(app):
    """Registra todos los blueprints de rutas"""
    from .licitaciones import bp as licitaciones_bp
    from .productos import bp as productos_bp
    from .catalogos import bp as catalogos_bp
    from .estadisticas import bp as estadisticas_bp
    from .catalogos_extra import bp as catalogos_extra_bp
    from .extras import bp as extras_bp
    from .uploads import bp as uploads_bp
    
    app.register_blueprint(licitaciones_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(estadisticas_bp)
    app.register_blueprint(catalogos_extra_bp)
    app.register_blueprint(extras_bp)
    app.register_blueprint(uploads_bp)
