import { modals } from './admin-utils.js';

let laboratorios = [];
let laboratoriosPaginacion = { pagina: 1, por_pagina: 50, total_paginas: 1 };

export async function cargarLaboratorios(pagina = 1) {
  const response = await fetch(`/api/laboratorios?pagina=${pagina}&por_pagina=50`);
  const resultado = await response.json();

  laboratorios = resultado.datos || [];
  laboratoriosPaginacion = {
    pagina: resultado.pagina,
    por_pagina: resultado.por_pagina,
    total: resultado.total,
    total_paginas: resultado.total_paginas
  };

  const tbody = document.getElementById('laboratoriosBody');
  tbody.innerHTML = '';
  laboratorios.forEach(l => {
    tbody.innerHTML += `<tr><td>${l.id}</td><td>${l.nombre}</td><td>
      <button onclick="window.editarLaboratorio(${l.id})" class="btn-primary">Editar</button>
      <button onclick="window.eliminarLaboratorio(${l.id})" class="btn-danger">Eliminar</button>
    </td></tr>`;
  });

  actualizarPaginacionLaboratorios();
}

function actualizarPaginacionLaboratorios() {
  const paginationDiv = document.getElementById('laboratoriosPaginacion');
  if (!paginationDiv) return;

  let html = `<p>Página ${laboratoriosPaginacion.pagina} de ${laboratoriosPaginacion.total_paginas} (Total: ${laboratoriosPaginacion.total})</p>`;
  html += '<div style="margin-top: 10px;">';

  if (laboratoriosPaginacion.pagina > 1) {
    html += `<button onclick="window.cargarLaboratorios(1)" style="margin: 5px;">Primera</button>`;
    html += `<button onclick="window.cargarLaboratorios(${laboratoriosPaginacion.pagina - 1})" style="margin: 5px;">Anterior</button>`;
  }

  if (laboratoriosPaginacion.pagina < laboratoriosPaginacion.total_paginas) {
    html += `<button onclick="window.cargarLaboratorios(${laboratoriosPaginacion.pagina + 1})" style="margin: 5px;">Siguiente</button>`;
    html += `<button onclick="window.cargarLaboratorios(${laboratoriosPaginacion.total_paginas})" style="margin: 5px;">Última</button>`;
  }

  html += '</div>';
  paginationDiv.innerHTML = html;
}

window.cargarLaboratorios = cargarLaboratorios;

export function nuevoLaboratorio() {
  document.getElementById('modalLaboratorioTitulo').textContent = 'Nuevo Laboratorio';
  document.getElementById('laboratorioForm').reset();
  document.getElementById('laboratorioId').value = '';
  document.getElementById('modalLaboratorio').style.display = 'block';
}

window.editarLaboratorio = function(id) {
  const laboratorio = laboratorios.find(l => l.id === id);
  if (!laboratorio) return;

  document.getElementById('modalLaboratorioTitulo').textContent = 'Editar Laboratorio';
  document.getElementById('laboratorioId').value = laboratorio.id;
  document.getElementById('laboratorioNombre').value = laboratorio.nombre;
  document.getElementById('modalLaboratorio').style.display = 'block';
};

export async function guardarLaboratorio(e) {
  e.preventDefault();
  const id = document.getElementById('laboratorioId').value;
  const nombre = document.getElementById('laboratorioNombre').value;

  const url = id ? `/api/laboratorios/${id}` : '/api/laboratorios';
  const method = id ? 'PUT' : 'POST';

  const response = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  const result = await response.json();
  if (result.success) {
    document.getElementById('modalLaboratorio').style.display = 'none';
    cargarLaboratorios();
    modals.showMessage('Éxito', id ? 'Laboratorio actualizado' : 'Laboratorio creado', 'success');
  } else {
    modals.showMessage('Error', result.error, 'error');
  }
}

window.eliminarLaboratorio = async function(id) {
  modals.showConfirm('¿Eliminar este laboratorio?', async () => {
    const response = await fetch(`/api/laboratorios/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      cargarLaboratorios();
      modals.showMessage('Éxito', 'Laboratorio eliminado', 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  });
};

export async function subirExcelLaboratorios() {
  const fileInput = document.getElementById('excelLaboratorios');
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/cargar-laboratorios', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (result.success) {
      cargarLaboratorios();
      modals.showMessage('Éxito', result.message, 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  } catch (error) {
    modals.showMessage('Error', error.message, 'error');
  }
  fileInput.value = '';
}
