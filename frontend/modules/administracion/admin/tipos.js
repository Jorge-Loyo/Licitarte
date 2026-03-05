import { modals } from './admin-utils.js';

let tiposLicitacion = [];

export async function cargarTipos() {
  const response = await fetch('/api/tipos-licitacion');
  tiposLicitacion = await response.json();
  mostrarTipos(tiposLicitacion);
}

async function mostrarTipos(data) {
  const tbody = document.getElementById('tiposBody');
  tbody.textContent = '';

  for (const t of data) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${t.id}</td>
      <td>${t.nombre}</td>
      <td>
        <button class="btn-editar btn-primary">Editar</button>
        <button class="btn-eliminar btn-danger">Eliminar</button>
      </td>
    `;
    
    tr.querySelector('.btn-editar').onclick = () => editarTipo(t.id);
    tr.querySelector('.btn-eliminar').onclick = () => eliminarTipo(t.id);
    
    tbody.appendChild(tr);
  }
}

export function nuevoTipo() {
  document.getElementById('modalTipoTitulo').textContent = 'Nuevo Tipo de Licitación';
  document.getElementById('tipoForm').reset();
  document.getElementById('tipoId').value = '';
  document.getElementById('modalTipo').style.display = 'block';
}

function editarTipo(id) {
  const tipo = tiposLicitacion.find(t => t.id === id);
  if (!tipo) return;

  document.getElementById('modalTipoTitulo').textContent = 'Editar Tipo de Licitación';
  document.getElementById('tipoId').value = tipo.id;
  document.getElementById('tipoNombre').value = tipo.nombre;
  document.getElementById('modalTipo').style.display = 'block';
}

export async function guardarTipo(e) {
  e.preventDefault();
  const id = document.getElementById('tipoId').value;
  const nombre = document.getElementById('tipoNombre').value;

  const url = id ? `/api/tipos-licitacion/${id}` : '/api/tipos-licitacion';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    modals.showMessage('Mensaje', id ? 'Tipo actualizado' : 'Tipo creado', 'success');
    document.getElementById('modalTipo').style.display = 'none';
    cargarTipos();
  } else {
    modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
  }
}

async function eliminarTipo(id) {
  modals.showConfirm('¿Eliminar este tipo de licitación?', async () => {
    const response = await fetch(`/api/tipos-licitacion/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      cargarTipos();
      modals.showMessage('Éxito', 'Tipo eliminado', 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  });
}

export async function subirExcelTipos() {
  const fileInput = document.getElementById('excelTipos');
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/cargar-tipos-licitacion', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', '✓ ' + result.message, 'success');
      cargarTipos();
    } else {
      modals.showMessage('Mensaje', '✗ Error: ' + result.error, 'success');
    }
  } catch (error) {
    modals.showMessage('Mensaje', '✗ Error: ' + error.message, 'success');
  }
  fileInput.value = '';
}
