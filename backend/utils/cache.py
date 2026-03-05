"""Sistema de caché simple en memoria"""
from functools import wraps
from datetime import datetime, timedelta

_cache = {}
_cache_ttl = {}

def cache(ttl_seconds=300):
    """Decorator para cachear resultados de funciones"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Crear key único
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Verificar si existe y no expiró
            if cache_key in _cache:
                if datetime.now() < _cache_ttl[cache_key]:
                    return _cache[cache_key]
            
            # Ejecutar función y cachear
            result = func(*args, **kwargs)
            _cache[cache_key] = result
            _cache_ttl[cache_key] = datetime.now() + timedelta(seconds=ttl_seconds)
            
            return result
        
        return wrapper
    return decorator

def clear_cache(pattern=None):
    """Limpiar caché completo o por patrón"""
    if pattern:
        keys_to_delete = [k for k in _cache.keys() if pattern in k]
        for key in keys_to_delete:
            del _cache[key]
            del _cache_ttl[key]
    else:
        _cache.clear()
        _cache_ttl.clear()
