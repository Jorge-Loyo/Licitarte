// Manejador global de errores

export const ErrorHandler = {
  // Inicializar manejador global
  init: () => {
    // Capturar errores no manejados
    window.addEventListener('error', (event) => {
      console.error('Error no manejado:', event.error);
      ErrorHandler.log(event.error);
    });

    // Capturar promesas rechazadas
    window.addEventListener('unhandledrejection', (event) => {
      console.error('Promise rechazada:', event.reason);
      ErrorHandler.log(event.reason);
    });
  },

  // Registrar error
  log: (error) => {
    const errorData = {
      message: error.message || 'Error desconocido',
      stack: error.stack,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
    };

    // Enviar a servidor (opcional)
    // fetch('/api/logs/error', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(errorData)
    // });

    console.error('Error registrado:', errorData);
  },

  // Manejar error HTTP
  handleHTTPError: (response) => {
    const errors = {
      400: 'Solicitud inválida',
      401: 'No autorizado. Por favor inicie sesión',
      403: 'Acceso denegado',
      404: 'Recurso no encontrado',
      500: 'Error del servidor',
      503: 'Servicio no disponible',
    };

    const message = errors[response.status] || `Error ${response.status}`;
    
    if (response.status === 401) {
      // Redirigir a login
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
    }

    return message;
  },
};

// Inicializar automáticamente
ErrorHandler.init();
