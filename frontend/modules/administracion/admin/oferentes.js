import { modals } from './admin-utils.js';

let oferentes = [];

export async function cargarOferentes() {
  const response = await fetch('/api/oferentes');
  oferentes = await response.json();
  mostrarOferentes(oferentes);
}

async function mostrarOferentes(data) {
  const tbody = document.getElementById('oferentesBody');
  tbody.textContent = '';

  for (const o of data) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${o.id}</td>
      <td>${o.nombre}</td>
      <td>
        <button class="btn-editar btn-primary">Editar</button>
        <button class="btn-eliminar btn-danger">Eliminar</button>
      </td>
    `;
    
    tr.querySelector('.btn-editar').onclick = () => editarOferente(o.id);
    tr.querySelector('.btn-eliminar').onclick = () => eliminarOferente(o.id);
    
    tbody.appendChild(tr);
  }
}

export function nuevoOferente() {
  document.getElementById('modalOferenteTitulo').textContent = 'Nuevo Oferente';
  document.getElementById('oferenteForm').reset();
  document.getElementById('oferenteId').value = '';
  document.getElementById('modalOferente').style.display = 'block';
}

function editarOferente(id) {
  const oferente = oferentes.find(o => o.id === id);
  if (!oferente) return;

  document.getElementById('modalOferenteTitulo').textContent = 'Editar Oferente';
  document.getElementById('oferenteId').value = oferente.id;
  document.getElementById('oferenteNombre').value = oferente.nombre;
  document.getElementById('modalOferente').style.display = 'block';
}

export async function guardarOferente(e) {
  e.preventDefault();
  const id = document.getElementById('oferenteId').value;
  const nombre = document.getElementById('oferenteNombre').value;

  const url = id ? `/api/oferentes/${id}` : '/api/oferentes';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    document.getElementById('modalOferente').style.display = 'none';
    cargarOferentes();
    modals.showMessage('Éxito', id ? 'Oferente actualizado' : 'Oferente creado', 'success');
  } else {
    modals.showMessage('Error', result.error, 'error');
  }
}

async function eliminarOferente(id) {
  modals.showConfirm('¿Eliminar este oferente?', async () => {
    const response = await fetch(`/api/oferentes/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      cargarOferentes();
      modals.showMessage('Éxito', 'Oferente eliminado', 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  });
}

export async function subirExcelOferentes() {
  const fileInput = document.getElementById('excelOferentes');
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/cargar-oferentes', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', '✓ ' + result.message, 'success');
      cargarOferentes();
    } else {
      modals.showMessage('Mensaje', '✗ Error: ' + result.error, 'success');
    }
  } catch (error) {
    modals.showMessage('Mensaje', '✗ Error: ' + error.message, 'success');
  }
  fileInput.value = '';
}
