let productoCount = 0;
let catalogoProductos = [];
let clientes = [];
let oferentes = [];
let marcas = [];
let tiposLicitacion = [];
let motivosPerdida = [];

// Cargar catálogo y clientes al iniciar
async function cargarCatalogo() {
    try {
        const response = await fetch('/api/catalogo');
        catalogoProductos = await response.json();
    } catch (error) {
        console.error('Error cargando catálogo:', error);
    }
}

async function cargarClientes() {
    try {
        const response = await fetch('/api/clientes');
        clientes = await response.json();
        const select = document.getElementById('clienteSelect');
        select.innerHTML = '<option value="">Seleccione cliente...</option>';
        clientes.forEach(c => {
            select.innerHTML += `<option value="${c.id}" data-organismo="${c.organismo_jurisdiccion || ''}">${c.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando clientes:', error);
    }
}

function seleccionarCliente() {
    const select = document.getElementById('clienteSelect');
    const option = select.options[select.selectedIndex];
    const organismo = option.dataset.organismo || '-';
    document.getElementById('clienteOrganismo').value = organismo;
}

async function cargarOferentes() {
    try {
        const response = await fetch('/api/oferentes');
        oferentes = await response.json();
    } catch (error) {
        console.error('Error cargando oferentes:', error);
    }
}

async function cargarMarcas() {
    try {
        const response = await fetch('/api/marcas');
        marcas = await response.json();
    } catch (error) {
        console.error('Error cargando marcas:', error);
    }
}

async function cargarTiposLicitacion() {
    try {
        const response = await fetch('/api/tipos-licitacion');
        tiposLicitacion = await response.json();
        const select = document.getElementById('tipoLicitacionSelect');
        select.innerHTML = '<option value="">Seleccione tipo...</option>';
        tiposLicitacion.forEach(t => {
            select.innerHTML += `<option value="${t.id}">${t.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando tipos de licitación:', error);
    }
}

async function cargarPortalesOrigen() {
    try {
        const response = await fetch('/api/portales-origen');
        const portales = await response.json();
        const select = document.getElementById('portalOrigen');
        select.innerHTML = '<option value="">Seleccione...</option>';
        portales.forEach(p => {
            select.innerHTML += `<option value="${p.nombre}">${p.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando portales:', error);
    }
}

async function cargarModalidadesEntrega() {
    try {
        const response = await fetch('/api/modalidades-entrega');
        const modalidades = await response.json();
        const select = document.getElementById('modalidadEntrega');
        select.innerHTML = '<option value="">Seleccione...</option>';
        modalidades.forEach(m => {
            select.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando modalidades:', error);
    }
}

async function cargarFormasPago() {
    try {
        const response = await fetch('/api/formas-pago');
        const formas = await response.json();
        const select = document.getElementById('formaPago');
        select.innerHTML = '<option value="">Seleccione...</option>';
        formas.forEach(f => {
            select.innerHTML += `<option value="${f.nombre}">${f.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando formas de pago:', error);
    }
}

function capitalizarTexto(texto) {
    if (!texto) return '';
    return texto.toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
}

function agregarProducto() {
    const container = document.getElementById('productosContainer');
    const div = document.createElement('div');
    div.className = 'producto-item';
    div.id = `producto-${productoCount}`;
    
    // Crear opciones de Marca - Presentación
    let options = '<option value="">Seleccione marca y presentación...</option>';
    catalogoProductos.forEach(p => {
        options += `<option value="${p.numero_registro}" data-monodroga="${p.monodroga}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-laboratorio="${p.laboratorio || ''}">
            ${p.marca} - ${p.presentacion}
        </option>`;
    });
    
    div.innerHTML = `
        <div style="background: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 15px; position: relative;">
            <button type="button" class="btn-remove" onclick="eliminarProducto(${productoCount})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-size: 18px;">✕</button>
            
            <h4 style="color: var(--primary); margin-bottom: 15px; font-size: 14px;">PRODUCTO #${productoCount + 1}</h4>
            
            <div class="form-group">
                <label>Marca - Presentación *</label>
                <select class="producto-selector" onchange="seleccionarProducto(this)" style="font-size: 16px; padding: 12px;">
                    ${options}
                </select>
            </div>
            <div class="form-group">
                <label>Monodroga</label>
                <input type="text" class="producto-monodroga-display" readonly style="background: #333; cursor: not-allowed; font-size: 16px; padding: 12px;">
            </div>
            <input type="hidden" class="producto-monodroga">
            <input type="hidden" class="producto-marca">
            <input type="hidden" class="producto-presentacion">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Cantidad *</label>
                    <input type="number" class="producto-cantidad" required style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Precio Ofertado *</label>
                    <input type="number" step="0.01" class="producto-precio" required oninput="calcularMargenIngreso(this)" style="font-size: 16px; padding: 12px;">
                </div>
            </div>
            <div class="alerta-margen" style="display: none; margin-top: 10px; padding: 12px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 14px;"></div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div class="form-group">
                    <label>Resultado *</label>
                    <select class="producto-resultado" onchange="manejarCambioResultado(this)" style="font-size: 16px; padding: 12px;">
                        <option value="Parcial">Parcial</option>
                        <option value="Adjudicado">Adjudicado</option>
                        <option value="No Adjudicado">No Adjudicado</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Marca Ofrecida</label>
                    <input type="text" class="producto-marca-ofrecida" style="font-size: 16px; padding: 12px;">
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div class="form-group">
                    <label>Oferente Ganador</label>
                    <select class="producto-oferente-ganador" style="font-size: 16px; padding: 12px;">
                        <option value="">Seleccione...</option>
                        <option value="Ganada">Ganada</option>
                        ${oferentes.map(o => `<option value="${o.nombre}">${o.nombre}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Marca Ganadora</label>
                    <input type="text" class="producto-marca-ganadora" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Precio Ganador</label>
                    <input type="number" step="0.01" class="producto-precio-ganador" style="font-size: 16px; padding: 12px;">
                </div>
            </div>
            <div class="form-group motivo-perdida-container" style="margin-top: 15px; display: none;">
                <label>Motivo de Pérdida *</label>
                <select class="producto-motivo-perdida" style="font-size: 16px; padding: 12px;">
                    <option value="">Seleccione...</option>
                </select>
            </div>
        </div>
    `;
    
    container.appendChild(div);
    productoCount++;
}

function seleccionarProducto(select) {
    const option = select.options[select.selectedIndex];
    const container = select.closest('.producto-item');
    
    const monodroga = option.dataset.monodroga || '';
    const marca = option.dataset.marca || '';
    const presentacion = option.dataset.presentacion || '';
    const laboratorio = option.dataset.laboratorio || '';
    
    // Capitalizar monodroga
    const monodrogaCapitalizada = capitalizarTexto(monodroga);
    
    container.querySelector('.producto-monodroga').value = monodrogaCapitalizada;
    container.querySelector('.producto-monodroga-display').value = monodrogaCapitalizada;
    container.querySelector('.producto-marca').value = marca;
    container.querySelector('.producto-presentacion').value = presentacion;
    container.querySelector('.producto-marca-ofrecida').value = laboratorio;
    
    // Guardar costo unitario
    const producto = catalogoProductos.find(p => p.numero_registro === option.value);
    container.dataset.costoUnitario = producto ? (producto.costo_unitario || 0) : 0;
    calcularMargenIngreso(container.querySelector('.producto-precio'));
}

function calcularMargenIngreso(input) {
    const container = input.closest('.producto-item');
    const alerta = container.querySelector('.alerta-margen');
    const precioOfertado = parseFloat(input.value) || 0;
    const costoUnitario = parseFloat(container.dataset.costoUnitario) || 0;
    
    if (precioOfertado === 0 || costoUnitario === 0) {
        alerta.style.display = 'none';
        return;
    }
    
    const margen = ((precioOfertado - costoUnitario) / costoUnitario) * 100;
    
    alerta.style.display = 'block';
    
    if (precioOfertado <= costoUnitario) {
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

function manejarCambioResultado(select) {
    const container = select.closest('.producto-item');
    const resultado = select.value;
    const oferenteGanador = container.querySelector('.producto-oferente-ganador');
    const marcaGanadora = container.querySelector('.producto-marca-ganadora');
    const precioGanador = container.querySelector('.producto-precio-ganador');
    const marcaOfrecida = container.querySelector('.producto-marca-ofrecida');
    const precioOfertado = container.querySelector('.producto-precio');
    const motivoPerdidaContainer = container.querySelector('.motivo-perdida-container');
    const motivoPerdida = container.querySelector('.producto-motivo-perdida');
    
    if (resultado === 'Adjudicado') {
        oferenteGanador.value = 'Ganada';
        marcaGanadora.value = marcaOfrecida.value;
        precioGanador.value = precioOfertado.value;
        oferenteGanador.disabled = true;
        marcaGanadora.disabled = true;
        precioGanador.disabled = true;
        motivoPerdidaContainer.style.display = 'none';
        motivoPerdida.required = false;
        motivoPerdida.value = '';
    } else if (resultado === 'No Adjudicado') {
        oferenteGanador.disabled = false;
        marcaGanadora.disabled = false;
        precioGanador.disabled = false;
        oferenteGanador.required = true;
        marcaGanadora.required = true;
        precioGanador.required = true;
        motivoPerdidaContainer.style.display = 'block';
        motivoPerdida.required = true;
        motivoPerdida.innerHTML = '<option value="">Seleccione...</option>';
        motivosPerdida.forEach(m => {
            motivoPerdida.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`;
        });
    } else {
        oferenteGanador.disabled = false;
        marcaGanadora.disabled = false;
        precioGanador.disabled = false;
        oferenteGanador.required = false;
        marcaGanadora.required = false;
        precioGanador.required = false;
        motivoPerdidaContainer.style.display = 'none';
        motivoPerdida.required = false;
        motivoPerdida.value = '';
    }
}

function eliminarProducto(id) {
    document.getElementById(`producto-${id}`).remove();
}

document.getElementById('licitacionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const productos = [];
    document.querySelectorAll('.producto-item').forEach(item => {
        const monodroga = item.querySelector('.producto-monodroga').value;
        const marca = item.querySelector('.producto-marca').value;
        const presentacion = item.querySelector('.producto-presentacion').value;
        
        if (!monodroga || !marca || !presentacion) {
            return;
        }
        
        productos.push({
            monodroga: monodroga,
            marca: marca,
            presentacion: presentacion,
            cantidad: item.querySelector('.producto-cantidad').value,
            precio: item.querySelector('.producto-precio').value,
            resultado: item.querySelector('.producto-resultado').value,
            marca_ofrecida: item.querySelector('.producto-marca-ofrecida').value,
            oferente_ganador: item.querySelector('.producto-oferente-ganador').value,
            marca_ganadora: item.querySelector('.producto-marca-ganadora').value,
            precio_ganador: item.querySelector('.producto-precio-ganador').value,
            motivo_perdida: item.querySelector('.producto-motivo-perdida').value
        });
    });
    
    if (productos.length === 0) {
        mostrarMensaje('Agregue al menos un producto y complete todos los campos', 'error');
        return;
    }
    
    const data = {
        numero: document.getElementById('numeroLicitacion').value,
        cliente_id: document.getElementById('clienteSelect').value,
        tipo_licitacion_id: document.getElementById('tipoLicitacionSelect').value,
        fecha: document.getElementById('fecha').value,
        portal_origen: document.getElementById('portalOrigen').value,
        modalidad_entrega: document.getElementById('modalidadEntrega').value,
        forma_pago: document.getElementById('formaPago').value,
        requiere_poliza: document.getElementById('requierePoliza').checked,
        monto_poliza: document.getElementById('montoPoliza').value || null,
        observaciones: document.getElementById('observaciones').value,
        productos: productos
    };
    
    try {
        const response = await fetch('/api/licitaciones', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarMensaje('Licitación guardada correctamente', 'success');
            document.getElementById('licitacionForm').reset();
            document.getElementById('productosContainer').innerHTML = '';
            productoCount = 0;
            agregarProducto();
        } else {
            mostrarMensaje('Error: ' + result.error, 'error');
        }
    } catch (error) {
        mostrarMensaje('Error al guardar: ' + error.message, 'error');
    }
});

function mostrarMensaje(texto, tipo) {
    document.getElementById('notificacionTitulo').textContent = tipo === 'success' ? '✔ Éxito' : '✗ Error';
    document.getElementById('notificacionMensaje').textContent = texto;
    document.getElementById('modalNotificacion').style.display = 'block';
}

function cerrarNotificacion() {
    document.getElementById('modalNotificacion').style.display = 'none';
}

async function nuevoOferente(btn) {
    const nombre = prompt('Nombre del oferente:');
    if (!nombre) return;
    
    try {
        const response = await fetch('/api/oferentes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre })
        });
        const result = await response.json();
        if (result.success) {
            await cargarOferentes();
            const select = btn.previousElementSibling;
            select.innerHTML = '<option value="">Seleccione...</option>' + 
                oferentes.map(o => `<option value="${o.nombre}">${o.nombre}</option>`).join('');
            select.value = nombre;
            mostrarMensaje('Oferente agregado', 'success');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function nuevaMarca(btn) {
    const nombre = prompt('Nombre de la marca:');
    if (!nombre) return;
    
    try {
        const response = await fetch('/api/marcas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre })
        });
        const result = await response.json();
        if (result.success) {
            await cargarMarcas();
            const select = btn.previousElementSibling;
            select.innerHTML = '<option value="">Seleccione...</option>' + 
                marcas.map(m => `<option value="${m.nombre}">${m.nombre}</option>`).join('');
            select.value = nombre;
            mostrarMensaje('Marca agregada', 'success');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function nuevoTipoLicitacion() {
    const nombre = prompt('Nombre del tipo de licitación:');
    if (!nombre) return;
    
    try {
        const response = await fetch('/api/tipos-licitacion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre })
        });
        const result = await response.json();
        if (result.success) {
            await cargarTiposLicitacion();
            document.getElementById('tipoLicitacionSelect').value = result.id;
            mostrarMensaje('Tipo de licitación agregado', 'success');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('fecha').valueAsDate = new Date();
    
    // Habilitar/deshabilitar monto de póliza
    document.getElementById('requierePoliza').addEventListener('change', (e) => {
        document.getElementById('montoPoliza').disabled = !e.target.checked;
        if (!e.target.checked) {
            document.getElementById('montoPoliza').value = '';
        }
    });
    
    await cargarCatalogo();
    await cargarClientes();
    await cargarOferentes();
    await cargarMarcas();
    await cargarTiposLicitacion();
    await cargarPortalesOrigen();
    await cargarModalidadesEntrega();
    await cargarFormasPago();
    
    // Cargar motivos de pérdida
    const responseMotivos = await fetch('/api/motivos-perdida');
    motivosPerdida = await responseMotivos.json();
    
    agregarProducto();
});

// Funciones para modales de creación rápida
let quickAddTipo = '';

function abrirModalNuevoCliente() {
    cargarOrganismosModal();
    document.getElementById('nuevoClienteNombre').value = '';
    document.getElementById('nuevoClienteRazon').value = '';
    document.getElementById('nuevoClienteOrganismo').value = '';
    document.getElementById('modalNuevoCliente').style.display = 'block';
}

function cerrarModalNuevoCliente() {
    document.getElementById('modalNuevoCliente').style.display = 'none';
}

async function cargarOrganismosModal() {
    const response = await fetch('/api/organismos');
    const organismos = await response.json();
    const select = document.getElementById('nuevoClienteOrganismo');
    select.innerHTML = '<option value="">Seleccione...</option>';
    organismos.forEach(o => {
        select.innerHTML += `<option value="${o.nombre}">${o.nombre}</option>`;
    });
}

document.getElementById('nuevoClienteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nombre: document.getElementById('nuevoClienteNombre').value,
        razon_social: document.getElementById('nuevoClienteRazon').value,
        organismo_jurisdiccion: document.getElementById('nuevoClienteOrganismo').value
    };
    
    const response = await fetch('/api/clientes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    
    if (result.success) {
        await cargarClientes();
        document.getElementById('clienteSelect').value = result.id;
        seleccionarCliente();
        cerrarModalNuevoCliente();
        mostrarMensaje('Cliente agregado', 'success');
    } else {
        alert('Error: ' + result.error);
    }
});

function abrirModalNuevoTipo() {
    quickAddTipo = 'tipo';
    document.getElementById('quickAddTitulo').textContent = 'Nuevo Tipo de Licitación';
    document.getElementById('quickAddLabel').textContent = 'Nombre *';
    document.getElementById('quickAddNombre').value = '';
    document.getElementById('modalQuickAdd').style.display = 'block';
}

function abrirModalNuevoPortal() {
    quickAddTipo = 'portal';
    document.getElementById('quickAddTitulo').textContent = 'Nuevo Portal/Origen';
    document.getElementById('quickAddLabel').textContent = 'Nombre *';
    document.getElementById('quickAddNombre').value = '';
    document.getElementById('modalQuickAdd').style.display = 'block';
}

function abrirModalNuevoModalidad() {
    quickAddTipo = 'modalidad';
    document.getElementById('quickAddTitulo').textContent = 'Nueva Modalidad de Entrega';
    document.getElementById('quickAddLabel').textContent = 'Nombre *';
    document.getElementById('quickAddNombre').value = '';
    document.getElementById('modalQuickAdd').style.display = 'block';
}

function abrirModalNuevoFormaPago() {
    quickAddTipo = 'forma';
    document.getElementById('quickAddTitulo').textContent = 'Nueva Forma de Pago';
    document.getElementById('quickAddLabel').textContent = 'Nombre *';
    document.getElementById('quickAddNombre').value = '';
    document.getElementById('modalQuickAdd').style.display = 'block';
}

function cerrarModalQuickAdd() {
    document.getElementById('modalQuickAdd').style.display = 'none';
}

document.getElementById('quickAddForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('quickAddNombre').value;
    
    let endpoint = '';
    let selectId = '';
    let recargarFn = null;
    
    if (quickAddTipo === 'tipo') {
        endpoint = '/api/tipos-licitacion';
        selectId = 'tipoLicitacionSelect';
        recargarFn = cargarTiposLicitacion;
    } else if (quickAddTipo === 'portal') {
        endpoint = '/api/portales-origen';
        selectId = 'portalOrigen';
        recargarFn = cargarPortalesOrigen;
    } else if (quickAddTipo === 'modalidad') {
        endpoint = '/api/modalidades-entrega';
        selectId = 'modalidadEntrega';
        recargarFn = cargarModalidadesEntrega;
    } else if (quickAddTipo === 'forma') {
        endpoint = '/api/formas-pago';
        selectId = 'formaPago';
        recargarFn = cargarFormasPago;
    }
    
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const result = await response.json();
    
    if (result.success) {
        await recargarFn();
        if (quickAddTipo === 'tipo') {
            document.getElementById(selectId).value = result.id;
        } else {
            document.getElementById(selectId).value = nombre;
        }
        cerrarModalQuickAdd();
        mostrarMensaje('Agregado correctamente', 'success');
    } else {
        alert('Error: ' + result.error);
    }
});
