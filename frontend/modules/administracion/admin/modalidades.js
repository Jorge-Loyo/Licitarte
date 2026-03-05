import { modals } from './admin-utils.js';

let modalidades = [];

export async function cargarModalidades() {
  const response = await fetch('/api/modalidades-entrega');
  modalidades = await response.json();
  const tbody = document.getElementById('modalidadesBody');
  tbody.innerHTML = '';
  modalidades.forEach(m => {
    tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
      <button onclick="window.editarModalidad(${m.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarModalidad(${m.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });
}

export function nuevaModalidad() {
  document.getElementById('modalModalidadTitulo').textContent = 'Nueva Modalidad de Entrega';
  document.getElementById('modalidadForm').reset();
  document.getElementById('modalidadId').value = '';
  document.getElementById('modalModalidad').style.display = 'block';
}

window.editarModalidad = function(id) {
  const modalidad = modalidades.find(m => m.id === id);
  if (!modalidad) return;

  document.getElementById('modalModalidadTitulo').textContent = 'Editar Modalidad de Entrega';
  document.getElementById('modalidadId').value = modalidad.id;
  document.getElementById('modalidadNombre').value = modalidad.nombre;
  document.getElementById('modalModalidad').style.display = 'block';
};

export async function guardarModalidad(e) {
  e.preventDefault();
  const id = document.getElementById('modalidadId').value;
  const nombre = document.getElementById('modalidadNombre').value;

  const url = id ? `/api/modalidades-entrega/${id}` : '/api/modalidades-entrega';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Modalidad actualizada' : 'Modalidad creada', 'success');
    document.getElementById('modalModalidad').style.display = 'none';
    cargarModalidades();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

window.eliminarModalidad = async function(id) {
  modals.showConfirm('¿Eliminar esta modalidad?', async () => {
    const response = await fetch(`/api/modalidades-entrega/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', 'Modalidad eliminada', 'success');
      cargarModalidades();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  });
};
