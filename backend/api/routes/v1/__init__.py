"""API v1 routes"""
from flask import Blueprint

def register_v1_routes(app):
    """Registra rutas API v1"""
    from ..auth import bp as auth_bp
    from ..licitaciones import bp as licitaciones_bp
    from ..productos import bp as productos_bp
    from ..catalogos import bp as catalogos_bp
    from ..estadisticas import bp as estadisticas_bp
    from ..catalogos_extra import bp as catalogos_extra_bp
    from ..extras import bp as extras_bp
    from ..uploads import bp as uploads_bp
    from ..health import bp as health_bp
    
    # Registrar con prefijo /api/v1 y nombres únicos
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth', name='auth_v1')
    app.register_blueprint(licitaciones_bp, url_prefix='/api/v1/licitaciones', name='licitaciones_v1')
    app.register_blueprint(productos_bp, url_prefix='/api/v1/productos', name='productos_v1')
    app.register_blueprint(catalogos_bp, url_prefix='/api/v1', name='catalogos_v1')
    app.register_blueprint(estadisticas_bp, url_prefix='/api/v1', name='estadisticas_v1')
    app.register_blueprint(catalogos_extra_bp, url_prefix='/api/v1', name='catalogos_extra_v1')
    app.register_blueprint(extras_bp, url_prefix='/api/v1', name='extras_v1')
    app.register_blueprint(uploads_bp, url_prefix='/api/v1', name='uploads_v1')
    app.register_blueprint(health_bp, url_prefix='/api/v1', name='health_v1')
