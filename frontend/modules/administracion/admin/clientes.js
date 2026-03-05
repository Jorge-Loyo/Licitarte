import { modals } from './admin-utils.js';

let clientes = [];

export async function cargarClientes() {
  try {
    const response = await fetch('/api/clientes');
    clientes = await response.json();
    mostrarClientes(clientes);
  } catch (error) {
    modals.showMessage('Error', 'Error al cargar clientes: ' + error.message, 'error');
  }
}

async function mostrarClientes(data) {
  const tbody = document.getElementById('clientesBody');
  tbody.textContent = '';

  for (const c of data) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${c.id}</td>
      <td>${c.nombre}</td>
      <td>${c.razon_social || '-'}</td>
      <td>${c.cuit || '-'}</td>
      <td>${c.telefono || '-'}</td>
      <td>${c.email || '-'}</td>
      <td>
        <button class="btn-editar btn-primary">Editar</button>
        <button class="btn-eliminar btn-danger">Eliminar</button>
      </td>
    `;
    
    tr.querySelector('.btn-editar').onclick = () => editarCliente(c.id);
    tr.querySelector('.btn-eliminar').onclick = () => eliminarCliente(c.id);
    
    tbody.appendChild(tr);
  }
}

export async function nuevoCliente() {
  await cargarOrganismosSelect();
  document.getElementById('modalClienteTitulo').textContent = 'Nuevo Cliente';
  document.getElementById('clienteForm').reset();
  document.getElementById('clienteId').value = '';
  document.getElementById('modalCliente').style.display = 'block';
}

async function editarCliente(id) {
  await cargarOrganismosSelect();
  const cliente = clientes.find(c => c.id === id);
  if (!cliente) return;

  document.getElementById('modalClienteTitulo').textContent = 'Editar Cliente';
  document.getElementById('clienteId').value = cliente.id;
  document.getElementById('clienteNombre').value = cliente.nombre;
  document.getElementById('clienteOrganismo').value = cliente.organismo_jurisdiccion || '';
  document.getElementById('clienteRazonSocial').value = cliente.razon_social || '';
  document.getElementById('clienteCuit').value = cliente.cuit || '';
  document.getElementById('clienteDireccion').value = cliente.direccion || '';
  document.getElementById('clienteTelefono').value = cliente.telefono || '';
  document.getElementById('clienteEmail').value = cliente.email || '';
  document.getElementById('modalCliente').style.display = 'block';
}

async function cargarOrganismosSelect() {
  const response = await fetch('/api/organismos');
  const organismos = await response.json();
  const select = document.getElementById('clienteOrganismo');
  select.innerHTML = '<option value="">Seleccione...</option>';
  organismos.forEach(o => {
    select.innerHTML += `<option value="${o.nombre}">${o.nombre}</option>`;
  });
}

export async function guardarCliente(e) {
  e.preventDefault();
  const id = document.getElementById('clienteId').value;
  const organismoValue = document.getElementById('clienteOrganismo').value;

  if (!organismoValue || organismoValue.trim() === '') {
    modals.showMessage('Error', 'Debe seleccionar un Organismo/Jurisdicción', 'error');
    return;
  }

  const data = {
    nombre: document.getElementById('clienteNombre').value,
    organismo_jurisdiccion: organismoValue,
    razon_social: document.getElementById('clienteRazonSocial').value,
    cuit: document.getElementById('clienteCuit').value,
    direccion: document.getElementById('clienteDireccion').value,
    telefono: document.getElementById('clienteTelefono').value,
    email: document.getElementById('clienteEmail').value
  };

  const url = id ? `/api/clientes/${id}` : '/api/clientes';
  const method = id ? 'PUT' : 'POST';

  try {
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();

    if (result.success) {
      modals.showMessage('Éxito', id ? 'Cliente actualizado' : 'Cliente creado', 'success');
      document.getElementById('modalCliente').style.display = 'none';
      cargarClientes();
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  } catch (error) {
    modals.showMessage('Error', 'Error de conexión: ' + error.message, 'error');
  }
}

async function eliminarCliente(id) {
  if (!Number.isInteger(id) || id <= 0) {
    modals.showMessage('Error', 'ID inválido', 'error');
    return;
  }
  modals.showConfirm('¿Eliminar este cliente?', async () => {
    const response = await fetch(`/api/clientes/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) {
      cargarClientes();
      modals.showMessage('Éxito', 'Cliente eliminado', 'success');
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  });
}

export async function subirExcelClientes() {
  const fileInput = document.getElementById('excelClientes');
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/cargar-clientes', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (result.success) {
      modals.showMessage('Éxito', result.message, 'success');
      cargarClientes();
    } else {
      modals.showMessage('Error', result.error, 'error');
    }
  } catch (error) {
    modals.showMessage('Error', error.message, 'error');
  }
  fileInput.value = '';
}
