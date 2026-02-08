"""Sistema de logging estructurado"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

# Crear directorio de logs
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Formatter para logs en formato JSON"""
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        return json.dumps(log_data, ensure_ascii=False)

def setup_logger(name='licitarte'):
    """Configurar logger con rotación de archivos"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicados
    if logger.handlers:
        return logger
    
    # Handler para archivo JSON
    json_handler = RotatingFileHandler(
        log_dir / 'app.json.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    json_handler.setFormatter(JSONFormatter())
    json_handler.setLevel(logging.INFO)
    
    # Handler para archivo texto
    text_handler = RotatingFileHandler(
        log_dir / 'app.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    text_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    text_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))
    console_handler.setLevel(logging.WARNING)
    
    logger.addHandler(json_handler)
    logger.addHandler(text_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()
