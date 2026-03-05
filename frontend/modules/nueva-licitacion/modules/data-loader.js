// Módulo para cargar datos iniciales
export let catalogoProductos = [];
export let clientes = [];
export let oferentes = [];
export let marcas = [];
export let tiposLicitacion = [];
export let motivosPerdida = [];

export async function cargarCatalogo() {
  const response = await fetch('/api/catalogo?per_page=100000');
  const data = await response.json();
  catalogoProductos = data.productos || [];
}

export async function cargarClientes() {
  const response = await fetch('/api/clientes');
  clientes = await response.json();
  const select = document.getElementById('clienteSelect');
  select.innerHTML = '<option value="">Seleccione cliente...</option>';
  clientes.forEach(c => {
    const option = document.createElement('option');
    option.value = c.id;
    option.textContent = c.nombre;
    option.dataset.organismo = c.organismo_jurisdiccion || '';
    select.appendChild(option);
  });
}

export async function cargarOferentes() {
  const response = await fetch('/api/oferentes');
  oferentes = await response.json();
}

export async function cargarMarcas() {
  const response = await fetch('/api/marcas');
  marcas = await response.json();
}

export async function cargarTiposLicitacion() {
  const response = await fetch('/api/tipos-licitacion');
  tiposLicitacion = await response.json();
  const select = document.getElementById('tipoLicitacionSelect');
  select.innerHTML = '<option value="">Seleccione tipo...</option>';
  tiposLicitacion.forEach(t => {
    const option = document.createElement('option');
    option.value = t.id;
    option.textContent = t.nombre;
    select.appendChild(option);
  });
}

export async function cargarPortalesOrigen() {
  const response = await fetch('/api/portales-origen');
  const portales = await response.json();
  const select = document.getElementById('portalOrigen');
  select.innerHTML = '<option value="">Seleccione...</option>';
  portales.forEach(p => {
    const option = document.createElement('option');
    option.value = p.nombre;
    option.textContent = p.nombre;
    select.appendChild(option);
  });
}

export async function cargarModalidadesEntrega() {
  const response = await fetch('/api/modalidades-entrega');
  const modalidades = await response.json();
  const select = document.getElementById('modalidadEntrega');
  select.innerHTML = '<option value="">Seleccione...</option>';
  modalidades.forEach(m => {
    const option = document.createElement('option');
    option.value = m.nombre;
    option.textContent = m.nombre;
    select.appendChild(option);
  });
}

export async function cargarFormasPago() {
  const response = await fetch('/api/formas-pago');
  const formas = await response.json();
  const select = document.getElementById('formaPago');
  select.innerHTML = '<option value="">Seleccione...</option>';
  formas.forEach(f => {
    const option = document.createElement('option');
    option.value = f.nombre;
    option.textContent = f.nombre;
    select.appendChild(option);
  });
}

export async function cargarMantenimientosOferta() {
  const response = await fetch('/api/mantenimientos-oferta');
  const mantenimientos = await response.json();
  const select = document.getElementById('mantenimientoOferta');
  select.innerHTML = '<option value="">Seleccione...</option>';
  mantenimientos.forEach(m => {
    const option = document.createElement('option');
    option.value = m.nombre;
    option.textContent = m.nombre;
    select.appendChild(option);
  });
}

export async function cargarMotivosPerdida() {
  const response = await fetch('/api/motivos-perdida');
  motivosPerdida = await response.json();
}
