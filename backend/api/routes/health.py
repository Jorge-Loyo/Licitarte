"""Health check endpoint"""
from flask import Blueprint, jsonify
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.database.db_manager import DatabaseManager

bp = Blueprint('health', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para monitoreo"""
    try:
        # Verificar conexión a BD
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'version': '1.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503

@bp.route('/status', methods=['GET'])
def status():
    """Status detallado del sistema"""
    import psutil
    import os
    
    return jsonify({
        'status': 'running',
        'pid': os.getpid(),
        'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
        'cpu_percent': psutil.cpu_percent(interval=0.1)
    }), 200
