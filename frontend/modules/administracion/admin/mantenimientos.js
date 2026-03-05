import { modals } from './admin-utils.js';

let mantenimientos = [];

export async function cargarMantenimientos() {
  const response = await fetch('/api/mantenimientos-oferta');
  mantenimientos = await response.json();
  const tbody = document.getElementById('mantenimientosBody');
  tbody.innerHTML = '';
  mantenimientos.forEach(m => {
    tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
      <button onclick="window.editarMantenimiento(${m.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarMantenimiento(${m.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });
}

export function nuevoMantenimiento() {
  document.getElementById('modalMantenimientoTitulo').textContent = 'Nuevo Mantenimiento de Oferta';
  document.getElementById('mantenimientoForm').reset();
  document.getElementById('mantenimientoId').value = '';
  document.getElementById('modalMantenimiento').style.display = 'block';
}

window.editarMantenimiento = function(id) {
  const mantenimiento = mantenimientos.find(m => m.id === id);
  if (!mantenimiento) return;

  document.getElementById('modalMantenimientoTitulo').textContent = 'Editar Mantenimiento de Oferta';
  document.getElementById('mantenimientoId').value = mantenimiento.id;
  document.getElementById('mantenimientoNombre').value = mantenimiento.nombre;
  document.getElementById('modalMantenimiento').style.display = 'block';
};

export async function guardarMantenimiento(e) {
  e.preventDefault();
  const id = document.getElementById('mantenimientoId').value;
  const nombre = document.getElementById('mantenimientoNombre').value;

  const url = id ? `/api/mantenimientos-oferta/${id}` : '/api/mantenimientos-oferta';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Mantenimiento actualizado' : 'Mantenimiento creado', 'success');
    document.getElementById('modalMantenimiento').style.display = 'none';
    cargarMantenimientos();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

window.eliminarMantenimiento = async function(id) {
  modals.showConfirm('¿Eliminar este mantenimiento de oferta?', async () => {
    const response = await fetch(`/api/mantenimientos-oferta/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', 'Mantenimiento eliminado', 'success');
      cargarMantenimientos();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  });
};
