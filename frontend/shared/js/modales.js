// Funciones de modales personalizados

function mostrarModalMensaje(titulo, mensaje, tipo) {
  let modal = document.getElementById("modalMensaje");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "modalMensaje";
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.7); display: flex; align-items: center;
      justify-content: center; z-index: 10001;
    `;
    modal.innerHTML = `
      <div style="background: var(--bg-card); padding: 30px; border-radius: 10px; min-width: 400px; max-width: 500px;">
        <h3 id="tituloMensaje" style="margin: 0 0 15px 0; color: var(--text);"></h3>
        <p id="textoMensaje" style="margin: 0 0 20px 0; color: var(--text);"></p>
        <button onclick="cerrarModalMensaje()" class="btn-primary" style="width: 100%;">Aceptar</button>
      </div>
    `;
    document.body.appendChild(modal);
  }
  document.getElementById("tituloMensaje").textContent = titulo;
  document.getElementById("tituloMensaje").style.color = tipo === "success" ? "#66bb6a" : "#ff5252";
  document.getElementById("textoMensaje").textContent = mensaje;
  modal.style.display = "flex";
}

function cerrarModalMensaje() {
  const modal = document.getElementById("modalMensaje");
  if (modal) modal.style.display = "none";
}

function mostrarModalConfirmar(mensaje, callback) {
  let modal = document.getElementById("modalConfirmar");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "modalConfirmar";
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.7); display: flex; align-items: center;
      justify-content: center; z-index: 10002;
    `;
    modal.innerHTML = `
      <div style="background: var(--bg-card); padding: 30px; border-radius: 10px; min-width: 400px; max-width: 500px;">
        <h3 style="margin: 0 0 15px 0; color: var(--text);">Confirmar</h3>
        <p id="textoConfirmar" style="margin: 0 0 20px 0; color: var(--text);"></p>
        <div style="display: flex; gap: 10px;">
          <button onclick="cerrarModalConfirmar()" class="btn-secondary" style="flex: 1;">Cancelar</button>
          <button id="btnConfirmar" class="btn-danger" style="flex: 1;">Aceptar</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  document.getElementById("textoConfirmar").textContent = mensaje;
  document.getElementById("btnConfirmar").onclick = () => {
    cerrarModalConfirmar();
    callback();
  };
  modal.style.display = "flex";
}

function cerrarModalConfirmar() {
  const modal = document.getElementById("modalConfirmar");
  if (modal) modal.style.display = "none";
}
