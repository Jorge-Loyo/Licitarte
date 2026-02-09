"""Configuración de Gunicorn para producción"""
import os

# Timeout aumentado para carga de Excel
timeout = 300  # 5 minutos

# Workers
workers = int(os.environ.get('WEB_CONCURRENCY', 1))

# Bind
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Worker class
worker_class = 'sync'

# Keep alive
keepalive = 5
