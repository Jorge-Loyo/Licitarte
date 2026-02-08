"""Configuración de seguridad"""
import os
from datetime import timedelta

class SecurityConfig:
    # Flask-Login
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).hex())
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Flask-Limiter
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Flask-CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000').split(',')
    CORS_SUPPORTS_CREDENTIALS = True
