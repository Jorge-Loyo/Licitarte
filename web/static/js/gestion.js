let licitaciones = [];
let licitacionesFiltradas = [];
let licitacionActual = null;
let paginaGestion = 1;
const porPaginaGestion = 10;
let tiposLicitacion = [];
let clientes = [];

async function cargarLicitaciones() {
    const response = await fetch('/api/licitaciones');
    licitaciones = await response.json();
    
    // Cargar tipos de licitación para el filtro
    const responseTipos = await fetch('/api/tipos-licitacion');
    tiposLicitacion = await responseTipos.json();
    
    // Cargar clientes
    const responseClientes = await fetch('/api/clientes');
    clientes = await responseClientes.json();
    
    const selectTipo = document.getElementById('filtroTipo');
    selectTipo.innerHTML = '<option value="">Todos los tipos</option>';
    tiposLicitacion.forEach(t => {
        selectTipo.innerHTML += `<option value="${t.nombre}">${t.nombre}</option>`;
    });
    
    filtrarLicitaciones();
}

function filtrarLicitaciones() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const filtroTipo = document.getElementById('filtroTipo').value;
    
    licitacionesFiltradas = licitaciones.filter(l => {
        const matchSearch = l.numero.toLowerCase().includes(search) || 
                           (l.oferente && l.oferente.toLowerCase().includes(search));
        const matchTipo = !filtroTipo || l.tipo_licitacion === filtroTipo;
        
        return matchSearch && matchTipo;
    });
    
    paginaGestion = 1;
    mostrarLicitaciones();
}

function mostrarLicitaciones() {
    const tbody = document.getElementById('licitacionesBody');
    tbody.innerHTML = '';
    
    const inicio = (paginaGestion - 1) * porPaginaGestion;
    const fin = inicio + porPaginaGestion;
    const licitacionesPagina = licitacionesFiltradas.slice(inicio, fin);
    
    licitacionesPagina.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${l.id}</td>
            <td>${l.numero}</td>
            <td>${l.cliente}</td>
            <td>${l.tipo_licitacion}</td>
            <td>${l.fecha}</td>
            <td>${l.ganancia || '-'}</td>
            <td>
                <button onclick="verDetalle(${l.id})" class="btn-primary">Ver Detalle</button>
                <button onclick="eliminar(${l.id})" class="btn-danger">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    const totalPaginas = Math.ceil(licitacionesFiltradas.length / porPaginaGestion);
    document.getElementById('paginaInfoGestion').textContent = `Página ${paginaGestion} de ${totalPaginas || 1}`;
    document.getElementById('btnAnteriorGestion').disabled = paginaGestion === 1;
    document.getElementById('btnSiguienteGestion').disabled = paginaGestion >= totalPaginas;
}

function cambiarPaginaGestion(direccion) {
    paginaGestion += direccion;
    mostrarLicitaciones();
}

async function verDetalle(id) {
    licitacionActual = id;
    
    const licitacion = licitaciones.find(l => l.id === id);
    const response = await fetch(`/api/productos/${id}`);
    const productos = await response.json();
    
    document.getElementById('detalleTitle').textContent = `Licitación N° ${licitacion.numero}`;
    document.getElementById('detalleInfo').innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
            <div><strong>N° Licitación:</strong> ${licitacion.numero}</div>
            <div><strong>Cliente:</strong> ${licitacion.cliente}</div>
            <div><strong>Tipo:</strong> ${licitacion.tipo_licitacion}</div>
            <div><strong>Fecha:</strong> ${licitacion.fecha}</div>
        </div>
    `;
    
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';
    
    productos.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.monodroga}</td>
            <td>${p.marca} - ${p.presentacion}</td>
            <td>${p.cantidad}</td>
            <td>$${p.precio_ofertado.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
            <td>${p.resultado}</td>
            <td>${p.oferente || '-'}</td>
            <td>${p.marca_ganadora || '-'}</td>
            <td>${p.precio_ganador ? '$' + p.precio_ganador.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '-'}</td>
            <td>${p.marca_ofrecida || '-'}</td>
            <td>
                <button onclick="editarProducto(${p.id}, ${JSON.stringify(p).replace(/"/g, '&quot;')})" class="btn-primary">Editar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    document.getElementById('modalDetalle').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalDetalle').style.display = 'none';
}

function editarProducto(id, producto) {
    document.getElementById('editProductoId').value = id;
    document.getElementById('editMonodroga').value = producto.monodroga;
    document.getElementById('editMarca').value = producto.marca;
    document.getElementById('editPresentacion').value = producto.presentacion;
    document.getElementById('editCantidad').value = producto.cantidad;
    document.getElementById('editPrecio').value = producto.precio_ofertado;
    document.getElementById('editResultado').value = producto.resultado;
    document.getElementById('editOferenteGanador').value = producto.oferente || '';
    document.getElementById('editMarcaGanadora').value = producto.marca_ganadora || '';
    document.getElementById('editPrecioGanador').value = producto.precio_ganador || '';
    document.getElementById('editMarcaOfrecida').value = producto.marca_ofrecida || '';
    
    document.getElementById('modalEditar').style.display = 'block';
}

function cerrarModalEditar() {
    document.getElementById('modalEditar').style.display = 'none';
}

document.getElementById('editarForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('editProductoId').value;
    const data = {
        monodroga: document.getElementById('editMonodroga').value,
        marca: document.getElementById('editMarca').value,
        presentacion: document.getElementById('editPresentacion').value,
        cantidad: document.getElementById('editCantidad').value,
        precio_ofertado: document.getElementById('editPrecio').value,
        resultado: document.getElementById('editResultado').value,
        oferente: document.getElementById('editOferenteGanador').value,
        marca_ganadora: document.getElementById('editMarcaGanadora').value,
        precio_ganador: document.getElementById('editPrecioGanador').value,
        marca_ofrecida: document.getElementById('editMarcaOfrecida').value
    };
    
    const response = await fetch(`/api/productos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    if (result.success) {
        alert('Producto actualizado');
        cerrarModalEditar();
        verDetalle(licitacionActual);
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminar(id) {
    if (!confirm('¿Eliminar esta licitación?')) return;
    
    const response = await fetch(`/api/licitaciones/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        alert('Licitación eliminada');
        cargarLicitaciones();
    } else {
        alert('Error: ' + result.error);
    }
}

document.addEventListener('DOMContentLoaded', cargarLicitaciones);

function editarLicitacion() {
    const licitacion = licitaciones.find(l => l.id === licitacionActual);
    if (!licitacion) return;
    
    document.getElementById('editLicitacionId').value = licitacion.id;
    document.getElementById('editNumeroLicitacion').value = licitacion.numero;
    document.getElementById('editFecha').value = licitacion.fecha;
    
    // Llenar select de clientes
    const selectCliente = document.getElementById('editClienteSelect');
    selectCliente.innerHTML = '<option value="">Seleccione cliente...</option>';
    clientes.forEach(c => {
        const selected = c.nombre === licitacion.cliente ? 'selected' : '';
        selectCliente.innerHTML += `<option value="${c.id}" ${selected}>${c.nombre}</option>`;
    });
    
    // Llenar select de tipos
    const selectTipo = document.getElementById('editTipoLicitacionSelect');
    selectTipo.innerHTML = '<option value="">Seleccione tipo...</option>';
    tiposLicitacion.forEach(t => {
        const selected = t.nombre === licitacion.tipo_licitacion ? 'selected' : '';
        selectTipo.innerHTML += `<option value="${t.id}" ${selected}>${t.nombre}</option>`;
    });
    
    document.getElementById('modalEditarLicitacion').style.display = 'block';
}

function cerrarModalEditarLicitacion() {
    document.getElementById('modalEditarLicitacion').style.display = 'none';
}

document.getElementById('editarLicitacionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('editLicitacionId').value;
    const data = {
        numero: document.getElementById('editNumeroLicitacion').value,
        cliente_id: document.getElementById('editClienteSelect').value,
        tipo_licitacion_id: document.getElementById('editTipoLicitacionSelect').value || null,
        fecha: document.getElementById('editFecha').value
    };
    
    const response = await fetch(`/api/licitaciones/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    if (result.success) {
        alert('Licitación actualizada');
        cerrarModalEditarLicitacion();
        await cargarLicitaciones();
        verDetalle(licitacionActual);
    } else {
        alert('Error: ' + result.error);
    }
});
