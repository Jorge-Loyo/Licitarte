let licitaciones = [];
let licitacionesFiltradas = [];
let licitacionActual = null;
let paginaGestion = 1;
const porPaginaGestion = 10;
let tiposLicitacion = [];
let clientes = [];
let modoEdicion = 'editar';
let catalogo = [];
let motivosPerdida = [];
let costoUnitarioActual = 0;

async function cargarLicitaciones() {
    const response = await fetch('/api/licitaciones');
    licitaciones = await response.json();
    
    // Cargar tipos de licitación para el filtro
    const responseTipos = await fetch('/api/tipos-licitacion');
    tiposLicitacion = await responseTipos.json();
    
    // Cargar clientes
    const responseClientes = await fetch('/api/clientes');
    clientes = await responseClientes.json();
    
    // Cargar catálogo
    const responseCatalogo = await fetch('/api/catalogo');
    catalogo = await responseCatalogo.json();
    
    // Cargar motivos de pérdida
    const responseMotivos = await fetch('/api/motivos-perdida');
    motivosPerdida = await responseMotivos.json();
    
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
                           (l.cliente && l.cliente.toLowerCase().includes(search));
        const matchTipo = !filtroTipo || l.tipo_licitacion === filtroTipo;
        
        return matchSearch && matchTipo;
    });
    
    paginaGestion = 1;
    mostrarLicitaciones();
}

function formatearMoneda(valor) {
    if (valor >= 1000000) {
        return '$' + (valor / 1000000).toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' MILL';
    }
    return '$' + valor.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

function mostrarLicitaciones() {
    const tbody = document.getElementById('licitacionesBody');
    tbody.innerHTML = '';
    
    const inicio = (paginaGestion - 1) * porPaginaGestion;
    const fin = inicio + porPaginaGestion;
    const licitacionesPagina = licitacionesFiltradas.slice(inicio, fin);
    
    licitacionesPagina.forEach(l => {
        const tr = document.createElement('tr');
        const totalCotizado = l.total_cotizado || 0;
        tr.innerHTML = `
            <td>${l.id}</td>
            <td>${l.numero}</td>
            <td>${l.cliente}</td>
            <td>${l.tipo_licitacion}</td>
            <td>${l.fecha}</td>
            <td>${formatearMoneda(totalCotizado)}</td>
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
    
    // Calcular total cotizado
    const totalCotizado = productos.reduce((sum, p) => sum + (p.precio_ofertado * p.cantidad), 0);
    
    document.getElementById('detalleTitle').textContent = `Licitación N° ${licitacion.numero}`;
    document.getElementById('detalleInfo').innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px;">
            <div><strong>N° Licitación:</strong> ${licitacion.numero}</div>
            <div><strong>Cliente:</strong> ${licitacion.cliente}</div>
            <div><strong>Tipo:</strong> ${licitacion.tipo_licitacion}</div>
            <div><strong>Fecha:</strong> ${licitacion.fecha}</div>
            <div><strong>Total Cotizado:</strong> ${formatearMoneda(totalCotizado)}</div>
        </div>
    `;
    
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';
    
    productos.forEach(p => {
        const tr = document.createElement('tr');
        const totalProducto = p.precio_ofertado * p.cantidad;
        let difPesos = '-';
        let difPorcentaje = '-';
        
        if (p.resultado === 'No Adjudicado' && p.precio_ganador && p.precio_ofertado) {
            const dif = p.precio_ofertado - p.precio_ganador;
            difPesos = formatearMoneda(dif);
            difPorcentaje = ((dif / p.precio_ganador) * 100).toFixed(2) + '%';
        }
        
        tr.innerHTML = `
            <td>${p.monodroga}</td>
            <td>${p.marca} - ${p.presentacion}</td>
            <td>${p.cantidad}</td>
            <td>${formatearMoneda(p.precio_ofertado)}</td>
            <td>${formatearMoneda(totalProducto)}</td>
            <td>${p.resultado}</td>
            <td>${p.oferente || '-'}</td>
            <td>${p.marca_ganadora || '-'}</td>
            <td>${p.precio_ganador ? formatearMoneda(p.precio_ganador) : '-'}</td>
            <td>${difPesos}</td>
            <td>${difPorcentaje}</td>
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
    modoEdicion = 'editar';
    document.getElementById('modalEditarTitulo').textContent = 'Editar Producto';
    document.getElementById('editProductoId').value = id;
    
    // Cargar catálogo en select
    const select = document.getElementById('editProductoSelect');
    select.innerHTML = '<option value="">Seleccione producto...</option>';
    catalogo.forEach(p => {
        select.innerHTML += `<option value="${p.id}" data-monodroga="${p.monodroga}" data-marca="${p.marca}" data-presentacion="${p.presentacion}">${p.marca} - ${p.presentacion}</option>`;
    });
    
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
    document.getElementById('editMotivoPerdida').value = producto.motivo_perdida || '';
    
    // Obtener costo unitario del producto
    const prodCatalogo = catalogo.find(p => p.monodroga === producto.monodroga && p.marca === producto.marca && p.presentacion === producto.presentacion);
    costoUnitarioActual = prodCatalogo ? (prodCatalogo.costo_unitario || 0) : 0;
    
    // Agregar listeners para recalcular diferencias
    document.getElementById('editPrecio').addEventListener('input', manejarCambioResultadoEdicion);
    document.getElementById('editPrecioGanador').addEventListener('input', manejarCambioResultadoEdicion);
    document.getElementById('editResultado').addEventListener('change', manejarCambioResultadoEdicion);
    
    // Aplicar lógica de resultado
    manejarCambioResultadoEdicion();
    calcularMargen();
    
    document.getElementById('modalEditar').style.display = 'block';
}

function agregarNuevoProducto() {
    modoEdicion = 'crear';
    document.getElementById('modalEditarTitulo').textContent = 'Agregar Producto';
    document.getElementById('editProductoId').value = '';
    
    // Cargar catálogo en select
    const select = document.getElementById('editProductoSelect');
    select.innerHTML = '<option value="">Seleccione producto...</option>';
    catalogo.forEach(p => {
        select.innerHTML += `<option value="${p.id}" data-monodroga="${p.monodroga}" data-marca="${p.marca}" data-presentacion="${p.presentacion}">${p.marca} - ${p.presentacion}</option>`;
    });
    
    document.getElementById('editMonodroga').value = '';
    document.getElementById('editMarca').value = '';
    document.getElementById('editPresentacion').value = '';
    document.getElementById('editCantidad').value = '';
    document.getElementById('editPrecio').value = '';
    document.getElementById('editResultado').value = 'Parcial';
    document.getElementById('editOferenteGanador').value = '';
    document.getElementById('editMarcaGanadora').value = '';
    document.getElementById('editPrecioGanador').value = '';
    document.getElementById('editMarcaOfrecida').value = 'Celtyc';
    
    document.getElementById('modalEditar').style.display = 'block';
}

function seleccionarProducto() {
    const select = document.getElementById('editProductoSelect');
    const option = select.options[select.selectedIndex];
    
    if (option.value) {
        document.getElementById('editMonodroga').value = option.dataset.monodroga;
        document.getElementById('editMarca').value = option.dataset.marca;
        document.getElementById('editPresentacion').value = option.dataset.presentacion;
        
        // Obtener costo unitario del producto
        const producto = catalogo.find(p => p.id == option.value);
        costoUnitarioActual = producto ? (producto.costo_unitario || 0) : 0;
        calcularMargen();
    }
}

function cerrarModalEditar() {
    document.getElementById('modalEditar').style.display = 'none';
}

function calcularMargen() {
    const precioOfertado = parseFloat(document.getElementById('editPrecio').value) || 0;
    const alerta = document.getElementById('alertaMargen');
    
    if (precioOfertado === 0 || costoUnitarioActual === 0) {
        alerta.style.display = 'none';
        return;
    }
    
    const margen = ((precioOfertado - costoUnitarioActual) / costoUnitarioActual) * 100;
    
    alerta.style.display = 'block';
    
    if (precioOfertado <= costoUnitarioActual) {
        alerta.style.background = '#dc3545';
        alerta.style.color = 'white';
        alerta.textContent = `⚠️ ALERTA: Precio por debajo del costo (${margen.toFixed(2)}%)`;
    } else if (margen < 8) {
        alerta.style.background = '#ffc107';
        alerta.style.color = '#000';
        alerta.textContent = `⚠️ MARGEN BAJO: ${margen.toFixed(2)}%`;
    } else {
        alerta.style.background = '#28a745';
        alerta.style.color = 'white';
        alerta.textContent = `✔ MARGEN: ${margen.toFixed(2)}%`;
    }
}

function manejarCambioResultadoEdicion() {
    const resultado = document.getElementById('editResultado').value;
    const oferenteGanador = document.getElementById('editOferenteGanador');
    const marcaGanadora = document.getElementById('editMarcaGanadora');
    const precioGanador = document.getElementById('editPrecioGanador');
    const marcaOfrecida = document.getElementById('editMarcaOfrecida');
    const precioOfertado = document.getElementById('editPrecio');
    const motivoPerdidaContainer = document.getElementById('motivoPerdidaContainer');
    const motivoPerdidaSelect = document.getElementById('editMotivoPerdida');
    const diferenciasContainer = document.getElementById('diferenciasContainer');
    
    if (resultado === 'Adjudicado') {
        oferenteGanador.value = 'Ganada';
        marcaGanadora.value = marcaOfrecida.value;
        precioGanador.value = precioOfertado.value;
        oferenteGanador.disabled = true;
        marcaGanadora.disabled = true;
        precioGanador.disabled = true;
        motivoPerdidaContainer.style.display = 'none';
        motivoPerdidaSelect.required = false;
        diferenciasContainer.style.display = 'none';
    } else if (resultado === 'No Adjudicado') {
        oferenteGanador.disabled = false;
        marcaGanadora.disabled = false;
        precioGanador.disabled = false;
        oferenteGanador.required = true;
        marcaGanadora.required = true;
        precioGanador.required = true;
        motivoPerdidaContainer.style.display = 'block';
        motivoPerdidaSelect.required = true;
        motivoPerdidaSelect.innerHTML = '<option value="">Seleccione...</option>';
        motivosPerdida.forEach(m => {
            motivoPerdidaSelect.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`;
        });
        
        const pOfertado = parseFloat(precioOfertado.value) || 0;
        const pGanador = parseFloat(precioGanador.value) || 0;
        if (pGanador > 0 && pOfertado > 0) {
            diferenciasContainer.style.display = 'block';
            const difPesos = pOfertado - pGanador;
            const difPorcentaje = ((difPesos / pGanador) * 100);
            document.getElementById('diferenciaPesos').textContent = formatearMoneda(difPesos);
            document.getElementById('diferenciaPorcentaje').textContent = difPorcentaje.toFixed(2) + '%';
        } else {
            diferenciasContainer.style.display = 'none';
        }
    } else {
        oferenteGanador.disabled = false;
        marcaGanadora.disabled = false;
        precioGanador.disabled = false;
        oferenteGanador.required = false;
        marcaGanadora.required = false;
        precioGanador.required = false;
        motivoPerdidaContainer.style.display = 'none';
        motivoPerdidaSelect.required = false;
        diferenciasContainer.style.display = 'none';
    }
}

document.getElementById('editarForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
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
        marca_ofrecida: document.getElementById('editMarcaOfrecida').value,
        motivo_perdida: document.getElementById('editMotivoPerdida').value
    };
    
    let response;
    if (modoEdicion === 'crear') {
        data.licitacion_id = licitacionActual;
        response = await fetch('/api/productos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    } else {
        const id = document.getElementById('editProductoId').value;
        response = await fetch(`/api/productos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    }
    
    const result = await response.json();
    if (result.success) {
        mostrarNotificacion('✓ Éxito', modoEdicion === 'crear' ? 'Producto agregado' : 'Producto actualizado');
        cerrarModalEditar();
        verDetalle(licitacionActual);
    } else {
        mostrarNotificacion('✗ Error', result.error);
    }
});

async function eliminar(id) {
    if (!confirm('¿Eliminar esta licitación?')) return;
    
    const response = await fetch(`/api/licitaciones/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        mostrarNotificacion('✓ Éxito', 'Licitación eliminada');
        cargarLicitaciones();
    } else {
        mostrarNotificacion('✗ Error', result.error);
    }
}

document.addEventListener('DOMContentLoaded', cargarLicitaciones);

function mostrarNotificacion(titulo, mensaje) {
    document.getElementById('notificacionTitulo').textContent = titulo;
    document.getElementById('notificacionMensaje').textContent = mensaje;
    document.getElementById('modalNotificacion').style.display = 'block';
}

function cerrarNotificacion() {
    document.getElementById('modalNotificacion').style.display = 'none';
}

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
        mostrarNotificacion('✓ Éxito', 'Licitación actualizada');
        cerrarModalEditarLicitacion();
        await cargarLicitaciones();
        verDetalle(licitacionActual);
    } else {
        mostrarNotificacion('✗ Error', result.error);
    }
});
