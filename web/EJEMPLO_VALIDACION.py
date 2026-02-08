"""Ejemplo de integración de validadores Pydantic"""
# Agregar al inicio de licitaciones.py:

from pydantic import ValidationError
from src.validators import LicitacionCreate
from src.utils.logging_config import logger

# Modificar endpoint crear_licitacion:

@bp.route('', methods=['POST'])
def crear_licitacion():
    """Crear nueva licitación con productos"""
    try:
        # Validar datos con Pydantic
        data = LicitacionCreate(**request.json)
        
        logger.info(f"Creating licitacion: {data.numero}")
        
        licitacion_id = db.crear_licitacion(
            data.numero,
            data.fecha,
            '',
            '',
            None,
            data.cliente_id,
            data.tipo_licitacion_id,
            data.portal_origen,
            data.modalidad_entrega,
            data.forma_pago,
            data.requiere_poliza,
            data.monto_poliza,
            data.observaciones,
            data.mantenimiento_oferta
        )
        
        logger.info(f"Licitacion created: {licitacion_id}")
        return jsonify({'success': True, 'id': licitacion_id}), 201
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.errors()}")
        return jsonify({
            'success': False,
            'error': 'Datos inválidos',
            'details': e.errors()
        }), 400
    except Exception as e:
        logger.error(f"Error creating licitacion: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Error interno'}), 500
