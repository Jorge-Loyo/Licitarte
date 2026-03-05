// Loading component reutilizable

export const Loading = {
  // Mostrar loading en elemento específico
  show: (elementId) => {
    const element = document.getElementById(elementId);
    if (!element) return;

    const spinner = document.createElement('div');
    spinner.className = 'loading-overlay';
    spinner.innerHTML = `
      <div class="spinner"></div>
      <p>Cargando...</p>
    `;
    element.style.position = 'relative';
    element.appendChild(spinner);
  },

  // Ocultar loading
  hide: (elementId) => {
    const element = document.getElementById(elementId);
    if (!element) return;

    const spinner = element.querySelector('.loading-overlay');
    if (spinner) spinner.remove();
  },

  // Loading global (fullscreen)
  showGlobal: (message = 'Cargando...') => {
    if (document.getElementById('global-loading')) return;

    const overlay = document.createElement('div');
    overlay.id = 'global-loading';
    overlay.className = 'loading-overlay global';
    overlay.innerHTML = `
      <div class="spinner"></div>
      <p>${message}</p>
    `;
    document.body.appendChild(overlay);
  },

  hideGlobal: () => {
    const overlay = document.getElementById('global-loading');
    if (overlay) overlay.remove();
  },
};

// Agregar estilos
const style = document.createElement('style');
style.textContent = `
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 999;
    border-radius: 10px;
  }

  .loading-overlay.global {
    position: fixed;
    border-radius: 0;
    z-index: 9999;
  }

  .loading-overlay p {
    color: white;
    margin-top: 15px;
    font-size: 16px;
  }
`;
document.head.appendChild(style);
