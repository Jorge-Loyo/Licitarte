import { modals } from './admin-utils.js';

let marcas = [];

export async function cargarMarcas() {
  const response = await fetch('/api/marcas');
  marcas = await response.json();
  mostrarMarcas(marcas);
}

async function mostrarMarcas(data) {
  const tbody = document.getElementById('marcasBody');
  tbody.textContent = '';

  for (const m of data) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${m.id}</td>
      <td>${m.nombre}</td>
      <td>
        <button class="btn-editar btn-primary">Editar</button>
        <button class="btn-eliminar btn-danger">Eliminar</button>
      </td>
    `;
    
    tr.querySelector('.btn-editar').onclick = () => editarMarca(m.id);
    tr.querySelector('.btn-eliminar').onclick = () => eliminarMarca(m.id);
    
    tbody.appendChild(tr);
  }
}

export function nuevaMarca() {
  document.getElementById('modalMarcaTitulo').textContent = 'Nueva Marca';
  document.getElementById('marcaForm').reset();
  document.getElementById('marcaId').value = '';
  document.getElementById('modalMarca').style.display = 'block';
}

function editarMarca(id) {
  const marca = marcas.find(m => m.id === id);
  if (!marca) return;

  document.getElementById('modalMarcaTitulo').textContent = 'Editar Marca';
  document.getElementById('marcaId').value = marca.id;
  document.getElementById('marcaNombre').value = marca.nombre;
  document.getElementById('modalMarca').style.display = 'block';
}

export async function guardarMarca(e) {
  e.preventDefault();
  const id = document.getElementById('marcaId').value;
  const nombre = document.getElementById('marcaNombre').value;

  const url = id ? `/api/marcas/${id}` : '/api/marcas';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    document.getElementById('modalMarca').style.display = 'none';
    cargarMarcas();
    modals.showMessage('Éxito', id ? 'Marca actualizada' : 'Marca creada', 'success');
  } else {
    modals.showMessage('Error', result.error, 'error');
  }
}

async function eliminarMarca(id) {
  modals.showConfirm('¿Eliminar esta marca?', async () => {
    const response = await fetch(`/api/marcas/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      cargarMarcas();
      modals.showMessage('Éxito', 'Marca eliminada', 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  });
}

export async function subirExcelMarcas() {
  const fileInput = document.getElementById('excelMarcas');
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/cargar-marcas', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (result.success) {
      cargarMarcas();
      modals.showMessage('Éxito', result.message, 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  } catch (error) {
    modals.showMessage('Error', error.message, 'error');
  }
  fileInput.value = '';
}
