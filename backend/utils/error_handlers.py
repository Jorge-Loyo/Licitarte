"""Manejadores de errores centralizados"""
from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from backend.utils.logging_config import logger

def register_error_handlers(app):
    """Registrar manejadores de errores"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Errores de validación Pydantic"""
        logger.warning(f"Validation error: {e.errors()}", extra={
            'endpoint': request.endpoint,
            'method': request.method,
            'url': request.url
        })
        return jsonify({
            'success': False,
            'error': 'Datos inválidos',
            'details': e.errors()
        }), 400
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """Bad Request"""
        logger.warning(f"Bad request: {e}", extra={
            'endpoint': request.endpoint,
            'url': request.url
        })
        return jsonify({
            'success': False,
            'error': 'Solicitud inválida'
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(e):
        """No autorizado"""
        logger.warning(f"Unauthorized access: {request.url}")
        return jsonify({
            'success': False,
            'error': 'No autorizado'
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(e):
        """Prohibido"""
        logger.warning(f"Forbidden access: {request.url}")
        return jsonify({
            'success': False,
            'error': 'Acceso prohibido'
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """No encontrado"""
        return jsonify({
            'success': False,
            'error': 'Recurso no encontrado'
        }), 404
    
    @app.errorhandler(429)
    def handle_rate_limit(e):
        """Rate limit excedido"""
        logger.warning(f"Rate limit exceeded: {request.remote_addr}")
        return jsonify({
            'success': False,
            'error': 'Demasiadas solicitudes. Intente más tarde.'
        }), 429
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """Error interno del servidor"""
        logger.error(f"Internal error: {e}", exc_info=True, extra={
            'endpoint': request.endpoint,
            'method': request.method,
            'url': request.url
        })
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Capturar todas las excepciones no manejadas"""
        if isinstance(e, HTTPException):
            return e
        
        logger.error(f"Unhandled exception: {e}", exc_info=True, extra={
            'endpoint': request.endpoint,
            'method': request.method,
            'url': request.url,
            'data': request.get_json(silent=True)
        })
        
        return jsonify({
            'success': False,
            'error': 'Error inesperado'
        }), 500
