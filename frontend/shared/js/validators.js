// Validaciones centralizadas para formularios

export const Validators = {
  // Validar email
  email: (value) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(value);
  },

  // Validar CUIT argentino (XX-XXXXXXXX-X)
  cuit: (value) => {
    const regex = /^\d{2}-\d{8}-\d{1}$/;
    return regex.test(value);
  },

  // Validar teléfono argentino
  telefono: (value) => {
    const regex = /^(\+54)?[\s-]?\d{2,4}[\s-]?\d{6,8}$/;
    return regex.test(value);
  },

  // Validar campo requerido
  required: (value) => {
    return value !== null && value !== undefined && value.toString().trim() !== '';
  },

  // Validar número positivo
  positiveNumber: (value) => {
    const num = parseFloat(value);
    return !isNaN(num) && num > 0;
  },

  // Validar rango numérico
  numberRange: (value, min, max) => {
    const num = parseFloat(value);
    return !isNaN(num) && num >= min && num <= max;
  },

  // Validar longitud mínima
  minLength: (value, length) => {
    return value && value.toString().length >= length;
  },

  // Validar longitud máxima
  maxLength: (value, length) => {
    return value && value.toString().length <= length;
  },

  // Validar fecha no futura
  notFutureDate: (value) => {
    const date = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date <= today;
  },

  // Validar fecha futura
  futureDate: (value) => {
    const date = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date >= today;
  },
};

// Mensajes de error por defecto
export const ErrorMessages = {
  required: 'Este campo es obligatorio',
  email: 'Email inválido',
  cuit: 'CUIT inválido (formato: XX-XXXXXXXX-X)',
  telefono: 'Teléfono inválido',
  positiveNumber: 'Debe ser un número positivo',
  minLength: (length) => `Mínimo ${length} caracteres`,
  maxLength: (length) => `Máximo ${length} caracteres`,
  notFutureDate: 'La fecha no puede ser futura',
  futureDate: 'La fecha debe ser futura',
};

// Validar formulario completo
export function validateForm(formId, rules) {
  const form = document.getElementById(formId);
  if (!form) return { valid: false, errors: ['Formulario no encontrado'] };

  const errors = [];
  let firstErrorField = null;

  for (const [fieldId, fieldRules] of Object.entries(rules)) {
    const field = document.getElementById(fieldId);
    if (!field) continue;

    const value = field.value;

    for (const rule of fieldRules) {
      const { validator, message, params = [] } = rule;
      
      if (!Validators[validator](value, ...params)) {
        errors.push({ field: fieldId, message });
        if (!firstErrorField) firstErrorField = field;
        
        // Marcar campo con error
        field.classList.add('error');
        break;
      } else {
        field.classList.remove('error');
      }
    }
  }

  // Focus en primer campo con error
  if (firstErrorField) {
    firstErrorField.focus();
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

// Limpiar errores de formulario
export function clearFormErrors(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.querySelectorAll('.error').forEach(field => {
    field.classList.remove('error');
  });
}

// Mostrar mensaje de error
export function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return;

  field.classList.add('error');
  
  // Crear o actualizar mensaje de error
  let errorMsg = field.nextElementSibling;
  if (!errorMsg || !errorMsg.classList.contains('error-message')) {
    errorMsg = document.createElement('small');
    errorMsg.className = 'error-message';
    errorMsg.style.color = 'var(--danger-color)';
    errorMsg.style.display = 'block';
    errorMsg.style.marginTop = '5px';
    field.parentNode.insertBefore(errorMsg, field.nextSibling);
  }
  errorMsg.textContent = message;
}

// Limpiar mensaje de error de campo
export function clearFieldError(fieldId) {
  const field = document.getElementById(fieldId);
  if (!field) return;

  field.classList.remove('error');
  
  const errorMsg = field.nextElementSibling;
  if (errorMsg && errorMsg.classList.contains('error-message')) {
    errorMsg.remove();
  }
}
