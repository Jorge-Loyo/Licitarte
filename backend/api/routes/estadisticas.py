"""Rutas de estadísticas y métricas - Refactorizado"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.api.services.estadisticas_service import EstadisticasService
from backend.api.schemas.dtos import ResponseDTO
from backend.constants import ErrorMessages

bp = Blueprint('estadisticas', __name__, url_prefix='/api')
service = EstadisticasService()

@bp.route('/estadisticas', methods=['GET'])
@login_required
def get_estadisticas():
    """Obtener estadísticas generales del dashboard"""
    try:
        stats = service.obtener_estadisticas_generales()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/historico', methods=['POST'])
@login_required
def get_historico():
    """Obtener histórico de precios con filtros"""
    try:
        data = request.json or {}
        filtro = data.get('monodroga', '')
        productos = service.obtener_historico(filtro)
        return jsonify(productos), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/productos-adjudicados', methods=['GET'])
@login_required
def get_productos_adjudicados():
    """Obtener productos adjudicados para dashboard"""
    try:
        productos = service.obtener_productos_adjudicados()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500
