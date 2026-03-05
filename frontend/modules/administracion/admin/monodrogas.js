import { modals } from './admin-utils.js';

let monodrogas = [];
let monodrogasPaginacion = { pagina: 1, por_pagina: 50, total_paginas: 1 };

export async function cargarMonodrogas(pagina = 1) {
  const search = document.getElementById('searchMonodroga')?.value || '';
  const response = await fetch(`/api/monodrogas?pagina=${pagina}&por_pagina=50&search=${encodeURIComponent(search)}`);
  const resultado = await response.json();

  monodrogas = resultado.datos || [];
  monodrogasPaginacion = {
    pagina: resultado.pagina,
    por_pagina: resultado.por_pagina,
    total: resultado.total,
    total_paginas: resultado.total_paginas
  };

  const tbody = document.getElementById('monodrogasBody');
  tbody.innerHTML = '';
  monodrogas.forEach(m => {
    tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
      <button onclick="window.editarMonodroga(${m.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarMonodroga(${m.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });

  actualizarPaginacionMonodrogas();
}

export function buscarMonodroga() {
  cargarMonodrogas(1);
}

function actualizarPaginacionMonodrogas() {
  const paginationDiv = document.getElementById('monodrogasPaginacion');
  if (!paginationDiv) return;

  let html = `<p>Página ${monodrogasPaginacion.pagina} de ${monodrogasPaginacion.total_paginas} (Total: ${monodrogasPaginacion.total})</p>`;
  html += '<div style="margin-top: 10px;">';

  if (monodrogasPaginacion.pagina > 1) {
    html += `<button onclick="window.cargarMonodrogas(1)" style="margin: 5px;">Primera</button>`;
    html += `<button onclick="window.cargarMonodrogas(${monodrogasPaginacion.pagina - 1})" style="margin: 5px;">Anterior</button>`;
  }

  if (monodrogasPaginacion.pagina < monodrogasPaginacion.total_paginas) {
    html += `<button onclick="window.cargarMonodrogas(${monodrogasPaginacion.pagina + 1})" style="margin: 5px;">Siguiente</button>`;
    html += `<button onclick="window.cargarMonodrogas(${monodrogasPaginacion.total_paginas})" style="margin: 5px;">Última</button>`;
  }

  html += '</div>';
  paginationDiv.innerHTML = html;
}

window.cargarMonodrogas = cargarMonodrogas;

export function nuevaMonodroga() {
  document.getElementById('modalMonodrogaTitulo').textContent = 'Nueva Monodroga';
  document.getElementById('monodrogaForm').reset();
  document.getElementById('monodrogaId').value = '';
  document.getElementById('modalMonodroga').style.display = 'block';
}

window.editarMonodroga = function(id) {
  const monodroga = monodrogas.find(m => m.id === id);
  if (!monodroga) return;

  document.getElementById('modalMonodrogaTitulo').textContent = 'Editar Monodroga';
  document.getElementById('monodrogaId').value = monodroga.id;
  document.getElementById('monodrogaNombre').value = monodroga.nombre;
  document.getElementById('modalMonodroga').style.display = 'block';
};

export async function guardarMonodroga(e) {
  e.preventDefault();
  const id = document.getElementById('monodrogaId').value;
  const nombre = document.getElementById('monodrogaNombre').value;

  const url = id ? `/api/monodrogas/${id}` : '/api/monodrogas';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    document.getElementById('modalMonodroga').style.display = 'none';
    cargarMonodrogas();
    modals.showMessage('Éxito', id ? 'Monodroga actualizada' : 'Monodroga creada', 'success');
  } else {
    modals.showMessage('Error', result.error, 'error');
  }
}

export async function subirExcelMonodrogas() {
  const fileInput = document.getElementById('excelMonodrogas');
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/cargar-monodrogas', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (result.success) {
      cargarMonodrogas();
      modals.showMessage('Éxito', result.message, 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  } catch (error) {
    modals.showMessage('Error', error.message, 'error');
  }
  fileInput.value = '';
}

window.eliminarMonodroga = async function(id) {
  if (!Number.isInteger(id) || id <= 0) {
    modals.showMessage('Error', 'ID inválido', 'error');
    return;
  }
  modals.showConfirm('¿Eliminar esta monodroga?', async () => {
    const response = await fetch(`/api/monodrogas/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      cargarMonodrogas();
      modals.showMessage('Éxito', 'Monodroga eliminada', 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  });
};
