import { modals } from './admin-utils.js';

let motivosPerdida = [];

export async function cargarMotivosPerdida() {
  const response = await fetch('/api/motivos-perdida');
  motivosPerdida = await response.json();
  const tbody = document.getElementById('motivosBody');
  tbody.innerHTML = '';
  motivosPerdida.forEach(m => {
    tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
      <button onclick="window.editarMotivoPerdida(${m.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarMotivoPerdida(${m.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });
}

export function nuevoMotivoPerdida() {
  document.getElementById('modalMotivoPerdidaTitulo').textContent = 'Nuevo Motivo de Pérdida';
  document.getElementById('motivoPerdidaForm').reset();
  document.getElementById('motivoPerdidaId').value = '';
  document.getElementById('modalMotivoPerdida').style.display = 'block';
}

window.editarMotivoPerdida = function(id) {
  const motivo = motivosPerdida.find(m => m.id === id);
  if (!motivo) return;

  document.getElementById('modalMotivoPerdidaTitulo').textContent = 'Editar Motivo de Pérdida';
  document.getElementById('motivoPerdidaId').value = motivo.id;
  document.getElementById('motivoPerdidaNombre').value = motivo.nombre;
  document.getElementById('modalMotivoPerdida').style.display = 'block';
};

export async function guardarMotivoPerdida(e) {
  e.preventDefault();
  const id = document.getElementById('motivoPerdidaId').value;
  const nombre = document.getElementById('motivoPerdidaNombre').value;

  const url = id ? `/api/motivos-perdida/${id}` : '/api/motivos-perdida';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Motivo actualizado' : 'Motivo creado', 'success');
    document.getElementById('modalMotivoPerdida').style.display = 'none';
    cargarMotivosPerdida();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

window.eliminarMotivoPerdida = async function(id) {
  modals.showConfirm('¿Eliminar este motivo de pérdida?', async () => {
    const response = await fetch(`/api/motivos-perdida/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', 'Motivo eliminado', 'success');
      cargarMotivosPerdida();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  });
};
