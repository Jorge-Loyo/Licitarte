import { modals } from './admin-utils.js';

let formasPago = [];

export async function cargarFormasPago() {
  const response = await fetch('/api/formas-pago');
  formasPago = await response.json();
  const tbody = document.getElementById('formasBody');
  tbody.innerHTML = '';
  formasPago.forEach(f => {
    tbody.innerHTML += `<tr><td>${f.id}</td><td>${f.nombre}</td><td>
      <button onclick="window.editarFormaPago(${f.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarFormaPago(${f.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });
}

export function nuevaFormaPago() {
  document.getElementById('modalFormaPagoTitulo').textContent = 'Nueva Forma de Pago';
  document.getElementById('formaPagoForm').reset();
  document.getElementById('formaPagoId').value = '';
  document.getElementById('modalFormaPago').style.display = 'block';
}

window.editarFormaPago = function(id) {
  const forma = formasPago.find(f => f.id === id);
  if (!forma) return;

  document.getElementById('modalFormaPagoTitulo').textContent = 'Editar Forma de Pago';
  document.getElementById('formaPagoId').value = forma.id;
  document.getElementById('formaPagoNombre').value = forma.nombre;
  document.getElementById('modalFormaPago').style.display = 'block';
};

export async function guardarFormaPago(e) {
  e.preventDefault();
  const id = document.getElementById('formaPagoId').value;
  const nombre = document.getElementById('formaPagoNombre').value;

  const url = id ? `/api/formas-pago/${id}` : '/api/formas-pago';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Forma de pago actualizada' : 'Forma de pago creada', 'success');
    document.getElementById('modalFormaPago').style.display = 'none';
    cargarFormasPago();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

window.eliminarFormaPago = async function(id) {
  modals.showConfirm('¿Eliminar esta forma de pago?', async () => {
    const response = await fetch(`/api/formas-pago/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', 'Forma de pago eliminada', 'success');
      cargarFormasPago();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  });
};
