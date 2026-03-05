import { modals } from './admin-utils.js';

let catalogoData = { productos: [], total: 0, page: 1, total_pages: 1 };
let catalogoPaginaActual = 1;

export function buscarCatalogo() {
  cargarCatalogo(1);
}

export async function cargarCatalogo(page = 1) {
  const search = document.getElementById('searchCatalogo')?.value || '';
  const url = `/api/catalogo?page=${page}&per_page=50&search=${encodeURIComponent(search)}`;

  const response = await fetch(url);
  catalogoData = await response.json();
  catalogoData.page = parseInt(catalogoData.page);
  catalogoData.total_pages = parseInt(catalogoData.total_pages);
  catalogoPaginaActual = catalogoData.page;

  mostrarCatalogo();
}

function mostrarCatalogo() {
  const tbody = document.getElementById('catalogoBody');
  tbody.innerHTML = '';

  catalogoData.productos.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <button onclick="window.editarProductoCatalogo(${p.id})" class="btn-primary">Editar</button>
      </td>
      <td>${p.numero_registro}</td>
      <td>${p.cod_monodroga !== null && p.cod_monodroga !== undefined ? p.cod_monodroga : '-'}</td>
      <td>${p.monodroga}</td>
      <td>${p.cod_laboratorio !== null && p.cod_laboratorio !== undefined ? p.cod_laboratorio : '-'}</td>
      <td>${p.laboratorio || '-'}</td>
      <td>${p.marca}</td>
      <td>${p.presentacion}</td>
      <td>${p.multidosis !== null && p.multidosis !== undefined ? p.multidosis : '-'}</td>
      <td>${p.precio_caja ? '$' + p.precio_caja.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '-'}</td>
      <td>${p.precio_unitario ? '$' + p.precio_unitario.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '-'}</td>
      <td>${p.fecha || '-'}</td>
      <td>${p.troquel || '-'}</td>
      <td>${p.cod_ab !== null && p.cod_ab !== undefined ? p.cod_ab : '-'}</td>
      <td>${p.troquel_ean || '-'}</td>
    `;
    tbody.appendChild(tr);
  });

  actualizarInfoCatalogo();
  actualizarPaginacionCatalogo();
  sincronizarScrolls();
}

function sincronizarScrolls() {
  const container = document.getElementById('catalogoScrollContainer');
  const scrollTop = document.querySelector('#catalogoScrollTop').parentElement;
  const table = container.querySelector('table');

  document.getElementById('catalogoScrollTop').style.width = table.offsetWidth + 'px';

  container.addEventListener('scroll', () => {
    scrollTop.scrollLeft = container.scrollLeft;
  });

  scrollTop.addEventListener('scroll', () => {
    container.scrollLeft = scrollTop.scrollLeft;
  });
}

function actualizarInfoCatalogo() {
  const info = document.getElementById('catalogoInfo');
  if (info) {
    const inicio = (catalogoData.page - 1) * 50 + 1;
    const fin = Math.min(catalogoData.page * 50, catalogoData.total);
    info.textContent = `Mostrando ${inicio}-${fin} de ${catalogoData.total} productos`;
  }
}

function actualizarPaginacionCatalogo() {
  let paginacion = document.getElementById('catalogoPaginacion');
  if (!paginacion) {
    const tabContent = document.getElementById('tab-catalogo');
    if (!tabContent) return;
    paginacion = document.createElement('div');
    paginacion.id = 'catalogoPaginacion';
    paginacion.style.cssText = 'margin-top: 15px; padding: 10px; text-align: center; background: #f5f5f5; border-radius: 4px;';
    tabContent.appendChild(paginacion);
  }

  let html = `<span>Página ${catalogoData.page} de ${catalogoData.total_pages}</span> `;

  if (catalogoData.page > 1) {
    html += `<button onclick="window.cargarCatalogo(1)" class="btn-secondary">« Primera</button> `;
    html += `<button onclick="window.cargarCatalogo(${catalogoData.page - 1})" class="btn-secondary">‹ Anterior</button> `;
  }

  html += `<input type="number" id="irPaginaCatalogo" min="1" max="${catalogoData.total_pages}" value="${catalogoData.page}" style="width: 60px; padding: 4px; margin: 0 5px; text-align: center;"> `;
  html += `<button onclick="window.irAPaginaCatalogo()" class="btn-secondary">Ir</button> `;

  if (catalogoData.page < catalogoData.total_pages) {
    html += `<button onclick="window.cargarCatalogo(${catalogoData.page + 1})" class="btn-secondary">Siguiente ›</button> `;
    html += `<button onclick="window.cargarCatalogo(${catalogoData.total_pages})" class="btn-secondary">Última »</button>`;
  }

  paginacion.innerHTML = html;
}

window.cargarCatalogo = cargarCatalogo;
window.irAPaginaCatalogo = function() {
  const pagina = parseInt(document.getElementById('irPaginaCatalogo').value);
  if (pagina >= 1 && pagina <= catalogoData.total_pages) {
    cargarCatalogo(pagina);
  }
};

export function nuevoProductoCatalogo() {
  document.getElementById('productoCatalogoForm').reset();
  document.getElementById('productoId').value = '';
  document.getElementById('modalProductoCatalogo').style.display = 'block';
}

window.editarProductoCatalogo = async function(id) {
  let producto = catalogoData.productos.find(p => p.id === id);
  if (!producto) {
    const response = await fetch(`/api/catalogo/${id}`);
    producto = await response.json();
  }

  document.getElementById('productoId').value = producto.id;
  document.getElementById('productoNumeroRegistro').value = producto.numero_registro;
  document.getElementById('productoMonodroga').value = producto.monodroga;
  document.getElementById('productoMarca').value = producto.marca;
  document.getElementById('productoPresentacion').value = producto.presentacion;
  document.getElementById('productoLaboratorio').value = producto.laboratorio || '';
  document.getElementById('productoPrecioCaja').value = producto.precio_caja || '';
  document.getElementById('productoPrecioUnitario').value = producto.precio_unitario || '';
  document.getElementById('productoCostoUnitario').value = producto.costo_unitario || '';

  if (producto.fecha) {
    const partes = producto.fecha.split('/');
    if (partes.length === 3) {
      document.getElementById('productoFecha').value = `${partes[2]}-${partes[1]}-${partes[0]}`;
    } else {
      document.getElementById('productoFecha').value = producto.fecha;
    }
  } else {
    document.getElementById('productoFecha').value = '';
  }

  document.getElementById('modalProductoCatalogo').style.display = 'block';
};

export async function guardarProductoCatalogo(e) {
  e.preventDefault();

  const id = document.getElementById('productoId').value;
  const data = {
    numero_registro: document.getElementById('productoNumeroRegistro').value,
    monodroga: document.getElementById('productoMonodroga').value,
    marca: document.getElementById('productoMarca').value,
    presentacion: document.getElementById('productoPresentacion').value,
    laboratorio: document.getElementById('productoLaboratorio').value,
    precio_caja: document.getElementById('productoPrecioCaja').value,
    precio_unitario: document.getElementById('productoPrecioUnitario').value,
    costo_unitario: document.getElementById('productoCostoUnitario').value,
    fecha: document.getElementById('productoFecha').value
  };

  try {
    const url = id ? `/api/catalogo/${id}` : '/api/catalogo';
    const method = id ? 'PUT' : 'POST';

    const response = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
      modals.showMessage('Mensaje', id ? 'Producto actualizado' : 'Producto agregado', 'success');
      document.getElementById('modalProductoCatalogo').style.display = 'none';
      cargarCatalogo();
    } else {
      modals.showMessage('Mensaje', 'Error: ' + result.error, 'success');
    }
  } catch (error) {
    modals.showMessage('Mensaje', 'Error: ' + error.message, 'success');
  }
}

export async function subirExcel() {
  const fileInput = document.getElementById('excelFile');
  const file = fileInput.files[0];

  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  modals.showProgress('Iniciando...', 0, 100);

  try {
    const response = await fetch('/api/cargar-catalogo', {
      method: 'POST',
      body: formData
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.substring(6));

          if (data.error) {
            modals.hideProgress();
            modals.showMessage('Error al cargar catálogo', data.error, 'error');
            return;
          }

          if (data.done) {
            modals.hideProgress();
            modals.showMessage('✓ Catálogo cargado exitosamente', `Se procesaron ${data.total} productos correctamente`, 'success');
            cargarCatalogo();
          } else {
            modals.updateProgress(data.message, data.progress, data.total);
          }
        }
      }
    }
  } catch (error) {
    modals.hideProgress();
    modals.showMessage('Error', 'Error al cargar archivo: ' + error.message, 'error');
  }

  fileInput.value = '';
}
