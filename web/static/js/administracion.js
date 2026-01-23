let clientes = [];
let catalogoCompleto = [];

function mostrarTab(tab) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(`tab-${tab}`).classList.add('active');
    event.target.classList.add('active');
    
    if (tab === 'clientes') cargarClientes();
    if (tab === 'catalogo') cargarCatalogo();
}

// Gestión Clientes
async function cargarClientes() {
    const response = await fetch('/api/clientes');
    clientes = await response.json();
    mostrarClientes(clientes);
}

function mostrarClientes(data) {
    const tbody = document.getElementById('clientesBody');
    tbody.innerHTML = '';
    
    data.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${c.id}</td>
            <td>${c.nombre}</td>
            <td>${c.razon_social || '-'}</td>
            <td>${c.cuit || '-'}</td>
            <td>${c.telefono || '-'}</td>
            <td>${c.email || '-'}</td>
            <td>
                <button onclick="editarCliente(${c.id})" class="btn-primary">Editar</button>
                <button onclick="eliminarCliente(${c.id})" class="btn-danger">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function nuevoCliente() {
    document.getElementById('modalClienteTitulo').textContent = 'Nuevo Cliente';
    document.getElementById('clienteForm').reset();
    document.getElementById('clienteId').value = '';
    document.getElementById('modalCliente').style.display = 'block';
}

function editarCliente(id) {
    const cliente = clientes.find(c => c.id === id);
    if (!cliente) return;
    
    document.getElementById('modalClienteTitulo').textContent = 'Editar Cliente';
    document.getElementById('clienteId').value = cliente.id;
    document.getElementById('clienteNombre').value = cliente.nombre;
    document.getElementById('clienteRazonSocial').value = cliente.razon_social || '';
    document.getElementById('clienteCuit').value = cliente.cuit || '';
    document.getElementById('clienteDireccion').value = cliente.direccion || '';
    document.getElementById('clienteTelefono').value = cliente.telefono || '';
    document.getElementById('clienteEmail').value = cliente.email || '';
    document.getElementById('modalCliente').style.display = 'block';
}

function cerrarModalCliente() {
    document.getElementById('modalCliente').style.display = 'none';
}

document.getElementById('clienteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('clienteId').value;
    const data = {
        nombre: document.getElementById('clienteNombre').value,
        razon_social: document.getElementById('clienteRazonSocial').value,
        cuit: document.getElementById('clienteCuit').value,
        direccion: document.getElementById('clienteDireccion').value,
        telefono: document.getElementById('clienteTelefono').value,
        email: document.getElementById('clienteEmail').value
    };
    
    const url = id ? `/api/clientes/${id}` : '/api/clientes';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Cliente actualizado' : 'Cliente creado');
        cerrarModalCliente();
        cargarClientes();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarCliente(id) {
    if (!confirm('¿Eliminar este cliente?')) return;
    
    const response = await fetch(`/api/clientes/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        alert('Cliente eliminado');
        cargarClientes();
    } else {
        alert('Error: ' + result.error);
    }
}

// Gestión Catálogo
async function cargarCatalogo() {
    const response = await fetch('/api/catalogo');
    catalogoCompleto = await response.json();
    mostrarCatalogo(catalogoCompleto);
}

function mostrarCatalogo(data) {
    const tbody = document.getElementById('catalogoBody');
    tbody.innerHTML = '';
    
    data.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.numero_registro}</td>
            <td>${p.monodroga}</td>
            <td>${p.marca}</td>
            <td>${p.presentacion}</td>
            <td>${p.laboratorio || '-'}</td>
            <td>${p.precio_caja ? '$' + p.precio_caja.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '-'}</td>
            <td>${p.precio_unitario ? '$' + p.precio_unitario.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '-'}</td>
            <td>${p.fecha || '-'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function filtrarCatalogo() {
    const search = document.getElementById('searchCatalogo').value.toLowerCase();
    const filtrado = catalogoCompleto.filter(p => 
        p.monodroga.toLowerCase().includes(search) ||
        p.marca.toLowerCase().includes(search) ||
        p.presentacion.toLowerCase().includes(search) ||
        (p.laboratorio && p.laboratorio.toLowerCase().includes(search))
    );
    mostrarCatalogo(filtrado);
}

async function recargarCatalogo() {
    if (!confirm('¿Recargar catálogo desde Excel? Esto puede tardar unos segundos.')) return;
    
    alert('Función de recarga desde servidor. Implementar endpoint si es necesario.');
}

document.addEventListener('DOMContentLoaded', () => {
    cargarClientes();
});
