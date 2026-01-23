let clientes = [];
let oferentes = [];
let marcas = [];
let tiposLicitacion = [];
let catalogoCompleto = [];

function mostrarTab(tab) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(`tab-${tab}`).classList.add('active');
    event.target.classList.add('active');
    
    if (tab === 'clientes') cargarClientes();
    if (tab === 'oferentes') cargarOferentes();
    if (tab === 'marcas') cargarMarcas();
    if (tab === 'tipos') cargarTipos();
    if (tab === 'catalogo') cargarCatalogo();
}

// Gestión Clientes
async function cargarClientes() {
    try {
        const response = await fetch('/api/clientes');
        console.log('Clientes response status:', response.status);
        clientes = await response.json();
        console.log('Clientes cargados:', clientes.length);
        mostrarClientes(clientes);
    } catch (error) {
        console.error('Error cargando clientes:', error);
        alert('Error al cargar clientes: ' + error.message);
    }
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
    
    console.log('Enviando datos:', data);
    
    const url = id ? `/api/clientes/${id}` : '/api/clientes';
    const method = id ? 'PUT' : 'POST';
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        console.log('Response status:', response.status);
        const result = await response.json();
        console.log('Response data:', result);
        
        if (result.success) {
            alert(id ? 'Cliente actualizado' : 'Cliente creado');
            cerrarModalCliente();
            cargarClientes();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error en fetch:', error);
        alert('Error de conexión: ' + error.message);
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

// Gestión Oferentes
async function cargarOferentes() {
    const response = await fetch('/api/oferentes');
    oferentes = await response.json();
    mostrarOferentes(oferentes);
}

function mostrarOferentes(data) {
    const tbody = document.getElementById('oferentesBody');
    tbody.innerHTML = '';
    
    data.forEach(o => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${o.id}</td>
            <td>${o.nombre}</td>
            <td>
                <button onclick="editarOferente(${o.id})" class="btn-primary">Editar</button>
                <button onclick="eliminarOferente(${o.id})" class="btn-danger">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function nuevoOferente() {
    const nombre = prompt('Nombre del oferente:');
    if (!nombre) return;
    
    fetch('/api/oferentes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert('Oferente creado');
            cargarOferentes();
        } else {
            alert('Error: ' + result.error);
        }
    });
}

function editarOferente(id) {
    const oferente = oferentes.find(o => o.id === id);
    if (!oferente) return;
    
    const nombre = prompt('Nombre del oferente:', oferente.nombre);
    if (!nombre) return;
    
    fetch(`/api/oferentes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert('Oferente actualizado');
            cargarOferentes();
        } else {
            alert('Error: ' + result.error);
        }
    });
}

async function eliminarOferente(id) {
    if (!confirm('¿Eliminar este oferente?')) return;
    
    const response = await fetch(`/api/oferentes/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        alert('Oferente eliminado');
        cargarOferentes();
    } else {
        alert('Error: ' + result.error);
    }
}

// Gestión Marcas
async function cargarMarcas() {
    const response = await fetch('/api/marcas');
    marcas = await response.json();
    mostrarMarcas(marcas);
}

function mostrarMarcas(data) {
    const tbody = document.getElementById('marcasBody');
    tbody.innerHTML = '';
    
    data.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${m.id}</td>
            <td>${m.nombre}</td>
            <td>
                <button onclick="editarMarca(${m.id})" class="btn-primary">Editar</button>
                <button onclick="eliminarMarca(${m.id})" class="btn-danger">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function nuevaMarca() {
    const nombre = prompt('Nombre de la marca:');
    if (!nombre) return;
    
    fetch('/api/marcas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert('Marca creada');
            cargarMarcas();
        } else {
            alert('Error: ' + result.error);
        }
    });
}

function editarMarca(id) {
    const marca = marcas.find(m => m.id === id);
    if (!marca) return;
    
    const nombre = prompt('Nombre de la marca:', marca.nombre);
    if (!nombre) return;
    
    fetch(`/api/marcas/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert('Marca actualizada');
            cargarMarcas();
        } else {
            alert('Error: ' + result.error);
        }
    });
}

async function eliminarMarca(id) {
    if (!confirm('¿Eliminar esta marca?')) return;
    
    const response = await fetch(`/api/marcas/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        alert('Marca eliminada');
        cargarMarcas();
    } else {
        alert('Error: ' + result.error);
    }
}

// Gestión Tipos de Licitación
async function cargarTipos() {
    const response = await fetch('/api/tipos-licitacion');
    tiposLicitacion = await response.json();
    mostrarTipos(tiposLicitacion);
}

function mostrarTipos(data) {
    const tbody = document.getElementById('tiposBody');
    tbody.innerHTML = '';
    
    data.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${t.id}</td>
            <td>${t.nombre}</td>
            <td>
                <button onclick="editarTipo(${t.id})" class="btn-primary">Editar</button>
                <button onclick="eliminarTipo(${t.id})" class="btn-danger">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function nuevoTipo() {
    const nombre = prompt('Nombre del tipo de licitación:');
    if (!nombre) return;
    
    fetch('/api/tipos-licitacion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert('Tipo creado');
            cargarTipos();
        } else {
            alert('Error: ' + result.error);
        }
    });
}

function editarTipo(id) {
    const tipo = tiposLicitacion.find(t => t.id === id);
    if (!tipo) return;
    
    const nombre = prompt('Nombre del tipo de licitación:', tipo.nombre);
    if (!nombre) return;
    
    fetch(`/api/tipos-licitacion/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert('Tipo actualizado');
            cargarTipos();
        } else {
            alert('Error: ' + result.error);
        }
    });
}

async function eliminarTipo(id) {
    if (!confirm('¿Eliminar este tipo de licitación?')) return;
    
    const response = await fetch(`/api/tipos-licitacion/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        alert('Tipo eliminado');
        cargarTipos();
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

async function subirExcel() {
    const fileInput = document.getElementById('excelFile');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/cargar-catalogo', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✓ Catálogo cargado exitosamente');
            cargarCatalogo();
        } else {
            alert('✗ Error: ' + result.error);
        }
    } catch (error) {
        alert('✗ Error al cargar archivo: ' + error.message);
    }
    
    fileInput.value = '';
}

document.addEventListener('DOMContentLoaded', () => {
    cargarClientes();
});
