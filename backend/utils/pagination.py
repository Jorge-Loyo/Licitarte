"""Utilidad de paginación consistente"""
from typing import Dict, Any, List
from math import ceil

class Paginator:
    """Paginador reutilizable"""
    
    def __init__(self, items: List[Any], page: int = 1, per_page: int = 10):
        self.items = items
        self.page = max(1, page)
        self.per_page = min(per_page, 100)  # Máximo 100 items
        self.total = len(items)
        self.total_pages = ceil(self.total / self.per_page) if self.per_page > 0 else 0
    
    def get_page(self) -> List[Any]:
        """Obtener items de la página actual"""
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para respuesta API"""
        return {
            'items': self.get_page(),
            'page': self.page,
            'per_page': self.per_page,
            'total': self.total,
            'total_pages': self.total_pages,
            'has_prev': self.page > 1,
            'has_next': self.page < self.total_pages
        }
