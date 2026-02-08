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
        const numeroPresupuesto = l.numero_presupuesto || '-';
        
        // Mostrar número de presupuesto con botón ver si existe
        let presupuestoHtml = numeroPresupuesto;
        if (numeroPresupuesto !== '-') {
            presupuestoHtml = `${numeroPresupuesto} <button onclick="window.open('/presupuesto/${numeroPresupuesto}', '_blank')" class="btn-primary" style="padding: 4px 8px; font-size: 12px;">👁️</button>`;
        }
        
        tr.innerHTML = `
            <td>${l.numero}</td>
            <td>${l.cliente}</td>
            <td>${l.tipo_licitacion}</td>
            <td>${l.fecha}</td>
            <td>${formatearMoneda(totalCotizado)}</td>
            <td>${presupuestoHtml}</td>
            <td>
                <button onclick="verDetalle(${l.id})" class="btn-primary">Ver Detalle</button>
                <button onclick="editarLicitacionPagina(${l.id})" class="btn-success">Editar</button>
                <button onclick="exportarExcel(${l.id})" class="btn-primary">📊 Excel</button>
                <button onclick="generarPresupuesto(${l.id})" class="btn-primary">📄 Nuevo Presupuesto</button>
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
    
    // Calcular total cotizado considerando alternativas
    let totalCotizado = 0;
    for (const p of productos) {
        let precioActual = p.precio_ofertado;
        
        if (p.producto_cotizar && p.producto_cotizar !== 'principal') {
            const match = p.producto_cotizar.match(/alt-\d+-(\d+)/);
            if (match) {
                const idx = parseInt(match[1]);
                const altResponse = await fetch(`/api/alternativas/${p.id}`);
                const alternativas = await altResponse.json();
                if (alternativas[idx]) {
                    precioActual = alternativas[idx].precio_ofertado;
                }
            }
        }
        
        totalCotizado += precioActual * p.cantidad;
    }
    
    // Formatear fecha a DD/MM/AAAA HH:MM
    let fechaFormateada = licitacion.fecha;
    if (licitacion.fecha) {
        const fecha = new Date(licitacion.fecha);
        const dia = String(fecha.getDate()).padStart(2, '0');
        const mes = String(fecha.getMonth() + 1).padStart(2, '0');
        const anio = fecha.getFullYear();
        const horas = String(fecha.getHours()).padStart(2, '0');
        const minutos = String(fecha.getMinutes()).padStart(2, '0');
        fechaFormateada = `${dia}/${mes}/${anio} ${horas}:${minutos}`;
    }
    
    document.getElementById('detalleTitle').textContent = `Licitación N° ${licitacion.numero}`;
    document.getElementById('detalleInfo').innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px;">
            <div><strong>N° Licitación:</strong> ${licitacion.numero}</div>
            <div><strong>Cliente:</strong> ${licitacion.cliente}</div>
            <div><strong>Tipo:</strong> ${licitacion.tipo_licitacion}</div>
            <div><strong>Apertura:</strong> ${fechaFormateada}</div>
            <div><strong>Total Cotizado:</strong> ${formatearMoneda(totalCotizado)}</div>
        </div>
    `;
    
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';
    
    for (const p of productos) {
        const tr = document.createElement('tr');
        
        console.log('Producto:', p.monodroga, 'producto_cotizar:', p.producto_cotizar);
        
        // Si es alternativa, buscar sus datos
        let precioActual = p.precio_ofertado;
        let marcaActual = p.marca;
        let presentacionActual = p.presentacion;
        let alternativaSeleccionada = null;
        
        if (p.producto_cotizar && p.producto_cotizar !== 'principal') {
            // Extraer índice de alternativa (ej: "alt-1-0" -> 0)
            const match = p.producto_cotizar.match(/alt-\d+-(\d+)/);
            if (match) {
                const idx = parseInt(match[1]);
                const altResponse = await fetch(`/api/alternativas/${p.id}`);
                const alternativas = await altResponse.json();
                console.log('Alternativas encontradas:', alternativas);
                console.log('Índice a buscar:', idx);
                if (alternativas[idx]) {
                    alternativaSeleccionada = alternativas[idx];
                    precioActual = alternativas[idx].precio_ofertado;
                    marcaActual = alternativas[idx].marca;
                    presentacionActual = alternativas[idx].presentacion;
                    console.log('Alternativa seleccionada:', alternativaSeleccionada);
                }
            }
        }
        
        const totalProducto = precioActual * p.cantidad;
        
        // Determinar ganador, precio y laboratorio según resultado
        let ganador = '-';
        let precioGanador = '-';
        let laboratorioGanador = '-';
        
        // Solo llenar si NO hay alternativa seleccionada (producto_cotizar === 'principal')
        if (p.producto_cotizar === 'principal' || !p.producto_cotizar) {
            if (p.resultado === 'Adjudicado') {
                ganador = 'Celtyc';
                precioGanador = formatearMoneda(precioActual);
                const prodCatalogo = catalogo.find(c => 
                    c.monodroga?.toLowerCase().trim() === p.monodroga?.toLowerCase().trim() && 
                    c.marca?.toLowerCase().trim() === marcaActual?.toLowerCase().trim() && 
                    c.presentacion?.toLowerCase().trim() === presentacionActual?.toLowerCase().trim()
                );
                laboratorioGanador = prodCatalogo?.laboratorio || 'Celtyc';
            } else if (p.resultado === 'No Adjudicado' && p.oferente_ganador) {
                ganador = p.oferente_ganador;
                precioGanador = p.precio_ganador ? formatearMoneda(p.precio_ganador) : '-';
                try {
                    const ofertasResponse = await fetch(`/api/ofertas/${p.id}`);
                    const ofertas = await ofertasResponse.json();
                    const ofertaGanadora = ofertas.find(o => o.oferente === ganador);
                    laboratorioGanador = ofertaGanadora?.laboratorio || '-';
                } catch (error) {
                    console.error('Error cargando ofertas:', error);
                    laboratorioGanador = '-';
                }
            }
        }
        
        tr.innerHTML = `
            <td>${p.monodroga}</td>
            <td>${marcaActual} - ${presentacionActual}</td>
            <td>${p.cantidad}</td>
            <td>${formatearMoneda(precioActual)}</td>
            <td>${formatearMoneda(totalProducto)}</td>
            <td>${p.observaciones || '-'}</td>
            <td>${ganador}</td>
            <td>${precioGanador}</td>
            <td>${laboratorioGanador}</td>
        `;
        tbody.appendChild(tr);
        
        // Cargar y mostrar alternativas
        const altResponse = await fetch(`/api/alternativas/${p.id}`);
        const alternativas = await altResponse.json();
        
        if (alternativas && alternativas.length > 0) {
            for (let altIndex = 0; altIndex < alternativas.length; altIndex++) {
                const alt = alternativas[altIndex];
                const trAlt = document.createElement('tr');
                trAlt.style.background = '#1a1a1a';
                const totalAlt = alt.precio_ofertado * p.cantidad;
                
                const esAlternativaSeleccionada = p.producto_cotizar === `alt-${p.id}-${altIndex}`;
                
                let ganadorAlt = '-';
                let precioGanadorAlt = '-';
                let laboratorioGanadorAlt = '-';
                
                if (esAlternativaSeleccionada) {
                    if (p.resultado === 'Adjudicado') {
                        ganadorAlt = 'Celtyc';
                        precioGanadorAlt = formatearMoneda(alt.precio_ofertado);
                        const prodCatalogo = catalogo.find(c => 
                            c.monodroga?.toLowerCase().trim() === p.monodroga?.toLowerCase().trim() && 
                            c.marca?.toLowerCase().trim() === alt.marca?.toLowerCase().trim() && 
                            c.presentacion?.toLowerCase().trim() === alt.presentacion?.toLowerCase().trim()
                        );
                        laboratorioGanadorAlt = prodCatalogo?.laboratorio || 'Celtyc';
                    } else if (p.resultado === 'No Adjudicado' && p.oferente_ganador) {
                        ganadorAlt = p.oferente_ganador;
                        precioGanadorAlt = p.precio_ganador ? formatearMoneda(p.precio_ganador) : '-';
                        try {
                            const ofertasResponse = await fetch(`/api/ofertas/${p.id}`);
                            const ofertas = await ofertasResponse.json();
                            const ofertaGanadora = ofertas.find(o => o.oferente === ganadorAlt);
                            laboratorioGanadorAlt = ofertaGanadora?.laboratorio || '-';
                        } catch (error) {
                            laboratorioGanadorAlt = '-';
                        }
                    }
                }
                
                trAlt.innerHTML = `
                    <td style="padding-left: 30px; color: #999;">ALT ${p.monodroga}</td>
                    <td style="color: #999;">${alt.marca} - ${alt.presentacion}</td>
                    <td style="color: #999;">${p.cantidad}</td>
                    <td style="color: #999;">${formatearMoneda(alt.precio_ofertado)}</td>
                    <td style="color: #999;">${formatearMoneda(totalAlt)}</td>
                    <td style="color: #999;">${alt.observaciones || '-'}</td>
                    <td style="color: #999;">${ganadorAlt}</td>
                    <td style="color: #999;">${precioGanadorAlt}</td>
                    <td style="color: #999;">${laboratorioGanadorAlt}</td>
                `;
                tbody.appendChild(trAlt);
            }
        }
    }
    
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
    const motivoPerdidaSelect = document.getElementById('editMotivoPerdida');
    const diferenciasContainer = document.getElementById('diferenciasContainer');
    
    if (resultado === 'Adjudicado') {
        oferenteGanador.value = 'Ganada';
        marcaGanadora.value = marcaOfrecida.value;
        precioGanador.value = precioOfertado.value;
        oferenteGanador.disabled = true;
        marcaGanadora.disabled = true;
        precioGanador.disabled = true;
        motivoPerdidaSelect.disabled = true;
        motivoPerdidaSelect.required = false;
        motivoPerdidaSelect.value = '';
        diferenciasContainer.style.display = 'none';
    } else if (resultado === 'No Adjudicado') {
        oferenteGanador.disabled = false;
        marcaGanadora.disabled = false;
        precioGanador.disabled = false;
        oferenteGanador.required = true;
        marcaGanadora.required = true;
        precioGanador.required = true;
        motivoPerdidaSelect.disabled = false;
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
        motivoPerdidaSelect.disabled = true;
        motivoPerdidaSelect.required = false;
        motivoPerdidaSelect.value = '';
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

let licitacionAEliminar = null;

function eliminar(id) {
    licitacionAEliminar = id;
    document.getElementById('modalConfirmar').style.display = 'block';
}

function cerrarModalConfirmar() {
    document.getElementById('modalConfirmar').style.display = 'none';
    licitacionAEliminar = null;
}

async function confirmarEliminacion() {
    if (!licitacionAEliminar) return;
    
    const response = await fetch(`/api/licitaciones/${licitacionAEliminar}`, { method: 'DELETE' });
    const result = await response.json();
    
    cerrarModalConfirmar();
    
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

function editarLicitacionPagina(id) {
    window.location.href = `/editar-licitacion/${id}`;
}

async function generarPresupuesto(licitacionId) {
    try {
        const response = await fetch('/api/presupuestos/crear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ licitacion_id: licitacionId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion('✓ Éxito', `Presupuesto N° ${result.numero} generado correctamente`);
            // Abrir presupuesto en nueva pestaña
            window.open(`/presupuesto/${result.numero}`, '_blank');
            cargarLicitaciones();
        } else {
            mostrarNotificacion('✗ Error', result.error);
        }
    } catch (error) {
        mostrarNotificacion('✗ Error', 'Error al generar presupuesto: ' + error.message);
    }
}

async function exportarExcel(licitacionId) {
    try {
        const response = await fetch(`/api/licitaciones/${licitacionId}/exportar-excel`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `licitacion_${licitacionId}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        mostrarNotificacion('✗ Error', 'Error al exportar: ' + error.message);
    }
}
