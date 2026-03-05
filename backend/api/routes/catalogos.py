"""Rutas de catálogos - Refactorizado"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from pydantic import ValidationError
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.api.services.catalogo_service import CatalogoService
from backend.api.schemas.dtos import ResponseDTO
from backend.validators import ClienteCreate
from backend.constants import ErrorMessages

bp = Blueprint('catalogos', __name__, url_prefix='/api')
service = CatalogoService()

# CLIENTES
@bp.route('/clientes', methods=['GET'])
@login_required
def get_clientes():
    try:
        clientes = service.obtener_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/clientes', methods=['POST'])
@login_required
def crear_cliente():
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        data = ClienteCreate(**request.json)
    except ValidationError as e:
        return jsonify(ResponseDTO.error(ErrorMessages.DATOS_INVALIDOS, e.errors())), 400
    
    try:
        cliente_id = service.crear_cliente(data)
        return jsonify(ResponseDTO.success({'id': cliente_id})), 201
    except Exception as e:
        return jsonify(ResponseDTO.error(str(e))), 400

@bp.route('/clientes/<int:id>', methods=['PUT'])
@login_required
def actualizar_cliente(id):
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        service.actualizar_cliente(id, request.json)
        return jsonify(ResponseDTO.success()), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/clientes/<int:id>', methods=['DELETE'])
@login_required
def eliminar_cliente(id):
    try:
        service.eliminar_cliente(id)
        return '', 204
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

# OFERENTES
@bp.route('/oferentes', methods=['GET'])
@login_required
def get_oferentes():
    try:
        oferentes = service.obtener_oferentes()
        return jsonify(oferentes), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/oferentes', methods=['POST'])
@login_required
def crear_oferente():
    if not request.json or not request.json.get('nombre'):
        return jsonify(ResponseDTO.error('Nombre es obligatorio')), 400
    
    try:
        oferente_id = service.crear_oferente(request.json['nombre'])
        return jsonify(ResponseDTO.success({'id': oferente_id})), 201
    except Exception as e:
        return jsonify(ResponseDTO.error(str(e))), 400

@bp.route('/oferentes/<int:id>', methods=['PUT'])
@login_required
def actualizar_oferente(id):
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        service.actualizar_oferente(id, request.json['nombre'])
        return jsonify(ResponseDTO.success()), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/oferentes/<int:id>', methods=['DELETE'])
@login_required
def eliminar_oferente(id):
    try:
        service.eliminar_oferente(id)
        return '', 204
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

# MARCAS
@bp.route('/marcas', methods=['GET'])
@login_required
def get_marcas():
    try:
        marcas = service.obtener_marcas()
        return jsonify(marcas), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/marcas', methods=['POST'])
@login_required
def crear_marca():
    if not request.json or not request.json.get('nombre'):
        return jsonify(ResponseDTO.error('Nombre es obligatorio')), 400
    
    try:
        marca_id = service.crear_marca(request.json['nombre'])
        return jsonify(ResponseDTO.success({'id': marca_id})), 201
    except Exception as e:
        return jsonify(ResponseDTO.error(str(e))), 400

@bp.route('/marcas/<int:id>', methods=['PUT'])
@login_required
def actualizar_marca(id):
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        service.actualizar_marca(id, request.json['nombre'])
        return jsonify(ResponseDTO.success()), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/marcas/<int:id>', methods=['DELETE'])
@login_required
def eliminar_marca(id):
    try:
        service.eliminar_marca(id)
        return '', 204
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

# TIPOS LICITACION
@bp.route('/tipos-licitacion', methods=['GET'])
@login_required
def get_tipos_licitacion():
    try:
        tipos = service.obtener_tipos_licitacion()
        return jsonify(tipos), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/tipos-licitacion', methods=['POST'])
@login_required
def crear_tipo_licitacion():
    if not request.json or not request.json.get('nombre'):
        return jsonify(ResponseDTO.error('Nombre es obligatorio')), 400
    
    try:
        tipo_id = service.crear_tipo_licitacion(request.json['nombre'])
        return jsonify(ResponseDTO.success({'id': tipo_id})), 201
    except Exception as e:
        return jsonify(ResponseDTO.error(str(e))), 400

@bp.route('/tipos-licitacion/<int:id>', methods=['PUT'])
@login_required
def actualizar_tipo_licitacion(id):
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        service.actualizar_tipo_licitacion(id, request.json['nombre'])
        return jsonify(ResponseDTO.success()), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

@bp.route('/tipos-licitacion/<int:id>', methods=['DELETE'])
@login_required
def eliminar_tipo_licitacion(id):
    try:
        service.eliminar_tipo_licitacion(id)
        return '', 204
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500

# CATALOGO MEDICAMENTOS
@bp.route('/catalogo', methods=['GET'])
@login_required
def get_catalogo():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        search = request.args.get('search', '').strip()
        
        resultado = service.obtener_catalogo(page, per_page, search)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500
