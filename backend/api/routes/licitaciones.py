"""Blueprint de licitaciones.

Maneja CRUD completo de licitaciones farmacéuticas.
Validación: Pydantic
Lógica de negocio: LicitacionService
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from pydantic import ValidationError
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.api.services.licitacion_service import LicitacionService
from backend.api.schemas.dtos import ResponseDTO
from backend.validators import LicitacionCreate
from backend.constants import ErrorMessages

bp = Blueprint('licitaciones', __name__, url_prefix='/api/licitaciones')
service = LicitacionService()

@bp.route('', methods=['GET'])
@login_required
def get_licitaciones():
    """Obtener todas las licitaciones con estadísticas"""
    try:
        licitaciones = service.obtener_todas()
        return jsonify(licitaciones), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('', methods=['POST'])
@login_required
def crear_licitacion():
    """Crear nueva licitación con productos"""
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        data = LicitacionCreate(**request.json)
    except ValidationError as e:
        return jsonify(ResponseDTO.error(ErrorMessages.DATOS_INVALIDOS, e.errors())), 400
    
    try:
        licitacion_id = service.crear(data)
        return jsonify(ResponseDTO.success({'id': licitacion_id})), 201
    except ValueError as e:
        return jsonify(ResponseDTO.error(str(e))), 400
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/<int:id>', methods=['GET'])
@login_required
def get_licitacion(id):
    """Obtener una licitación específica"""
    try:
        licitacion = service.obtener_por_id(id)
        if licitacion:
            return jsonify(licitacion), 200
        return jsonify(ResponseDTO.error(ErrorMessages.NO_ENCONTRADO)), 404
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/<int:id>/detalle', methods=['GET'])
@login_required
def get_licitacion_detalle(id):
    """Obtener detalle completo de licitación para edición"""
    try:
        detalle = service.obtener_detalle(id)
        if detalle:
            return jsonify(detalle), 200
        return jsonify(ResponseDTO.error(ErrorMessages.NO_ENCONTRADO)), 404
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar_licitacion(id):
    """Actualizar licitación existente"""
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        service.actualizar(id, request.json)
        return jsonify(ResponseDTO.success()), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def eliminar_licitacion(id):
    """Eliminar licitación"""
    try:
        service.eliminar(id)
        return '', 204
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500
