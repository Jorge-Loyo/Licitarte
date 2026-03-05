// Configuración centralizada de rutas API
export const API_ROUTES = {
  // Licitaciones
  licitaciones: '/api/licitaciones',
  licitacionById: (id) => `/api/licitaciones/${id}`,
  
  // Productos
  productos: '/api/productos',
  productosAdjudicados: '/api/productos-adjudicados',
  historico: '/api/historico',
  
  // Estadísticas
  estadisticas: '/api/estadisticas',
  
  // Administración - Clientes
  clientes: '/api/clientes',
  clienteById: (id) => `/api/clientes/${id}`,
  clientesExcel: '/api/clientes/excel',
  
  // Administración - Oferentes
  oferentes: '/api/oferentes',
  oferenteById: (id) => `/api/oferentes/${id}`,
  oferentesExcel: '/api/oferentes/excel',
  
  // Administración - Marcas
  marcas: '/api/marcas',
  marcaById: (id) => `/api/marcas/${id}`,
  marcasExcel: '/api/marcas/excel',
  
  // Administración - Laboratorios
  laboratorios: '/api/laboratorios',
  laboratorioById: (id) => `/api/laboratorios/${id}`,
  laboratoriosExcel: '/api/laboratorios/excel',
  
  // Administración - Monodrogas
  monodrogas: '/api/monodrogas',
  monodrogaById: (id) => `/api/monodrogas/${id}`,
  monodrogasExcel: '/api/monodrogas/excel',
  
  // Administración - Catálogo
  catalogo: '/api/catalogo',
  catalogoById: (id) => `/api/catalogo/${id}`,
  catalogoExcel: '/api/catalogo/excel',
  
  // Administración - Tipos
  tipos: '/api/tipos-licitacion',
  tipoById: (id) => `/api/tipos-licitacion/${id}`,
  
  // Administración - Organismos
  organismos: '/api/organismos',
  organismoById: (id) => `/api/organismos/${id}`,
  
  // Administración - Portales
  portales: '/api/portales',
  portalById: (id) => `/api/portales/${id}`,
  
  // Administración - Modalidades
  modalidades: '/api/modalidades',
  modalidadById: (id) => `/api/modalidades/${id}`,
  
  // Administración - Formas de Pago
  formasPago: '/api/formas-pago',
  formaPagoById: (id) => `/api/formas-pago/${id}`,
  
  // Administración - Motivos Pérdida
  motivosPerdida: '/api/motivos-perdida',
  motivoPerdidaById: (id) => `/api/motivos-perdida/${id}`,
  
  // Administración - Mantenimientos
  mantenimientos: '/api/mantenimientos',
  mantenimientoById: (id) => `/api/mantenimientos/${id}`,
  
  // Pólizas
  polizas: '/api/polizas',
  polizaById: (id) => `/api/polizas/${id}`,
};

// Rutas de páginas
export const PAGE_ROUTES = {
  dashboard: '/dashboard',
  nuevaLicitacion: '/nueva-licitacion',
  gestion: '/gestion',
  gestionNueva: '/gestion-nueva',
  metricas: '/metricas',
  polizas: '/polizas',
  documentacion: '/documentacion',
  administracion: '/administracion',
  ayuda: '/ayuda',
  editarLicitacion: (id) => `/editar-licitacion/${id}`,
  resultadoLicitacion: (id) => `/resultado-licitacion/${id}`,
  presupuesto: (numero) => `/presupuesto/${numero}`,
};

// Constantes del sistema
export const CONSTANTS = {
  // Paginación
  ITEMS_PER_PAGE: 10,
  MAX_ITEMS_PER_PAGE: 100,
  
  // Archivos
  MAX_FILE_SIZE: 16 * 1024 * 1024, // 16MB
  ALLOWED_FILE_TYPES: ['.pdf', '.jpg', '.jpeg', '.png', '.xlsx', '.xls'],
  MAX_FILES: 10,
  
  // Formatos
  DATE_FORMAT: 'DD/MM/YYYY',
  DATETIME_FORMAT: 'DD/MM/YYYY HH:mm',
  CURRENCY_LOCALE: 'es-AR',
  
  // Validaciones
  MIN_PASSWORD_LENGTH: 8,
  MAX_TEXT_LENGTH: 500,
  CUIT_REGEX: /^\d{2}-\d{8}-\d{1}$/,
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  
  // Timeouts
  DEBOUNCE_DELAY: 300,
  NOTIFICATION_DURATION: 3000,
  API_TIMEOUT: 30000,
};
