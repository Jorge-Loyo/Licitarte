// Copiar todo el código de ingreso.js y agregar funcionalidad de carga
let productoCount = 0;
let catalogoProductos = [];
let clientes = [];
let tiposLicitacion = [];
let licitacionId = null;
let alternativaCount = 0;

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

async function cargarMantenimientosOferta() {
    try {
        const response = await fetch('/api/mantenimientos-oferta');
        const mantenimientos = await response.json();
        const select = document.getElementById('mantenimientoOferta');
        select.innerHTML = '<option value="">Seleccione...</option>';
        mantenimientos.forEach(m => {
            select.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando mantenimientos:', error);
    }
}

async function cargarLicitacion() {
    const path = window.location.pathname;
    licitacionId = path.split('/').pop();
    
    try {
        // Obtener datos completos de la licitación
        const detResponse = await fetch(`/api/licitaciones/${licitacionId}/detalle`);
        const detalle = await detResponse.json();
        
        if (!detalle || detalle.error) {
            alert('Licitación no encontrada');
            window.location.href = '/gestion';
            return;
        }
        
        // Llenar formulario básico
        document.getElementById('licitacionId').value = detalle.id;
        document.getElementById('numeroLicitacion').value = detalle.numero;
        
        // Separar fecha y hora
        const fechaHora = detalle.fecha.split(' ');
        document.getElementById('fecha').value = fechaHora[0];
        document.getElementById('horaApertura').value = fechaHora[1] || '10:00';
        
        // Mostrar fecha de carga si existe
        if (detalle.fecha_carga) {
            const fechaCarga = new Date(detalle.fecha_carga);
            document.getElementById('fechaCarga').value = fechaCarga.toLocaleDateString('es-AR');
        }
        
        // Seleccionar cliente y tipo
        document.getElementById('clienteSelect').value = detalle.cliente_id || '';
        seleccionarCliente();
        document.getElementById('tipoLicitacionSelect').value = detalle.tipo_licitacion_id || '';
        
        // Llenar campos adicionales
        document.getElementById('portalOrigen').value = detalle.portal_origen || '';
        document.getElementById('modalidadEntrega').value = detalle.modalidad_entrega || '';
        document.getElementById('formaPago').value = detalle.forma_pago || '';
        document.getElementById('mantenimientoOferta').value = detalle.mantenimiento_oferta || '';
        document.getElementById('tipoAdjudicacion').value = detalle.tipo_adjudicacion || 'Parcial';
        document.getElementById('observaciones').value = detalle.observaciones || '';
        
        // Póliza
        if (detalle.requiere_poliza) {
            document.getElementById('requierePoliza').checked = true;
            document.getElementById('porcentajePoliza').disabled = false;
            if (detalle.porcentaje_poliza) {
                document.getElementById('porcentajePoliza').value = detalle.porcentaje_poliza;
            }
        }
        
        manejarTipoAdjudicacion();
        
        // Cargar productos
        const prodResponse = await fetch(`/api/productos/${licitacionId}`);
        const productos = await prodResponse.json();
        
        for (const p of productos) {
            agregarProductoConDatos(p);
            
            // Cargar alternativas para este producto
            const altResponse = await fetch(`/api/alternativas/${p.id}`);
            const alternativas = await altResponse.json();
            
            if (alternativas && alternativas.length > 0) {
                const productoIndex = productoCount - 1;
                for (const alt of alternativas) {
                    agregarAlternativaConDatos(productoIndex, alt);
                }
            }
            
            // Establecer el valor del select producto-seleccionado
            const productoDiv = document.getElementById(`producto-${productoCount - 1}`);
            if (productoDiv && productoDiv.dataset.productoCotizar) {
                const selector = productoDiv.querySelector('.producto-seleccionado');
                if (selector) {
                    selector.value = productoDiv.dataset.productoCotizar;
                }
            }
        }
        
        calcularMontoPoliza();
        
    } catch (error) {
        console.error('Error cargando licitación:', error);
        alert('Error cargando datos: ' + error.message);
    }
}

function agregarProductoConDatos(datos) {
    const container = document.getElementById('productosContainer');
    const div = document.createElement('div');
    div.className = 'producto-item';
    div.id = `producto-${productoCount}`;
    div.dataset.productoId = datos.id;
    
    const totalRenglon = (datos.cantidad || 0) * (datos.precio_ofertado || 0);
    const totalRenglonFormateado = totalRenglon > 0 ? '$' + totalRenglon.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '';
    
    div.innerHTML = `
        <div style="background: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 15px; position: relative;">
            <button type="button" class="btn-remove" onclick="eliminarProducto(${productoCount})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-size: 18px;">✕</button>
            
            <h4 style="color: var(--primary); margin-bottom: 15px; font-size: 14px;">PRODUCTO #${productoCount + 1}</h4>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Renglón Nº</label>
                    <input type="text" class="producto-numero-renglon" value="${datos.numero_renglon || ''}" placeholder="210" style="font-size: 16px; padding: 12px; width: 100px;">
                </div>
                <div class="form-group">
                    <label>Monodroga *</label>
                    <input type="text" class="producto-monodroga" value="${datos.monodroga}" readonly style="font-size: 16px; padding: 12px; background: #333;">
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Marca - Presentación *</label>
                    <input type="text" value="${datos.marca} - ${datos.presentacion}" readonly style="font-size: 16px; padding: 12px; background: #333;">
                </div>
                <div class="form-group">
                    <label>Laboratorio</label>
                    <input type="text" class="producto-marca-ofrecida" value="${datos.marca_ofrecida || ''}" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Cantidad *</label>
                    <input type="number" class="producto-cantidad" value="${datos.cantidad}" required oninput="calcularTotalRenglon(this)" style="font-size: 16px; padding: 12px;">
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Costo Unitario</label>
                    <input type="number" step="0.01" class="producto-costo-unitario" value="${datos.costo_unitario || ''}" oninput="calcularPrecioOfertado(this)" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Margen (%)</label>
                    <input type="number" step="0.01" class="producto-margen-deseado" value="${datos.margen_porcentaje || ''}" oninput="calcularPrecioOfertado(this)" placeholder="Ej: 15" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Precio Ofertado *</label>
                    <input type="number" step="0.01" class="producto-precio" value="${datos.precio_ofertado}" required readonly style="background: #333; cursor: not-allowed; font-size: 16px; padding: 12px; font-weight: bold; color: var(--primary);">
                </div>
            </div>
            <div class="form-group">
                <label>Total de Renglón</label>
                <input type="text" class="producto-total-renglon" value="${totalRenglonFormateado}" readonly style="background: #333; cursor: not-allowed; font-size: 16px; padding: 12px; font-weight: bold; color: var(--primary); max-width: 250px;">
            </div>
            <div class="form-group">
                <label>Observaciones del Renglón</label>
                <input type="text" class="producto-observaciones" value="${datos.observaciones || ''}" placeholder="Notas específicas de este renglón..." style="font-size: 16px; padding: 12px;">
            </div>
            <div style="margin-top: 15px; padding: 15px; background: #0d0d0d; border-radius: 8px; border-left: 3px solid var(--primary);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h5 style="color: var(--primary); margin: 0; font-size: 14px;">ALTERNATIVAS</h5>
                    <button type="button" onclick="agregarAlternativa(${productoCount})" class="btn-primary" style="padding: 8px 15px; font-size: 14px; border-radius: 6px;">+ Agregar Alternativa</button>
                </div>
                <div class="alternativas-container"></div>
            </div>
            <div class="form-group" style="margin-top: 15px;">
                <label>Producto a Cotizar</label>
                <select class="producto-seleccionado" onchange="recalcularTotales()" style="font-size: 16px; padding: 12px;">
                    <option value="principal">Producto Principal</option>
                </select>
            </div>
            <input type="hidden" class="producto-marca" value="${datos.marca}">
            <input type="hidden" class="producto-presentacion" value="${datos.presentacion}">
            <input type="hidden" class="producto-resultado" value="${datos.resultado}">
        </div>
    `;
    
    container.appendChild(div);
    if (datos.costo_unitario) {
        div.dataset.costoUnitario = datos.costo_unitario;
    }
    
    // Guardar producto_cotizar para establecerlo después de cargar alternativas
    div.dataset.productoCotizar = datos.producto_cotizar || 'principal';
    
    productoCount++;
}

function agregarProducto() {
    const container = document.getElementById('productosContainer');
    const div = document.createElement('div');
    div.className = 'producto-item';
    div.id = `producto-${productoCount}`;
    
    // Obtener monodrogas únicas
    const monodrogasUnicas = [...new Set(catalogoProductos.map(p => p.monodroga))].sort();
    
    div.innerHTML = `
        <div style="background: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 15px; position: relative;">
            <button type="button" class="btn-remove" onclick="eliminarProducto(${productoCount})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-size: 18px;">✕</button>
            
            <h4 style="color: var(--primary); margin-bottom: 15px; font-size: 14px;">PRODUCTO #${productoCount + 1}</h4>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Renglón Nº</label>
                    <input type="text" class="producto-numero-renglon" placeholder="210" style="font-size: 16px; padding: 12px; width: 100px;">
                </div>
                <div class="form-group">
                    <label>Monodroga *</label>
                    <select class="producto-monodroga-select" onchange="filtrarMarcasPresentaciones(this)" style="font-size: 16px; padding: 12px;">
                        <option value="">Seleccione monodroga...</option>
                        ${monodrogasUnicas.map(m => `<option value="${m}">${m}</option>`).join('')}
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>Marca - Presentación *</label>
                <select class="producto-selector" onchange="seleccionarProducto(this)" disabled style="font-size: 16px; padding: 12px;">
                    <option value="">Primero seleccione monodroga...</option>
                </select>
            </div>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Marca - Presentación (Confirmación)</label>
                    <input type="text" class="producto-marca-presentacion" readonly style="font-size: 16px; padding: 12px; background: #333;">
                </div>
                <div class="form-group">
                    <label>Laboratorio</label>
                    <input type="text" class="producto-marca-ofrecida" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Cantidad *</label>
                    <input type="number" class="producto-cantidad" required oninput="calcularTotalRenglon(this)" style="font-size: 16px; padding: 12px;">
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Costo Unitario</label>
                    <input type="number" step="0.01" class="producto-costo-unitario" oninput="calcularPrecioOfertado(this)" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Margen (%)</label>
                    <input type="number" step="0.01" class="producto-margen-deseado" oninput="calcularPrecioOfertado(this)" placeholder="Ej: 15" style="font-size: 16px; padding: 12px;">
                </div>
                <div class="form-group">
                    <label>Precio Ofertado *</label>
                    <input type="number" step="0.01" class="producto-precio" required readonly style="background: #333; cursor: not-allowed; font-size: 16px; padding: 12px; font-weight: bold; color: var(--primary);">
                </div>
            </div>
            <div class="form-group">
                <label>Total de Renglón</label>
                <input type="text" class="producto-total-renglon" readonly style="background: #333; cursor: not-allowed; font-size: 16px; padding: 12px; font-weight: bold; color: var(--primary); max-width: 250px;">
            </div>
            <div class="form-group">
                <label>Observaciones del Renglón</label>
                <input type="text" class="producto-observaciones" placeholder="Notas específicas de este renglón..." style="font-size: 16px; padding: 12px;">
            </div>
            <div style="margin-top: 15px; padding: 15px; background: #0d0d0d; border-radius: 8px; border-left: 3px solid var(--primary);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h5 style="color: var(--primary); margin: 0; font-size: 14px;">ALTERNATIVAS</h5>
                    <button type="button" onclick="agregarAlternativa(${productoCount})" class="btn-primary" style="padding: 8px 15px; font-size: 14px; border-radius: 6px;">+ Agregar Alternativa</button>
                </div>
                <div class="alternativas-container"></div>
            </div>
            <div class="form-group" style="margin-top: 15px;">
                <label>Producto a Cotizar</label>
                <select class="producto-seleccionado" onchange="recalcularTotales()" style="font-size: 16px; padding: 12px;">
                    <option value="principal">Producto Principal</option>
                </select>
            </div>
            <input type="hidden" class="producto-monodroga">
            <input type="hidden" class="producto-marca">
            <input type="hidden" class="producto-presentacion">
            <input type="hidden" class="producto-resultado" value="Parcial">
        </div>
    `;
    
    container.appendChild(div);
    productoCount++;
}

function filtrarMarcasPresentaciones(select) {
    const monodroga = select.value;
    const container = select.closest('.producto-item');
    const selectorProducto = container.querySelector('.producto-selector');
    
    container.querySelector('.producto-monodroga').value = monodroga;
    
    if (!monodroga) {
        selectorProducto.disabled = true;
        selectorProducto.innerHTML = '<option value="">Primero seleccione monodroga...</option>';
        return;
    }
    
    const productosFiltrados = catalogoProductos.filter(p => p.monodroga === monodroga);
    
    selectorProducto.disabled = false;
    selectorProducto.innerHTML = '<option value="">Seleccione marca - presentación...</option>';
    productosFiltrados.forEach(p => {
        selectorProducto.innerHTML += `<option value="${p.id}" data-monodroga="${p.monodroga}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-laboratorio="${p.laboratorio || ''}" data-costo="${p.costo_unitario || 0}">${p.marca} - ${p.presentacion}</option>`;
    });
}

function seleccionarProducto(select) {
    const option = select.options[select.selectedIndex];
    const container = select.closest('.producto-item');
    
    const marca = option.dataset.marca || '';
    const presentacion = option.dataset.presentacion || '';
    const laboratorio = option.dataset.laboratorio || '';
    const costoUnitario = option.dataset.costo || 0;
    
    container.querySelector('.producto-monodroga').value = option.dataset.monodroga || '';
    container.querySelector('.producto-marca').value = marca;
    container.querySelector('.producto-presentacion').value = presentacion;
    container.querySelector('.producto-marca-presentacion').value = marca + ' - ' + presentacion;
    container.querySelector('.producto-marca-ofrecida').value = laboratorio;
    container.querySelector('.producto-costo-unitario').value = costoUnitario;
    container.dataset.costoUnitario = costoUnitario;
    
    calcularPrecioOfertado(container.querySelector('.producto-costo-unitario'));
}

function calcularPrecioOfertado(input) {
    const container = input.closest('.producto-item');
    const costoUnitario = parseFloat(container.querySelector('.producto-costo-unitario').value) || 0;
    const margenPorcentaje = parseFloat(container.querySelector('.producto-margen-deseado').value) || 0;
    
    const precioOfertado = costoUnitario * (1 + margenPorcentaje / 100);
    const precioInput = container.querySelector('.producto-precio');
    precioInput.value = precioOfertado > 0 ? precioOfertado.toFixed(2) : '';
    
    calcularTotalRenglon(container.querySelector('.producto-cantidad'));
}

function recalcularTotales() {
    calcularMontoPoliza();
    calcularMargenTotal();
}

function calcularTotalRenglon(input) {
    const container = input.closest('.producto-item');
    const cantidad = parseFloat(container.querySelector('.producto-cantidad').value) || 0;
    const precioOfertado = parseFloat(container.querySelector('.producto-precio').value) || 0;
    
    const totalRenglon = cantidad * precioOfertado;
    container.querySelector('.producto-total-renglon').value = totalRenglon > 0 ? '$' + totalRenglon.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '';
    
    // Recalcular totales de alternativas también
    const alternativas = container.querySelectorAll('.alternativa-item');
    alternativas.forEach(alt => {
        const precioAlt = parseFloat(alt.querySelector('.alt-precio').value) || 0;
        const totalAlt = cantidad * precioAlt;
        alt.querySelector('.alt-total-renglon').value = totalAlt > 0 ? '$' + totalAlt.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '';
    });
    
    calcularMontoPoliza();
    calcularMargenTotal();
}

function calcularMontoPoliza() {
    const productos = document.querySelectorAll('.producto-item');
    let montoTotal = 0;
    
    productos.forEach(item => {
        const cantidad = parseFloat(item.querySelector('.producto-cantidad').value) || 0;
        const precioPrincipal = parseFloat(item.querySelector('.producto-precio').value) || 0;
        
        // Calcular total del producto principal
        let totalMaximo = cantidad * precioPrincipal;
        
        // Comparar con totales de alternativas
        const alternativas = item.querySelectorAll('.alternativa-item');
        alternativas.forEach(alt => {
            const precioAlt = parseFloat(alt.querySelector('.alt-precio').value) || 0;
            const totalAlt = cantidad * precioAlt;
            if (totalAlt > totalMaximo) {
                totalMaximo = totalAlt;
            }
        });
        
        montoTotal += totalMaximo;
    });
    
    document.getElementById('montoTotalDisplay').value = '$' + montoTotal.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    
    const porcentaje = parseFloat(document.getElementById('porcentajePoliza').value) || 0;
    const montoPoliza = (montoTotal * porcentaje) / 100;
    
    document.getElementById('montoPolizaDisplay').value = '$' + montoPoliza.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('montoPoliza').value = montoPoliza;
}

function manejarTipoAdjudicacion() {
    const tipo = document.getElementById('tipoAdjudicacion').value;
    const margenContainer = document.getElementById('margenTotalContainer');
    
    if (tipo === 'Total') {
        margenContainer.style.display = 'block';
        calcularMargenTotal();
    } else {
        margenContainer.style.display = 'none';
    }
}

function calcularMargenTotal() {
    const tipo = document.getElementById('tipoAdjudicacion').value;
    if (tipo !== 'Total') return;
    
    const productos = document.querySelectorAll('.producto-item');
    let costoTotal = 0;
    let precioTotal = 0;
    
    productos.forEach(item => {
        const cantidad = parseFloat(item.querySelector('.producto-cantidad').value) || 0;
        const selector = item.querySelector('.producto-seleccionado');
        const seleccionado = selector.value;
        
        let costoUnitario = 0;
        let precioOfertado = 0;
        
        if (seleccionado === 'principal') {
            costoUnitario = parseFloat(item.querySelector('.producto-costo-unitario').value) || 0;
            precioOfertado = parseFloat(item.querySelector('.producto-precio').value) || 0;
        } else {
            const alt = document.getElementById(seleccionado);
            if (alt) {
                costoUnitario = parseFloat(alt.querySelector('.alt-costo').value) || 0;
                precioOfertado = parseFloat(alt.querySelector('.alt-precio').value) || 0;
            }
        }
        
        costoTotal += cantidad * costoUnitario;
        precioTotal += cantidad * precioOfertado;
    });
    
    const margenTotal = precioTotal - costoTotal;
    const margenPorcentaje = costoTotal > 0 ? (margenTotal / costoTotal) * 100 : 0;
    
    document.getElementById('costoTotalDisplay').value = '$' + costoTotal.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('precioTotalDisplay').value = '$' + precioTotal.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('margenTotalDisplay').value = '$' + margenTotal.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('margenTotalPorcentajeDisplay').value = margenPorcentaje.toFixed(2) + '%';
}

function eliminarProducto(id) {
    const item = document.getElementById(`producto-${id}`);
    const productoId = item.dataset.productoId;
    
    if (productoId) {
        // Marcar para eliminar del servidor
        if (!window.productosAEliminar) window.productosAEliminar = [];
        window.productosAEliminar.push(productoId);
    }
    
    item.remove();
    calcularMontoPoliza();
    calcularMargenTotal();
}

document.getElementById('licitacionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const productos = [];
    document.querySelectorAll('.producto-item').forEach(item => {
        const monodroga = item.querySelector('.producto-monodroga').value;
        const marca = item.querySelector('.producto-marca').value;
        const presentacion = item.querySelector('.producto-presentacion').value;
        
        if (!monodroga || !marca || !presentacion) return;
        
        const producto = {
            monodroga: monodroga,
            marca: marca,
            presentacion: presentacion,
            cantidad: item.querySelector('.producto-cantidad').value,
            precio_ofertado: item.querySelector('.producto-precio').value,
            resultado: item.querySelector('.producto-resultado').value,
            marca_ofrecida: item.querySelector('.producto-marca-ofrecida').value,
            numero_renglon: item.querySelector('.producto-numero-renglon').value,
            costo_unitario: item.querySelector('.producto-costo-unitario').value,
            margen_porcentaje: item.querySelector('.producto-margen-deseado').value,
            observaciones: item.querySelector('.producto-observaciones').value,
            producto_cotizar: item.querySelector('.producto-seleccionado') ? item.querySelector('.producto-seleccionado').value : 'principal'
        };
        
        console.log('DEBUG - Producto a guardar:', producto);
        
        if (item.dataset.productoId) {
            producto.id = item.dataset.productoId;
        }
        
        // Recopilar alternativas
        const alternativas = [];
        item.querySelectorAll('.alternativa-item').forEach(alt => {
            const altMarca = alt.querySelector('.alt-marca').value;
            const altPresentacion = alt.querySelector('.alt-presentacion').value;
            if (altMarca && altPresentacion) {
                alternativas.push({
                    marca: altMarca,
                    presentacion: altPresentacion,
                    laboratorio: alt.querySelector('.alt-laboratorio').value,
                    costo_unitario: alt.querySelector('.alt-costo').value,
                    margen_porcentaje: alt.querySelector('.alt-margen').value,
                    precio_ofertado: alt.querySelector('.alt-precio').value,
                    observaciones: alt.querySelector('.alt-observaciones').value
                });
            }
        });
        producto.alternativas = alternativas;
        
        productos.push(producto);
    });
    
    if (productos.length === 0) {
        mostrarMensaje('Agregue al menos un producto', 'error');
        return;
    }
    
    const data = {
        numero: document.getElementById('numeroLicitacion').value,
        cliente_id: document.getElementById('clienteSelect').value,
        tipo_licitacion_id: document.getElementById('tipoLicitacionSelect').value || null,
        fecha: document.getElementById('fecha').value + ' ' + document.getElementById('horaApertura').value,
        portal_origen: document.getElementById('portalOrigen').value,
        modalidad_entrega: document.getElementById('modalidadEntrega').value,
        forma_pago: document.getElementById('formaPago').value,
        requiere_poliza: document.getElementById('requierePoliza').checked,
        monto_poliza: document.getElementById('montoPoliza').value || null,
        observaciones: document.getElementById('observaciones').value,
        mantenimiento_oferta: document.getElementById('mantenimientoOferta').value,
        tipo_adjudicacion: document.getElementById('tipoAdjudicacion').value
    };
    
    try {
        // Actualizar licitación
        const response = await fetch(`/api/licitaciones/${licitacionId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Actualizar/crear productos y alternativas
            for (const prod of productos) {
                let productoId = prod.id;
                
                console.log('DEBUG - Guardando producto:', prod);
                
                if (prod.id) {
                    await fetch(`/api/productos/${prod.id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(prod)
                    });
                } else {
                    prod.licitacion_id = licitacionId;
                    const prodResponse = await fetch('/api/productos', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(prod)
                    });
                    const prodResult = await prodResponse.json();
                    productoId = prodResult.id;
                }
                
                // Eliminar alternativas existentes y crear nuevas
                if (productoId) {
                    await fetch(`/api/alternativas/${productoId}`, { method: 'DELETE' });
                    
                    for (const alt of prod.alternativas) {
                        alt.producto_id = productoId;
                        await fetch('/api/alternativas', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(alt)
                        });
                    }
                }
            }
            
            mostrarMensaje('Licitación actualizada correctamente', 'success');
            setTimeout(() => {
                window.location.href = '/gestion';
            }, 1500);
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

function agregarAlternativa(productoId) {
    const producto = document.getElementById(`producto-${productoId}`);
    const container = producto.querySelector('.alternativas-container');
    const monodroga = producto.querySelector('.producto-monodroga').value;
    const selector = producto.querySelector('.producto-seleccionado');
    
    if (!monodroga) {
        mostrarMensaje('Primero seleccione la monodroga del producto principal', 'error');
        return;
    }
    
    const altId = `alt-${productoId}-${alternativaCount}`;
    alternativaCount++;
    
    const div = document.createElement('div');
    div.className = 'alternativa-item';
    div.id = altId;
    div.style.cssText = 'background: #1a1a1a; padding: 15px; border-radius: 6px; margin-top: 10px; position: relative;';
    
    div.innerHTML = `
        <button type="button" onclick="eliminarAlternativa('${altId}', ${productoId})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-size: 14px;">✕</button>
        <h6 style="color: #999; margin-bottom: 10px; font-size: 13px;">Alternativa #${alternativaCount}</h6>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
            <div class="form-group" style="position: relative;">
                <label style="font-size: 14px;">Laboratorio *</label>
                <input type="text" class="alt-laboratorio-input" oninput="buscarLaboratorioAlternativa(this, '${monodroga}')" placeholder="Escriba para buscar..." style="font-size: 14px; padding: 10px;">
                <div class="alt-laboratorio-sugerencias" style="display: none; position: absolute; background: #1a1a1a; border: 1px solid var(--primary); border-radius: 5px; max-height: 200px; overflow-y: auto; z-index: 1000; width: calc(100% - 20px);"></div>
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Marca - Presentación *</label>
                <select class="alt-selector" onchange="seleccionarAlternativa(this)" disabled style="font-size: 14px; padding: 10px;">
                    <option value="">Primero seleccione laboratorio...</option>
                </select>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
            <div class="form-group">
                <label style="font-size: 14px;">Costo Unitario</label>
                <input type="number" step="0.01" class="alt-costo" oninput="calcularPrecioAlternativa(this)" style="font-size: 14px; padding: 10px;">
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Margen (%)</label>
                <input type="number" step="0.01" class="alt-margen" oninput="calcularPrecioAlternativa(this)" style="font-size: 14px; padding: 10px;">
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Precio Ofertado</label>
                <input type="number" step="0.01" class="alt-precio" readonly style="background: #2a2a2a; font-size: 14px; padding: 10px; font-weight: bold; color: var(--primary);">
            </div>
        </div>
        <div class="form-group" style="margin-top: 10px;">
            <label style="font-size: 14px;">Total de Renglón (Alternativa)</label>
            <input type="text" class="alt-total-renglon" readonly style="background: #2a2a2a; cursor: not-allowed; font-size: 14px; padding: 10px; font-weight: bold; color: var(--primary); max-width: 250px;">
        </div>
        <div class="form-group" style="margin-top: 10px;">
            <label style="font-size: 14px;">Observaciones de la Alternativa</label>
            <input type="text" class="alt-observaciones" placeholder="Notas específicas de esta alternativa..." style="font-size: 14px; padding: 10px;">
        </div>
        <input type="hidden" class="alt-marca">
        <input type="hidden" class="alt-presentacion">
        <input type="hidden" class="alt-laboratorio">
    `;
    
    container.appendChild(div);
    
    const option = document.createElement('option');
    option.value = altId;
    option.textContent = `Alternativa #${alternativaCount}`;
    selector.appendChild(option);
}

async function buscarLaboratorioAlternativa(input, monodroga) {
    const texto = input.value.trim();
    const container = input.closest('.alternativa-item');
    const sugerencias = container.querySelector('.alt-laboratorio-sugerencias');
    const selectorMarca = container.querySelector('.alt-selector');
    
    if (texto.length === 0) {
        sugerencias.style.display = 'none';
        selectorMarca.innerHTML = '<option value="">Primero seleccione laboratorio...</option>';
        selectorMarca.disabled = true;
        return;
    }
    
    try {
        const response = await fetch(`/api/laboratorios/buscar?monodroga=${encodeURIComponent(monodroga)}&q=${encodeURIComponent(texto)}`);
        const laboratorios = await response.json();
        
        if (laboratorios.length === 0) {
            sugerencias.style.display = 'none';
            return;
        }
        
        sugerencias.innerHTML = laboratorios.map(lab => 
            `<div onclick="seleccionarLaboratorioAlternativa(this, '${lab.nombre.replace(/'/g, "\\'")}')"
                  style="padding: 10px; cursor: pointer; border-bottom: 1px solid #333;">
                ${lab.nombre}
             </div>`
        ).join('');
        
        sugerencias.style.display = 'block';
    } catch (error) {
        console.error('Error buscando laboratorios:', error);
        sugerencias.style.display = 'none';
    }
}

function seleccionarLaboratorioAlternativa(element, laboratorio) {
    const container = element.closest('.alternativa-item');
    const input = container.querySelector('.alt-laboratorio-input');
    const sugerencias = container.querySelector('.alt-laboratorio-sugerencias');
    const hiddenLaboratorio = container.querySelector('.alt-laboratorio');
    const selectorMarca = container.querySelector('.alt-selector');
    const producto = container.closest('.producto-item');
    const monodroga = producto.querySelector('.producto-monodroga').value;
    
    input.value = laboratorio;
    hiddenLaboratorio.value = laboratorio;
    sugerencias.style.display = 'none';
    
    const productosFiltrados = catalogoProductos.filter(p => 
        p.monodroga && p.monodroga.toLowerCase() === monodroga.toLowerCase() &&
        p.laboratorio && p.laboratorio.toLowerCase() === laboratorio.toLowerCase()
    );
    
    selectorMarca.innerHTML = '<option value="">Seleccione marca - presentación...</option>';
    productosFiltrados.forEach(p => {
        selectorMarca.innerHTML += `<option value="${p.numero_registro}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-costo="${p.costo_unitario || 0}">
            ${p.marca} - ${p.presentacion}
        </option>`;
    });
    selectorMarca.disabled = false;
}

function seleccionarAlternativa(select) {
    const option = select.options[select.selectedIndex];
    const container = select.closest('.alternativa-item');
    
    container.querySelector('.alt-marca').value = option.dataset.marca || '';
    container.querySelector('.alt-presentacion').value = option.dataset.presentacion || '';
    container.querySelector('.alt-costo').value = option.dataset.costo || '';
    
    calcularPrecioAlternativa(container.querySelector('.alt-costo'));
}

function calcularPrecioAlternativa(input) {
    const container = input.closest('.alternativa-item');
    const costo = parseFloat(container.querySelector('.alt-costo').value) || 0;
    const margen = parseFloat(container.querySelector('.alt-margen').value) || 0;
    
    const precio = costo * (1 + margen / 100);
    container.querySelector('.alt-precio').value = precio > 0 ? precio.toFixed(2) : '';
    
    const productoItem = container.closest('.producto-item');
    const cantidad = parseFloat(productoItem.querySelector('.producto-cantidad').value) || 0;
    const totalRenglon = cantidad * precio;
    container.querySelector('.alt-total-renglon').value = totalRenglon > 0 ? '$' + totalRenglon.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '';
    
    calcularMontoPoliza();
    calcularMargenTotal();
}

function eliminarAlternativa(altId, productoId) {
    document.getElementById(altId).remove();
    calcularMontoPoliza();
    calcularMargenTotal();
}

function agregarAlternativaConDatos(productoId, datos) {
    const producto = document.getElementById(`producto-${productoId}`);
    const container = producto.querySelector('.alternativas-container');
    const selector = producto.querySelector('.producto-seleccionado');
    
    const altId = `alt-${productoId}-${alternativaCount}`;
    alternativaCount++;
    
    const div = document.createElement('div');
    div.className = 'alternativa-item';
    div.id = altId;
    div.dataset.alternativaId = datos.id;
    div.style.cssText = 'background: #1a1a1a; padding: 15px; border-radius: 6px; margin-top: 10px; position: relative;';
    
    div.innerHTML = `
        <button type="button" onclick="eliminarAlternativa('${altId}', ${productoId})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-size: 14px;">✕</button>
        <h6 style="color: #999; margin-bottom: 10px; font-size: 13px;">Alternativa #${alternativaCount}</h6>
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px; margin-bottom: 10px;">
            <div class="form-group">
                <label style="font-size: 14px;">Marca - Presentación</label>
                <input type="text" value="${datos.marca} - ${datos.presentacion}" readonly style="font-size: 14px; padding: 10px; background: #2a2a2a;">
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Laboratorio</label>
                <input type="text" class="alt-laboratorio" value="${datos.laboratorio || ''}" style="font-size: 14px; padding: 10px;">
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
            <div class="form-group">
                <label style="font-size: 14px;">Costo Unitario</label>
                <input type="number" step="0.01" class="alt-costo" value="${datos.costo_unitario || ''}" oninput="calcularPrecioAlternativa(this)" style="font-size: 14px; padding: 10px;">
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Margen (%)</label>
                <input type="number" step="0.01" class="alt-margen" value="${datos.margen_porcentaje || ''}" oninput="calcularPrecioAlternativa(this)" style="font-size: 14px; padding: 10px;">
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Precio Ofertado</label>
                <input type="number" step="0.01" class="alt-precio" value="${datos.precio_ofertado || ''}" readonly style="background: #2a2a2a; font-size: 14px; padding: 10px; font-weight: bold; color: var(--primary);">
            </div>
        </div>
        <div class="form-group" style="margin-top: 10px;">
            <label style="font-size: 14px;">Total de Renglón (Alternativa)</label>
            <input type="text" class="alt-total-renglon" readonly style="background: #2a2a2a; cursor: not-allowed; font-size: 14px; padding: 10px; font-weight: bold; color: var(--primary); max-width: 250px;">
        </div>
        <div class="form-group" style="margin-top: 10px;">
            <label style="font-size: 14px;">Observaciones de la Alternativa</label>
            <input type="text" class="alt-observaciones" value="${datos.observaciones || ''}" placeholder="Notas específicas de esta alternativa..." style="font-size: 14px; padding: 10px;">
        </div>
        <input type="hidden" class="alt-marca" value="${datos.marca}">
        <input type="hidden" class="alt-presentacion" value="${datos.presentacion}">
    `;
    
    container.appendChild(div);
    
    const option = document.createElement('option');
    option.value = altId;
    option.textContent = `Alternativa #${alternativaCount}`;
    selector.appendChild(option);
    
    calcularPrecioAlternativa(div.querySelector('.alt-costo'));
}

document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('requierePoliza').addEventListener('change', (e) => {
        document.getElementById('porcentajePoliza').disabled = !e.target.checked;
        if (!e.target.checked) {
            document.getElementById('porcentajePoliza').value = '';
            document.getElementById('montoPoliza').value = '';
            document.getElementById('montoPolizaDisplay').value = '';
        }
    });
    
    await cargarCatalogo();
    await cargarClientes();
    await cargarTiposLicitacion();
    await cargarPortalesOrigen();
    await cargarModalidadesEntrega();
    await cargarFormasPago();
    await cargarMantenimientosOferta();
    await cargarLicitacion();
});
