import { modals } from './admin-utils.js';

let organismos = [];

export async function cargarOrganismos() {
  const response = await fetch('/api/organismos');
  organismos = await response.json();
  const tbody = document.getElementById('organismosBody');
  tbody.innerHTML = '';
  organismos.forEach(o => {
    tbody.innerHTML += `<tr><td>${o.id}</td><td>${o.nombre}</td><td>
      <button onclick="window.editarOrganismo(${o.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarOrganismo(${o.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });
}

export function nuevoOrganismo() {
  document.getElementById('modalOrganismoTitulo').textContent = 'Nuevo Organismo';
  document.getElementById('organismoForm').reset();
  document.getElementById('organismoId').value = '';
  document.getElementById('modalOrganismo').style.display = 'block';
}

window.editarOrganismo = function(id) {
  const organismo = organismos.find(o => o.id === id);
  if (!organismo) return;

  document.getElementById('modalOrganismoTitulo').textContent = 'Editar Organismo';
  document.getElementById('organismoId').value = organismo.id;
  document.getElementById('organismoNombre').value = organismo.nombre;
  document.getElementById('modalOrganismo').style.display = 'block';
};

export async function guardarOrganismo(e) {
  e.preventDefault();
  const id = document.getElementById('organismoId').value;
  const nombre = document.getElementById('organismoNombre').value;

  const url = id ? `/api/organismos/${id}` : '/api/organismos';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Organismo actualizado' : 'Organismo creado', 'success');
    document.getElementById('modalOrganismo').style.display = 'none';
    cargarOrganismos();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

window.eliminarOrganismo = async function(id) {
  modals.showConfirm('¿Eliminar este organismo?', async () => {
    const response = await fetch(`/api/organismos/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', 'Organismo eliminado', 'success');
      cargarOrganismos();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  });
};
