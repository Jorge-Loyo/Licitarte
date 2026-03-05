"""Middleware de métricas de performance"""
from flask import request, g
from time import time
from collections import defaultdict
import threading

# Almacenamiento en memoria de métricas
_metrics = defaultdict(lambda: {'count': 0, 'total_time': 0, 'min_time': float('inf'), 'max_time': 0})
_lock = threading.Lock()

def setup_metrics(app):
    """Configura middleware de métricas"""
    
    @app.before_request
    def before_request():
        g.start_time = time()
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            elapsed = time() - g.start_time
            endpoint = request.endpoint or 'unknown'
            
            with _lock:
                _metrics[endpoint]['count'] += 1
                _metrics[endpoint]['total_time'] += elapsed
                _metrics[endpoint]['min_time'] = min(_metrics[endpoint]['min_time'], elapsed)
                _metrics[endpoint]['max_time'] = max(_metrics[endpoint]['max_time'], elapsed)
        
        return response
    
    @app.route('/api/metrics')
    def get_metrics():
        """Endpoint de métricas"""
        with _lock:
            metrics = {}
            for endpoint, data in _metrics.items():
                metrics[endpoint] = {
                    'count': data['count'],
                    'avg_time_ms': round((data['total_time'] / data['count']) * 1000, 2) if data['count'] > 0 else 0,
                    'min_time_ms': round(data['min_time'] * 1000, 2),
                    'max_time_ms': round(data['max_time'] * 1000, 2),
                    'total_time_s': round(data['total_time'], 2)
                }
        
        return metrics

def reset_metrics():
    """Resetear métricas"""
    with _lock:
        _metrics.clear()
