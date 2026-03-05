"""Blueprint de productos - Refactorizado"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from pydantic import ValidationError
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.api.services.producto_service import ProductoService
from backend.api.schemas.dtos import ResponseDTO
from backend.validators import ProductoCreate
from backend.constants import ErrorMessages

bp = Blueprint('productos', __name__, url_prefix='/api/productos')
service = ProductoService()

@bp.route('/<int:licitacion_id>', methods=['GET'])
@login_required
def get_productos(licitacion_id):
    """Obtener productos de una licitación"""
    try:
        productos = service.obtener_por_licitacion(licitacion_id)
        return jsonify(productos), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('', methods=['POST'])
@login_required
def crear_producto():
    """Crear nuevo producto"""
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        data = ProductoCreate(**request.json)
    except ValidationError as e:
        return jsonify(ResponseDTO.error(ErrorMessages.DATOS_INVALIDOS, e.errors())), 400
    
    try:
        producto_id = service.crear(data)
        return jsonify(ResponseDTO.success({'id': producto_id})), 201
    except Exception as e:
        return jsonify(ResponseDTO.error(str(e))), 400

@bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar_producto(id):
    """Actualizar producto existente"""
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        service.actualizar(id, request.json)
        return jsonify(ResponseDTO.success()), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500
