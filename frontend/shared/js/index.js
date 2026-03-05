// Exports centralizados de utilidades compartidas

export { API_ROUTES, PAGE_ROUTES, CONSTANTS } from './config.js';
export { 
  Validators, 
  ErrorMessages, 
  validateForm, 
  clearFormErrors,
  showFieldError,
  clearFieldError 
} from './validators.js';
export { Loading } from './loading.js';
export { ErrorHandler } from './error-handler.js';

// Utilidades comunes
export const Utils = {
  // Formatear moneda argentina
  formatCurrency: (value) => {
    if (value >= 1000000) {
      return '$' + (value / 1000000).toLocaleString('es-AR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }) + ' MILL';
    }
    return '$' + value.toLocaleString('es-AR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  },

  // Formatear fecha
  formatDate: (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-AR');
  },

  // Formatear fecha y hora
  formatDateTime: (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('es-AR');
  },

  // Debounce para búsquedas
  debounce: (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // Mostrar notificación
  showNotification: (message, type = 'info') => {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 25px;
      background: var(--${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'}-color);
      color: white;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.3);
      z-index: 10000;
      animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-out';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  },

  // Confirmar acción
  confirm: async (message) => {
    return window.confirm(message);
  },

  // Crear elemento de tabla
  createTableCell: (text) => {
    const td = document.createElement('td');
    td.textContent = text;
    return td;
  },

  // Fetch con manejo de errores
  fetchAPI: async (url, options = {}) => {
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      Utils.showNotification('Error al conectar con el servidor', 'error');
      throw error;
    }
  },
};

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
  
  .error {
    border-color: var(--danger-color) !important;
    box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2) !important;
  }
`;
document.head.appendChild(style);
