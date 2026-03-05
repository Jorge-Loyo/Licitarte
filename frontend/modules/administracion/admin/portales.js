import { modals } from './admin-utils.js';

let portales = [];

export async function cargarPortales() {
  const response = await fetch('/api/portales-origen');
  portales = await response.json();
  const tbody = document.getElementById('portalesBody');
  tbody.innerHTML = '';
  portales.forEach(p => {
    tbody.innerHTML += `<tr><td>${p.id}</td><td>${p.nombre}</td><td>
      <button onclick="window.editarPortal(${p.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarPortal(${p.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });
}

export function nuevoPortal() {
  document.getElementById('modalPortalTitulo').textContent = 'Nuevo Portal/Origen';
  document.getElementById('portalForm').reset();
  document.getElementById('portalId').value = '';
  document.getElementById('modalPortal').style.display = 'block';
}

window.editarPortal = function(id) {
  const portal = portales.find(p => p.id === id);
  if (!portal) return;

  document.getElementById('modalPortalTitulo').textContent = 'Editar Portal/Origen';
  document.getElementById('portalId').value = portal.id;
  document.getElementById('portalNombre').value = portal.nombre;
  document.getElementById('modalPortal').style.display = 'block';
};

export async function guardarPortal(e) {
  e.preventDefault();
  const id = document.getElementById('portalId').value;
  const nombre = document.getElementById('portalNombre').value;

  const url = id ? `/api/portales-origen/${id}` : '/api/portales-origen';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Portal actualizado' : 'Portal creado', 'success');
    document.getElementById('modalPortal').style.display = 'none';
    cargarPortales();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

window.eliminarPortal = async function(id) {
  modals.showConfirm('¿Eliminar este portal?', async () => {
    const response = await fetch(`/api/portales-origen/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', 'Portal eliminado', 'success');
      cargarPortales();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  });
};
