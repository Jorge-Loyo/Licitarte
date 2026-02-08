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
    if (tab === 'organismos') cargarOrganismos();
    if (tab === 'portales') cargarPortales();
    if (tab === 'modalidades') cargarModalidades();
    if (tab === 'formas') cargarFormasPago();
    if (tab === 'motivos') cargarMotivosPerdida();
    if (tab === 'mantenimientos') cargarMantenimientos();
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

async function nuevoCliente() {
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

function cerrarModalCliente() {
    document.getElementById('modalCliente').style.display = 'none';
}

document.getElementById('clienteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('clienteId').value;
    const data = {
        nombre: document.getElementById('clienteNombre').value,
        organismo_jurisdiccion: document.getElementById('clienteOrganismo').value,
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

function cerrarModalOferente() {
    document.getElementById('modalOferente').style.display = 'none';
}

document.getElementById('oferenteForm').addEventListener('submit', async (e) => {
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
        alert(id ? 'Oferente actualizado' : 'Oferente creado');
        cerrarModalOferente();
        cargarOferentes();
    } else {
        alert('Error: ' + result.error);
    }
});

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

function cerrarModalMarca() {
    document.getElementById('modalMarca').style.display = 'none';
}

document.getElementById('marcaForm').addEventListener('submit', async (e) => {
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
        alert(id ? 'Marca actualizada' : 'Marca creada');
        cerrarModalMarca();
        cargarMarcas();
    } else {
        alert('Error: ' + result.error);
    }
});

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

function cerrarModalTipo() {
    document.getElementById('modalTipo').style.display = 'none';
}

document.getElementById('tipoForm').addEventListener('submit', async (e) => {
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
        alert(id ? 'Tipo actualizado' : 'Tipo creado');
        cerrarModalTipo();
        cargarTipos();
    } else {
        alert('Error: ' + result.error);
    }
});

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
            <td>${p.costo_unitario ? '$' + p.costo_unitario.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '-'}</td>
            <td>${p.fecha || '-'}</td>
            <td>
                <button onclick="editarProductoCatalogo(${p.id})" class="btn-primary">Editar</button>
            </td>
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

async function subirExcelClientes() {
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
            alert('✓ ' + result.message);
            cargarClientes();
        } else {
            alert('✗ Error: ' + result.error);
        }
    } catch (error) {
        alert('✗ Error: ' + error.message);
    }
    fileInput.value = '';
}

async function subirExcelOferentes() {
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
            alert('✓ ' + result.message);
            cargarOferentes();
        } else {
            alert('✗ Error: ' + result.error);
        }
    } catch (error) {
        alert('✗ Error: ' + error.message);
    }
    fileInput.value = '';
}

async function subirExcelMarcas() {
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
            alert('✓ ' + result.message);
            cargarMarcas();
        } else {
            alert('✗ Error: ' + result.error);
        }
    } catch (error) {
        alert('✗ Error: ' + error.message);
    }
    fileInput.value = '';
}

async function subirExcelTipos() {
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
            alert('✓ ' + result.message);
            cargarTipos();
        } else {
            alert('✗ Error: ' + result.error);
        }
    } catch (error) {
        alert('✗ Error: ' + error.message);
    }
    fileInput.value = '';
}

document.addEventListener('DOMContentLoaded', () => {
    cargarClientes();
});

function nuevoProductoCatalogo() {
    document.getElementById('productoCatalogoForm').reset();
    document.getElementById('productoId').value = '';
    document.getElementById('modalProductoCatalogo').style.display = 'block';
}

function cerrarModalProductoCatalogo() {
    document.getElementById('modalProductoCatalogo').style.display = 'none';
}

document.getElementById('productoCatalogoForm').addEventListener('submit', async (e) => {
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
            alert(id ? 'Producto actualizado' : 'Producto agregado');
            cerrarModalProductoCatalogo();
            cargarCatalogo();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

function editarProductoCatalogo(id) {
    const producto = catalogoCompleto.find(p => p.id === id);
    if (!producto) return;
    
    document.getElementById('productoId').value = producto.id;
    document.getElementById('productoNumeroRegistro').value = producto.numero_registro;
    document.getElementById('productoMonodroga').value = producto.monodroga;
    document.getElementById('productoMarca').value = producto.marca;
    document.getElementById('productoPresentacion').value = producto.presentacion;
    document.getElementById('productoLaboratorio').value = producto.laboratorio || '';
    document.getElementById('productoPrecioCaja').value = producto.precio_caja || '';
    document.getElementById('productoPrecioUnitario').value = producto.precio_unitario || '';
    document.getElementById('productoCostoUnitario').value = producto.costo_unitario || '';
    
    // Convertir fecha de dd/mm/yyyy a yyyy-mm-dd para input type="date"
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
}

// Gestión Portales Origen
let portales = [];
async function cargarPortales() {
    const response = await fetch('/api/portales-origen');
    portales = await response.json();
    const tbody = document.getElementById('portalesBody');
    tbody.innerHTML = '';
    portales.forEach(p => {
        tbody.innerHTML += `<tr><td>${p.id}</td><td>${p.nombre}</td><td>
            <button onclick="editarPortal(${p.id})" class="btn-primary">Editar</button>
            <button onclick="eliminarPortal(${p.id})" class="btn-danger">Eliminar</button>
        </td></tr>`;
    });
}

function nuevoPortal() {
    document.getElementById('modalPortalTitulo').textContent = 'Nuevo Portal/Origen';
    document.getElementById('portalForm').reset();
    document.getElementById('portalId').value = '';
    document.getElementById('modalPortal').style.display = 'block';
}

function editarPortal(id) {
    const portal = portales.find(p => p.id === id);
    if (!portal) return;
    
    document.getElementById('modalPortalTitulo').textContent = 'Editar Portal/Origen';
    document.getElementById('portalId').value = portal.id;
    document.getElementById('portalNombre').value = portal.nombre;
    document.getElementById('modalPortal').style.display = 'block';
}

function cerrarModalPortal() {
    document.getElementById('modalPortal').style.display = 'none';
}

document.getElementById('portalForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('portalId').value;
    const nombre = document.getElementById('portalNombre').value;
    
    const url = id ? `/api/portales-origen/${id}` : '/api/portales-origen';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Portal actualizado' : 'Portal creado');
        cerrarModalPortal();
        cargarPortales();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarPortal(id) {
    if (!confirm('¿Eliminar?')) return;
    const response = await fetch(`/api/portales-origen/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) { alert('Portal eliminado'); cargarPortales(); }
    else alert('Error: ' + result.error);
}

// Gestión Modalidades Entrega
let modalidades = [];
async function cargarModalidades() {
    const response = await fetch('/api/modalidades-entrega');
    modalidades = await response.json();
    const tbody = document.getElementById('modalidadesBody');
    tbody.innerHTML = '';
    modalidades.forEach(m => {
        tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
            <button onclick="editarModalidad(${m.id})" class="btn-primary">Editar</button>
            <button onclick="eliminarModalidad(${m.id})" class="btn-danger">Eliminar</button>
        </td></tr>`;
    });
}

function nuevaModalidad() {
    document.getElementById('modalModalidadTitulo').textContent = 'Nueva Modalidad de Entrega';
    document.getElementById('modalidadForm').reset();
    document.getElementById('modalidadId').value = '';
    document.getElementById('modalModalidad').style.display = 'block';
}

function editarModalidad(id) {
    const modalidad = modalidades.find(m => m.id === id);
    if (!modalidad) return;
    
    document.getElementById('modalModalidadTitulo').textContent = 'Editar Modalidad de Entrega';
    document.getElementById('modalidadId').value = modalidad.id;
    document.getElementById('modalidadNombre').value = modalidad.nombre;
    document.getElementById('modalModalidad').style.display = 'block';
}

function cerrarModalModalidad() {
    document.getElementById('modalModalidad').style.display = 'none';
}

document.getElementById('modalidadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('modalidadId').value;
    const nombre = document.getElementById('modalidadNombre').value;
    
    const url = id ? `/api/modalidades-entrega/${id}` : '/api/modalidades-entrega';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Modalidad actualizada' : 'Modalidad creada');
        cerrarModalModalidad();
        cargarModalidades();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarModalidad(id) {
    if (!confirm('¿Eliminar?')) return;
    const response = await fetch(`/api/modalidades-entrega/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) { alert('Modalidad eliminada'); cargarModalidades(); }
    else alert('Error: ' + result.error);
}

// Gestión Formas Pago
let formasPago = [];
async function cargarFormasPago() {
    const response = await fetch('/api/formas-pago');
    formasPago = await response.json();
    const tbody = document.getElementById('formasBody');
    tbody.innerHTML = '';
    formasPago.forEach(f => {
        tbody.innerHTML += `<tr><td>${f.id}</td><td>${f.nombre}</td><td>
            <button onclick="editarFormaPago(${f.id})" class="btn-primary">Editar</button>
            <button onclick="eliminarFormaPago(${f.id})" class="btn-danger">Eliminar</button>
        </td></tr>`;
    });
}

function nuevaFormaPago() {
    document.getElementById('modalFormaPagoTitulo').textContent = 'Nueva Forma de Pago';
    document.getElementById('formaPagoForm').reset();
    document.getElementById('formaPagoId').value = '';
    document.getElementById('modalFormaPago').style.display = 'block';
}

function editarFormaPago(id) {
    const forma = formasPago.find(f => f.id === id);
    if (!forma) return;
    
    document.getElementById('modalFormaPagoTitulo').textContent = 'Editar Forma de Pago';
    document.getElementById('formaPagoId').value = forma.id;
    document.getElementById('formaPagoNombre').value = forma.nombre;
    document.getElementById('modalFormaPago').style.display = 'block';
}

function cerrarModalFormaPago() {
    document.getElementById('modalFormaPago').style.display = 'none';
}

document.getElementById('formaPagoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('formaPagoId').value;
    const nombre = document.getElementById('formaPagoNombre').value;
    
    const url = id ? `/api/formas-pago/${id}` : '/api/formas-pago';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Forma de pago actualizada' : 'Forma de pago creada');
        cerrarModalFormaPago();
        cargarFormasPago();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarFormaPago(id) {
    if (!confirm('¿Eliminar?')) return;
    const response = await fetch(`/api/formas-pago/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) { alert('Forma de pago eliminada'); cargarFormasPago(); }
    else alert('Error: ' + result.error);
}

// Gestión Organismos
let organismos = [];
async function cargarOrganismos() {
    const response = await fetch('/api/organismos');
    organismos = await response.json();
    const tbody = document.getElementById('organismosBody');
    tbody.innerHTML = '';
    organismos.forEach(o => {
        tbody.innerHTML += `<tr><td>${o.id}</td><td>${o.nombre}</td><td>
            <button onclick="editarOrganismo(${o.id})" class="btn-primary">Editar</button>
            <button onclick="eliminarOrganismo(${o.id})" class="btn-danger">Eliminar</button>
        </td></tr>`;
    });
}

function nuevoOrganismo() {
    document.getElementById('modalOrganismoTitulo').textContent = 'Nuevo Organismo';
    document.getElementById('organismoForm').reset();
    document.getElementById('organismoId').value = '';
    document.getElementById('modalOrganismo').style.display = 'block';
}

function editarOrganismo(id) {
    const organismo = organismos.find(o => o.id === id);
    if (!organismo) return;
    
    document.getElementById('modalOrganismoTitulo').textContent = 'Editar Organismo';
    document.getElementById('organismoId').value = organismo.id;
    document.getElementById('organismoNombre').value = organismo.nombre;
    document.getElementById('modalOrganismo').style.display = 'block';
}

function cerrarModalOrganismo() {
    document.getElementById('modalOrganismo').style.display = 'none';
}

document.getElementById('organismoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('organismoId').value;
    const nombre = document.getElementById('organismoNombre').value;
    
    const url = id ? `/api/organismos/${id}` : '/api/organismos';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Organismo actualizado' : 'Organismo creado');
        cerrarModalOrganismo();
        cargarOrganismos();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarOrganismo(id) {
    if (!confirm('¿Eliminar?')) return;
    const response = await fetch(`/api/organismos/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) { alert('Organismo eliminado'); cargarOrganismos(); }
    else alert('Error: ' + result.error);
}

// Gestión Motivos Pérdida
let motivosPerdida = [];
async function cargarMotivosPerdida() {
    const response = await fetch('/api/motivos-perdida');
    motivosPerdida = await response.json();
    const tbody = document.getElementById('motivosBody');
    tbody.innerHTML = '';
    motivosPerdida.forEach(m => {
        tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
            <button onclick="editarMotivoPerdida(${m.id})" class="btn-primary">Editar</button>
            <button onclick="eliminarMotivoPerdida(${m.id})" class="btn-danger">Eliminar</button>
        </td></tr>`;
    });
}

function nuevoMotivoPerdida() {
    document.getElementById('modalMotivoPerdidaTitulo').textContent = 'Nuevo Motivo de Pérdida';
    document.getElementById('motivoPerdidaForm').reset();
    document.getElementById('motivoPerdidaId').value = '';
    document.getElementById('modalMotivoPerdida').style.display = 'block';
}

function editarMotivoPerdida(id) {
    const motivo = motivosPerdida.find(m => m.id === id);
    if (!motivo) return;
    
    document.getElementById('modalMotivoPerdidaTitulo').textContent = 'Editar Motivo de Pérdida';
    document.getElementById('motivoPerdidaId').value = motivo.id;
    document.getElementById('motivoPerdidaNombre').value = motivo.nombre;
    document.getElementById('modalMotivoPerdida').style.display = 'block';
}

function cerrarModalMotivoPerdida() {
    document.getElementById('modalMotivoPerdida').style.display = 'none';
}

document.getElementById('motivoPerdidaForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('motivoPerdidaId').value;
    const nombre = document.getElementById('motivoPerdidaNombre').value;
    
    const url = id ? `/api/motivos-perdida/${id}` : '/api/motivos-perdida';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Motivo actualizado' : 'Motivo creado');
        cerrarModalMotivoPerdida();
        cargarMotivosPerdida();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarMotivoPerdida(id) {
    if (!confirm('¿Eliminar?')) return;
    const response = await fetch(`/api/motivos-perdida/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) { alert('Motivo eliminado'); cargarMotivosPerdida(); }
    else alert('Error: ' + result.error);
}

// Gestión Mantenimientos Oferta
let mantenimientos = [];
async function cargarMantenimientos() {
    const response = await fetch('/api/mantenimientos-oferta');
    mantenimientos = await response.json();
    const tbody = document.getElementById('mantenimientosBody');
    tbody.innerHTML = '';
    mantenimientos.forEach(m => {
        tbody.innerHTML += `<tr><td>${m.id}</td><td>${m.nombre}</td><td>
            <button onclick="editarMantenimiento(${m.id})" class="btn-primary">Editar</button>
            <button onclick="eliminarMantenimiento(${m.id})" class="btn-danger">Eliminar</button>
        </td></tr>`;
    });
}

function nuevoMantenimiento() {
    document.getElementById('modalMantenimientoTitulo').textContent = 'Nuevo Mantenimiento de Oferta';
    document.getElementById('mantenimientoForm').reset();
    document.getElementById('mantenimientoId').value = '';
    document.getElementById('modalMantenimiento').style.display = 'block';
}

function editarMantenimiento(id) {
    const mantenimiento = mantenimientos.find(m => m.id === id);
    if (!mantenimiento) return;
    
    document.getElementById('modalMantenimientoTitulo').textContent = 'Editar Mantenimiento de Oferta';
    document.getElementById('mantenimientoId').value = mantenimiento.id;
    document.getElementById('mantenimientoNombre').value = mantenimiento.nombre;
    document.getElementById('modalMantenimiento').style.display = 'block';
}

function cerrarModalMantenimiento() {
    document.getElementById('modalMantenimiento').style.display = 'none';
}

document.getElementById('mantenimientoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('mantenimientoId').value;
    const nombre = document.getElementById('mantenimientoNombre').value;
    
    const url = id ? `/api/mantenimientos-oferta/${id}` : '/api/mantenimientos-oferta';
    const method = id ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    if (result.success) {
        alert(id ? 'Mantenimiento actualizado' : 'Mantenimiento creado');
        cerrarModalMantenimiento();
        cargarMantenimientos();
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminarMantenimiento(id) {
    if (!confirm('¿Eliminar?')) return;
    const response = await fetch(`/api/mantenimientos-oferta/${id}`, { method: 'DELETE' });
    const result = await response.json();
    if (result.success) { alert('Mantenimiento eliminado'); cargarMantenimientos(); }
    else alert('Error: ' + result.error);
}
