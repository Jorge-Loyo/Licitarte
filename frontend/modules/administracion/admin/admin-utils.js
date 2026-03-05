// Utilidades compartidas para administración
export const utils = {
  async renderRow(templateName, data) {
    const html = await TemplateLoader.loadAndRender(templateName, data);
    const tr = document.createElement('tr');
    tr.innerHTML = html;
    return tr.firstElementChild;
  },

  showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
  },

  hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
  },

  resetForm(formId) {
    document.getElementById(formId).reset();
  }
};

export const modals = {
  showMessage(titulo, mensaje, tipo) {
    let modal = document.getElementById('modalMensaje');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'modalMensaje';
      modal.style.cssText = `position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7); display: flex; align-items: center;
        justify-content: center; z-index: 10001;`;
      modal.innerHTML = `
        <div style="background: var(--bg-card); padding: 30px; border-radius: 10px; min-width: 400px; max-width: 500px;">
          <h3 id="tituloMensaje" style="margin: 0 0 15px 0; color: var(--text);"></h3>
          <p id="textoMensaje" style="margin: 0 0 20px 0; color: var(--text);"></p>
          <button onclick="document.getElementById('modalMensaje').style.display='none'" class="btn-primary" style="width: 100%;">Aceptar</button>
        </div>`;
      document.body.appendChild(modal);
    }
    document.getElementById('tituloMensaje').textContent = titulo;
    document.getElementById('tituloMensaje').style.color = tipo === 'success' ? '#66bb6a' : '#ff5252';
    document.getElementById('textoMensaje').textContent = mensaje;
    modal.style.display = 'flex';
  },

  showConfirm(mensaje, callback) {
    let modal = document.getElementById('modalConfirmar');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'modalConfirmar';
      modal.style.cssText = `position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7); display: flex; align-items: center;
        justify-content: center; z-index: 10002;`;
      modal.innerHTML = `
        <div style="background: var(--bg-card); padding: 30px; border-radius: 10px; min-width: 400px; max-width: 500px;">
          <h3 style="margin: 0 0 15px 0; color: var(--text);">Confirmar</h3>
          <p id="textoConfirmar" style="margin: 0 0 20px 0; color: var(--text);"></p>
          <div style="display: flex; gap: 10px;">
            <button onclick="document.getElementById('modalConfirmar').style.display='none'" class="btn-secondary" style="flex: 1;">Cancelar</button>
            <button id="btnConfirmar" class="btn-danger" style="flex: 1;">Aceptar</button>
          </div>
        </div>`;
      document.body.appendChild(modal);
    }
    document.getElementById('textoConfirmar').textContent = mensaje;
    document.getElementById('btnConfirmar').onclick = () => {
      modal.style.display = 'none';
      callback();
    };
    modal.style.display = 'flex';
  },

  showProgress(mensaje, progreso, total) {
    let modal = document.getElementById('modalProgreso');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'modalProgreso';
      modal.style.cssText = `position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7); display: flex; align-items: center;
        justify-content: center; z-index: 10000;`;
      modal.innerHTML = `
        <div style="background: var(--bg-card); padding: 30px; border-radius: 10px; min-width: 400px; text-align: center;">
          <div class="spinner" style="margin: 0 auto 20px;"></div>
          <p id="mensajeProgreso" style="margin: 15px 0; font-size: 16px; color: var(--text);"></p>
          <div style="background: var(--bg-dark); border-radius: 10px; height: 30px; overflow: hidden; margin-top: 15px;">
            <div id="barraProgreso" style="background: var(--primary); height: 100%; width: 0%; transition: width 0.3s;"></div>
          </div>
          <p id="porcentajeProgreso" style="margin-top: 10px; color: var(--primary); font-weight: bold;"></p>
        </div>`;
      document.body.appendChild(modal);
    }
    document.getElementById('mensajeProgreso').textContent = mensaje;
    document.getElementById('barraProgreso').style.width = `${(progreso / total) * 100}%`;
    document.getElementById('porcentajeProgreso').textContent = `${progreso} / ${total}`;
    modal.style.display = 'flex';
  },

  updateProgress(mensaje, progreso, total) {
    document.getElementById('mensajeProgreso').textContent = mensaje;
    document.getElementById('barraProgreso').style.width = `${(progreso / total) * 100}%`;
    document.getElementById('porcentajeProgreso').textContent = `${progreso} / ${total}`;
  },

  hideProgress() {
    const modal = document.getElementById('modalProgreso');
    if (modal) modal.style.display = 'none';
  }
};

window.mostrarModalMensaje = modals.showMessage;
window.mostrarModalConfirmar = modals.showConfirm;
