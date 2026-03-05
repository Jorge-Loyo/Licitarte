"""Middleware para logging de requests"""
from flask import request, g
from time import time
import uuid
from backend.utils.logging_config import logger
from flask_login import current_user

def setup_request_logging(app):
    """Configurar logging de requests"""
    
    @app.before_request
    def before_request():
        """Antes de cada request"""
        g.start_time = time()
        g.request_id = str(uuid.uuid4())
        
        logger.info(f"Request started: {request.method} {request.path}", extra={
            'request_id': g.request_id,
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_id': current_user.id if current_user.is_authenticated else None
        })
    
    @app.after_request
    def after_request(response):
        """Después de cada request"""
        if hasattr(g, 'start_time'):
            elapsed = time() - g.start_time
            
            logger.info(f"Request completed: {request.method} {request.path}", extra={
                'request_id': g.request_id,
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'elapsed_ms': round(elapsed * 1000, 2),
                'user_id': current_user.id if current_user.is_authenticated else None
            })
        
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        
        return response
    
    @app.teardown_request
    def teardown_request(exception=None):
        """Al finalizar request"""
        if exception:
            logger.error(f"Request failed: {exception}", exc_info=True, extra={
                'request_id': g.request_id if hasattr(g, 'request_id') else None
            })
