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
        const response = await fetch('/api/catalogo?per_page=100000');
        const data = await response.json();
        catalogoProductos = data.productos || [];
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

function agregarProducto() {
    const container = document.getElementById('productosContainer');
    const div = document.createElement('div');
    div.className = 'producto-item';
    div.id = `producto-${productoCount}`;
    
    div.innerHTML = `
        <div style="background: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 15px; position: relative;">
            <button type="button" class="btn-remove" onclick="eliminarProducto(${productoCount})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-size: 18px;">✕</button>
            
            <h4 style="color: var(--primary); margin-bottom: 15px; font-size: 14px;">PRODUCTO #${productoCount + 1}</h4>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Renglón Nº</label>
                    <input type="text" class="producto-numero-renglon" oninput="validarNumeroRenglon(this)" placeholder="210" style="font-size: 16px; padding: 12px; width: 100px;">
                    <small class="renglon-error" style="color: var(--danger-color); display: none; margin-top: 5px;">Este número de renglón ya existe</small>
                </div>
                <div class="form-group" style="position: relative;">
                    <label>Monodroga *</label>
                    <input type="text" class="producto-monodroga-input" oninput="buscarMonodroga(this)" placeholder="Escriba al menos 3 letras..." style="font-size: 16px; padding: 12px;">
                    <div class="monodroga-sugerencias" style="display: none; position: absolute; background: #1a1a1a; border: 1px solid var(--primary); border-radius: 5px; max-height: 200px; overflow-y: auto; z-index: 1000; width: calc(100% - 40px);"></div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div class="form-group" style="position: relative;">
                    <label>Laboratorio *</label>
                    <input type="text" class="producto-laboratorio-input" oninput="buscarLaboratorio(this)" placeholder="Primero seleccione monodroga..." disabled style="font-size: 16px; padding: 12px;">
                    <div class="laboratorio-sugerencias" style="display: none; position: absolute; background: #1a1a1a; border: 1px solid var(--primary); border-radius: 5px; max-height: 200px; overflow-y: auto; z-index: 1000; width: calc(100% - 40px);"></div>
                </div>
                <div class="form-group">
                    <label>Marca - Presentación *</label>
                    <select class="producto-selector-marca-presentacion" onchange="seleccionarProducto(this)" disabled style="font-size: 16px; padding: 12px;">
                        <option value="">Primero seleccione laboratorio...</option>
                    </select>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr; gap: 15px;">
                <div class="form-group">
                    <label>Cantidad *</label>
                    <input type="number" class="producto-cantidad" required oninput="calcularTotalRenglon(this)" style="font-size: 16px; padding: 12px;">
                </div>
            </div>
            <input type="hidden" class="producto-laboratorio">
            <input type="hidden" class="producto-marca-ofrecida">
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
            <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px;">
                <div class="form-group">
                    <label>Total de Renglón</label>
                    <input type="text" class="producto-total-renglon" readonly style="background: #333; cursor: not-allowed; font-size: 16px; padding: 12px; font-weight: bold; color: var(--primary); max-width: 250px;">
                </div>
                <div></div>
            </div>
            <div class="form-group" style="margin-top: 15px;">
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
            <input type="hidden" class="producto-oferente-ganador">
            <input type="hidden" class="producto-marca-ganadora">
            <input type="hidden" class="producto-precio-ganador">
        </div>
    `;
    
    container.appendChild(div);
    productoCount++;
}

async function buscarMonodroga(input) {
    const texto = input.value.trim();
    const container = input.closest('.producto-item');
    const sugerencias = container.querySelector('.monodroga-sugerencias');
    
    if (texto.length < 3) {
        sugerencias.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/monodrogas/buscar?q=${encodeURIComponent(texto)}`);
        const monodrogas = await response.json();
        
        if (monodrogas.length === 0) {
            sugerencias.style.display = 'none';
            return;
        }
        
        sugerencias.innerHTML = monodrogas.map(m => 
            `<div onclick="seleccionarMonodroga(this, '${m.nombre.replace(/'/g, "\\'")}')"
                  style="padding: 10px; cursor: pointer; border-bottom: 1px solid #333;">
                ${capitalizarTexto(m.nombre)}
             </div>`
        ).join('');
        
        sugerencias.style.display = 'block';
    } catch (error) {
        console.error('Error buscando monodrogas:', error);
        sugerencias.style.display = 'none';
    }
}

async function seleccionarMonodroga(element, monodroga) {
    const container = element.closest('.producto-item');
    const input = container.querySelector('.producto-monodroga-input');
    const sugerencias = container.querySelector('.monodroga-sugerencias');
    const laboratorioInput = container.querySelector('.producto-laboratorio-input');
    const hiddenMonodroga = container.querySelector('.producto-monodroga');
    
    const monodrogaCapitalizada = capitalizarTexto(monodroga);
    input.value = monodrogaCapitalizada;
    hiddenMonodroga.value = monodrogaCapitalizada;
    sugerencias.style.display = 'none';
    
    // Habilitar input de laboratorio
    laboratorioInput.disabled = false;
    laboratorioInput.placeholder = 'Escriba para buscar...';
}

async function buscarLaboratorio(input) {
    const texto = input.value.trim();
    const container = input.closest('.producto-item');
    const monodroga = container.querySelector('.producto-monodroga').value;
    const sugerencias = container.querySelector('.laboratorio-sugerencias');
    const selectorMarcaPresentacion = container.querySelector('.producto-selector-marca-presentacion');
    
    if (!monodroga) {
        sugerencias.style.display = 'none';
        return;
    }
    
    if (texto.length === 0) {
        sugerencias.style.display = 'none';
        selectorMarcaPresentacion.innerHTML = '<option value="">Primero seleccione laboratorio...</option>';
        selectorMarcaPresentacion.disabled = true;
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
            `<div onclick="seleccionarLaboratorioSugerencia(this, '${lab.nombre.replace(/'/g, "\\'")}')"
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

function seleccionarLaboratorioSugerencia(element, laboratorio) {
    const container = element.closest('.producto-item');
    const input = container.querySelector('.producto-laboratorio-input');
    const sugerencias = container.querySelector('.laboratorio-sugerencias');
    const hiddenLaboratorio = container.querySelector('.producto-laboratorio');
    const monodroga = container.querySelector('.producto-monodroga').value;
    const selectorMarcaPresentacion = container.querySelector('.producto-selector-marca-presentacion');
    
    input.value = laboratorio;
    hiddenLaboratorio.value = laboratorio;
    sugerencias.style.display = 'none';
    
    const productosFiltrados = catalogoProductos.filter(p => 
        p.monodroga && p.monodroga.toLowerCase() === monodroga.toLowerCase() &&
        p.laboratorio && p.laboratorio.toLowerCase() === laboratorio.toLowerCase()
    );
    
    selectorMarcaPresentacion.innerHTML = '<option value="">Seleccione marca - presentación...</option>';
    productosFiltrados.forEach(p => {
        selectorMarcaPresentacion.innerHTML += `<option value="${p.numero_registro}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-laboratorio="${p.laboratorio || ''}" data-costo="${p.costo_unitario || 0}">
            ${p.marca} - ${p.presentacion}
        </option>`;
    });
    selectorMarcaPresentacion.disabled = false;
}

async function seleccionarLaboratorio(select) {
    const container = select.closest('.producto-item');
    const monodroga = container.querySelector('.producto-monodroga').value;
    const laboratorio = select.value;
    const selectorMarcaPresentacion = container.querySelector('.producto-selector-marca-presentacion');
    
    if (!laboratorio) {
        selectorMarcaPresentacion.innerHTML = '<option value="">Primero seleccione laboratorio...</option>';
        selectorMarcaPresentacion.disabled = true;
        return;
    }
    
    // Buscar productos que coincidan con monodroga y laboratorio
    const productosFiltrados = catalogoProductos.filter(p => 
        p.monodroga && p.monodroga.toLowerCase() === monodroga.toLowerCase() &&
        p.laboratorio && p.laboratorio.toLowerCase() === laboratorio.toLowerCase()
    );
    
    selectorMarcaPresentacion.innerHTML = '<option value="">Seleccione marca - presentación...</option>';
    productosFiltrados.forEach(p => {
        selectorMarcaPresentacion.innerHTML += `<option value="${p.numero_registro}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-laboratorio="${p.laboratorio || ''}" data-costo="${p.costo_unitario || 0}">
            ${p.marca} - ${p.presentacion}
        </option>`;
    });
    selectorMarcaPresentacion.disabled = false;
}



function seleccionarProducto(select) {
    const option = select.options[select.selectedIndex];
    const container = select.closest('.producto-item');
    
    const marca = option.dataset.marca || '';
    const presentacion = option.dataset.presentacion || '';
    const laboratorio = option.dataset.laboratorio || '';
    const costoUnitario = option.dataset.costo || 0;
    
    container.querySelector('.producto-marca').value = marca;
    container.querySelector('.producto-presentacion').value = presentacion;
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
    calcularMontoPoliza();
    calcularMargenTotal();
}

document.getElementById('licitacionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validar campos obligatorios
    const errores = validarFormularioCompleto();
    if (errores.length > 0) {
        mostrarMensaje(errores.join('\n'), 'error');
        return;
    }
    
    // Verificar si ya existe
    const existe = await verificarLicitacionExistente();
    if (existe) {
        mostrarMensaje('Ya existe una licitación con este número para el cliente seleccionado', 'error');
        return;
    }
    
    const productos = [];
    document.querySelectorAll('.producto-item').forEach(item => {
        const monodroga = item.querySelector('.producto-monodroga').value;
        const marca = item.querySelector('.producto-marca').value;
        const presentacion = item.querySelector('.producto-presentacion').value;
        
        if (!monodroga || !marca || !presentacion) {
            return;
        }
        
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
        
        productos.push({
            monodroga: monodroga,
            marca: marca,
            presentacion: presentacion,
            cantidad: item.querySelector('.producto-cantidad').value,
            precio: item.querySelector('.producto-precio').value,
            resultado: 'Parcial',
            marca_ofrecida: item.querySelector('.producto-marca-ofrecida').value,
            oferente_ganador: '',
            marca_ganadora: '',
            precio_ganador: null,
            motivo_perdida: '',
            numero_renglon: item.querySelector('.producto-numero-renglon').value,
            costo_unitario: item.querySelector('.producto-costo-unitario').value,
            margen_porcentaje: item.querySelector('.producto-margen-deseado').value,
            observaciones: item.querySelector('.producto-observaciones').value,
            producto_cotizar: item.querySelector('.producto-seleccionado').value,
            alternativas: alternativas
        });
    });
    
    const data = {
        numero: document.getElementById('numeroLicitacion').value,
        cliente_id: document.getElementById('clienteSelect').value,
        tipo_licitacion_id: document.getElementById('tipoLicitacionSelect').value,
        fecha: document.getElementById('fecha').value + ' ' + document.getElementById('horaApertura').value,
        portal_origen: document.getElementById('portalOrigen').value,
        modalidad_entrega: document.getElementById('modalidadEntrega').value,
        forma_pago: document.getElementById('formaPago').value,
        requiere_poliza: document.getElementById('requierePoliza').checked,
        monto_poliza: document.getElementById('montoPoliza').value || null,
        observaciones: document.getElementById('observaciones').value,
        mantenimiento_oferta: document.getElementById('mantenimientoOferta').value,
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
    document.getElementById('horaApertura').value = '10:00';
    
    // Habilitar/deshabilitar monto de póliza
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
    await cargarOferentes();
    await cargarMarcas();
    await cargarTiposLicitacion();
    await cargarPortalesOrigen();
    await cargarModalidadesEntrega();
    await cargarFormasPago();
    await cargarMantenimientosOferta();
    
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
    } else if (quickAddTipo === 'mantenimiento') {
        endpoint = '/api/mantenimientos-oferta';
        selectId = 'mantenimientoOferta';
        recargarFn = cargarMantenimientosOferta;
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

// Cerrar sugerencias al hacer clic fuera
document.addEventListener('click', (e) => {
    if (!e.target.classList.contains('producto-monodroga-input') && !e.target.classList.contains('producto-laboratorio-input')) {
        document.querySelectorAll('.monodroga-sugerencias').forEach(s => s.style.display = 'none');
        document.querySelectorAll('.laboratorio-sugerencias').forEach(s => s.style.display = 'none');
    }
});

function validarNumeroRenglon(input) {
    const numeroRenglon = input.value.trim();
    const container = input.closest('.producto-item');
    const errorMsg = container.querySelector('.renglon-error');
    
    if (!numeroRenglon) {
        errorMsg.style.display = 'none';
        return;
    }
    
    const productos = document.querySelectorAll('.producto-item');
    let duplicado = false;
    
    productos.forEach(item => {
        if (item !== container) {
            const otroNumero = item.querySelector('.producto-numero-renglon').value.trim();
            if (otroNumero === numeroRenglon) {
                duplicado = true;
            }
        }
    });
    
    if (duplicado) {
        errorMsg.style.display = 'block';
        input.style.borderColor = 'var(--danger-color)';
    } else {
        errorMsg.style.display = 'none';
        input.style.borderColor = '';
    }
}

let archivosPliegosSeleccionados = [];

function agregarPliegos(input) {
    const nuevosArchivos = Array.from(input.files);
    
    nuevosArchivos.forEach(archivo => {
        if (archivosPliegosSeleccionados.length < 10) {
            archivosPliegosSeleccionados.push(archivo);
        }
    });
    
    if (archivosPliegosSeleccionados.length > 10) {
        archivosPliegosSeleccionados = archivosPliegosSeleccionados.slice(0, 10);
        mostrarMensaje('Máximo 10 archivos permitidos', 'error');
    }
    
    input.value = '';
    actualizarListaPliegos();
}

function actualizarListaPliegos() {
    const lista = document.getElementById('pliegosList');
    const count = document.getElementById('pliegosCount');
    
    count.textContent = archivosPliegosSeleccionados.length;
    
    lista.innerHTML = archivosPliegosSeleccionados.map((archivo, index) => `
        <div style="display: flex; align-items: center; gap: 10px; padding: 8px; background: #1a1a1a; border-radius: 5px; margin-top: 5px;">
            <span style="flex: 1; font-size: 14px;">${archivo.name}</span>
            <button type="button" onclick="eliminarPliego(${index})" style="background: var(--danger-color); color: white; border: none; border-radius: 3px; padding: 5px 10px; cursor: pointer; font-size: 14px;">✕</button>
        </div>
    `).join('');
}

function eliminarPliego(index) {
    archivosPliegosSeleccionados.splice(index, 1);
    actualizarListaPliegos();
}

let alternativaCount = 0;

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
    
    const productosFiltrados = catalogoProductos.filter(p => 
        p.monodroga && p.monodroga.toLowerCase() === monodroga.toLowerCase()
    );
    
    let optionsMarca = '<option value="">Seleccione marca y presentación...</option>';
    productosFiltrados.forEach(p => {
        optionsMarca += `<option value="${p.numero_registro}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-laboratorio="${p.laboratorio || ''}" data-costo="${p.costo_unitario || 0}">
            ${p.marca} - ${p.presentacion}
        </option>`;
    });
    
    div.innerHTML = `
        <button type="button" onclick="eliminarAlternativa('${altId}', ${productoId})" style="position: absolute; top: 10px; right: 10px; background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-size: 14px;">✕</button>
        <h6 style="color: #999; margin-bottom: 10px; font-size: 13px;">Alternativa #${alternativaCount}</h6>
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px; margin-bottom: 10px;">
            <div class="form-group">
                <label style="font-size: 14px;">Marca - Presentación</label>
                <select class="alt-selector" onchange="seleccionarAlternativa(this)" style="font-size: 14px; padding: 10px;">
                    ${optionsMarca}
                </select>
            </div>
            <div class="form-group">
                <label style="font-size: 14px;">Laboratorio</label>
                <input type="text" class="alt-laboratorio" style="font-size: 14px; padding: 10px;">
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
    `;
    
    container.appendChild(div);
    
    const option = document.createElement('option');
    option.value = altId;
    option.textContent = `Alternativa #${alternativaCount}`;
    selector.appendChild(option);
}

function seleccionarAlternativa(select) {
    const option = select.options[select.selectedIndex];
    const container = select.closest('.alternativa-item');
    
    container.querySelector('.alt-marca').value = option.dataset.marca || '';
    container.querySelector('.alt-presentacion').value = option.dataset.presentacion || '';
    container.querySelector('.alt-laboratorio').value = option.dataset.laboratorio || '';
    container.querySelector('.alt-costo').value = option.dataset.costo || '';
    
    calcularPrecioAlternativa(container.querySelector('.alt-costo'));
}

function calcularPrecioAlternativa(input) {
    const container = input.closest('.alternativa-item');
    const costo = parseFloat(container.querySelector('.alt-costo').value) || 0;
    const margen = parseFloat(container.querySelector('.alt-margen').value) || 0;
    
    const precio = costo * (1 + margen / 100);
    container.querySelector('.alt-precio').value = precio > 0 ? precio.toFixed(2) : '';
    
    // Calcular total de renglón de la alternativa
    const productoItem = container.closest('.producto-item');
    const cantidad = parseFloat(productoItem.querySelector('.producto-cantidad').value) || 0;
    const totalRenglon = cantidad * precio;
    container.querySelector('.alt-total-renglon').value = totalRenglon > 0 ? '$' + totalRenglon.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '';
    
    recalcularTotales();
}

function eliminarAlternativa(altId, productoId) {
    const producto = document.getElementById(`producto-${productoId}`);
    const selector = producto.querySelector('.producto-seleccionado');
    
    document.getElementById(altId).remove();
    
    const option = selector.querySelector(`option[value="${altId}"]`);
    if (option) option.remove();
    
    if (selector.value === altId) {
        selector.value = 'principal';
    }
    
    recalcularTotales();
}

function recalcularTotales() {
    calcularMontoPoliza();
    calcularMargenTotal();
}


function validarFormularioCompleto() {
    const errores = [];
    
    // Validar datos básicos
    if (!document.getElementById('numeroLicitacion').value) errores.push('Número de licitación requerido');
    if (!document.getElementById('clienteSelect').value) errores.push('Cliente requerido');
    if (!document.getElementById('fecha').value) errores.push('Fecha requerida');
    
    // Validar productos
    const productos = document.querySelectorAll('.producto-item');
    if (productos.length === 0) {
        errores.push('Debe agregar al menos un producto');
        return errores;
    }
    
    const numerosRenglon = new Set();
    let productosValidos = 0;
    
    productos.forEach((item, index) => {
        const numeroRenglon = item.querySelector('.producto-numero-renglon').value.trim();
        const monodroga = item.querySelector('.producto-monodroga').value;
        const cantidad = item.querySelector('.producto-cantidad').value;
        const precio = item.querySelector('.producto-precio').value;
        
        // Solo validar productos que tienen al menos monodroga
        if (monodroga) {
            productosValidos++;
            
            if (!numeroRenglon) {
                errores.push(`Producto ${index + 1}: falta número de renglón`);
            } else if (numerosRenglon.has(numeroRenglon)) {
                errores.push(`Número de renglón duplicado: ${numeroRenglon}`);
            } else {
                numerosRenglon.add(numeroRenglon);
            }
            
            if (!cantidad) errores.push(`Producto ${index + 1}: falta cantidad`);
            if (!precio) errores.push(`Producto ${index + 1}: falta precio`);
        }
    });
    
    if (productosValidos === 0) {
        errores.push('Debe completar al menos un producto');
    }
    
    return errores;
}

async function verificarLicitacionExistente() {
    const numero = document.getElementById('numeroLicitacion').value;
    const clienteId = document.getElementById('clienteSelect').value;
    
    if (!numero || !clienteId) return false;
    
    try {
        const response = await fetch(`/api/licitaciones/verificar?numero=${encodeURIComponent(numero)}&cliente_id=${clienteId}`);
        const result = await response.json();
        return result.existe;
    } catch (error) {
        console.error('Error verificando licitación:', error);
        return false;
    }
}

async function generarVistaPrevia() {
    console.log('Generando vista previa...');
    
    // Validaciones básicas
    const numeroLicitacion = document.getElementById('numeroLicitacion').value;
    const clienteSelect = document.getElementById('clienteSelect');
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('horaApertura').value;
    
    if (!numeroLicitacion || !clienteSelect.value || !fecha) {
        alert('Complete los datos básicos: Número de licitación, Cliente y Fecha');
        return;
    }
    
    // Obtener siguiente número de presupuesto
    let numeroPresupuesto = 1;
    try {
        const response = await fetch('/api/presupuestos/siguiente-numero');
        const result = await response.json();
        numeroPresupuesto = result.numero;
    } catch (error) {
        console.error('Error obteniendo número de presupuesto:', error);
    }
    
    const clienteNombre = clienteSelect.options[clienteSelect.selectedIndex].text;
    
    // Recopilar productos
    const productosData = [];
    document.querySelectorAll('.producto-item').forEach(item => {
        const numeroRenglon = item.querySelector('.producto-numero-renglon').value.trim();
        const monodroga = item.querySelector('.producto-monodroga').value;
        const cantidad = item.querySelector('.producto-cantidad').value;
        
        if (!numeroRenglon || !monodroga || !cantidad) return;
        
        const selector = item.querySelector('.producto-seleccionado');
        const seleccionado = selector.value;
        
        // Producto principal
        let productoPrincipal = {
            numeroRenglon: numeroRenglon,
            numeroRenglonDisplay: numeroRenglon,
            monodroga: monodroga,
            cantidad: cantidad,
            marca: item.querySelector('.producto-marca').value,
            presentacion: item.querySelector('.producto-presentacion').value,
            laboratorio: item.querySelector('.producto-marca-ofrecida').value,
            precio: parseFloat(item.querySelector('.producto-precio').value) || 0,
            observaciones: item.querySelector('.producto-observaciones').value,
            esSeleccionado: seleccionado === 'principal'
        };
        
        productosData.push(productoPrincipal);
        
        // Alternativas
        const alternativas = item.querySelectorAll('.alternativa-item');
        alternativas.forEach((alt, altIndex) => {
            const altId = alt.id;
            const marca = alt.querySelector('.alt-marca').value;
            const presentacion = alt.querySelector('.alt-presentacion').value;
            
            if (marca && presentacion) {
                productosData.push({
                    numeroRenglon: numeroRenglon,
                    numeroRenglonDisplay: `${numeroRenglon}-ALT`,
                    monodroga: monodroga,
                    cantidad: cantidad,
                    marca: marca,
                    presentacion: presentacion,
                    laboratorio: alt.querySelector('.alt-laboratorio').value,
                    precio: parseFloat(alt.querySelector('.alt-precio').value) || 0,
                    observaciones: alt.querySelector('.alt-observaciones').value,
                    esSeleccionado: seleccionado === altId
                });
            }
        });
    });
    
    if (productosData.length === 0) {
        alert('Debe agregar al menos un producto completo');
        return;
    }
    
    console.log('Productos encontrados:', productosData.length);
    
    // Ordenar por número de renglón
    productosData.sort((a, b) => {
        const numA = parseInt(a.numeroRenglon);
        const numB = parseInt(b.numeroRenglon);
        if (numA !== numB) return numA - numB;
        if (a.numeroRenglonDisplay.includes('ALT') && !b.numeroRenglonDisplay.includes('ALT')) return 1;
        if (!a.numeroRenglonDisplay.includes('ALT') && b.numeroRenglonDisplay.includes('ALT')) return -1;
        return 0;
    });
    
    // Calcular total solo de productos seleccionados
    const total = productosData.filter(p => p.esSeleccionado).reduce((sum, p) => sum + (p.cantidad * p.precio), 0);
    
    // Generar HTML
    let html = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Presupuesto N° ${numeroPresupuesto} - Licitación ${numeroLicitacion}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: white; color: #333; }
                h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
                .info-box { margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-left: 4px solid #3498db; }
                .info-box p { margin: 5px 0; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
                thead tr { background: #3498db; color: white; }
                th { padding: 12px; text-align: left; border: 1px solid #ddd; }
                td { padding: 10px; border: 1px solid #ddd; }
                tbody tr:nth-child(even) { background: #f8f9fa; }
                .seleccionado { background: #d4edda !important; font-weight: bold; }
                .observacion { font-size: 13px; color: #666; font-style: italic; }
                tfoot tr { background: #2c3e50; color: white; font-weight: bold; }
                .footer { margin-top: 50px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #7f8c8d; }
                @media print {
                    body { margin: 20px; }
                    .no-print { display: none; }
                }
                .btn-toolbar { text-align: center; margin-bottom: 20px; }
                .btn { padding: 12px 30px; margin: 0 10px; font-size: 16px; cursor: pointer; border: none; border-radius: 5px; }
                .btn-primary { background: #3498db; color: white; }
                .btn-secondary { background: #95a5a6; color: white; }
            </style>
        </head>
        <body>
            <div class="btn-toolbar no-print">
                <button class="btn btn-primary" onclick="window.print()">🖨️ Imprimir</button>
                <button class="btn btn-secondary" onclick="window.close()">✕ Cerrar</button>
            </div>
            
            <h1>Presupuesto N° ${numeroPresupuesto}</h1>
            
            <div class="info-box">
                <p><strong>Cliente:</strong> ${clienteNombre}</p>
                <p><strong>Licitación N°:</strong> ${numeroLicitacion}</p>
                <p><strong>Fecha:</strong> ${new Date(fecha).toLocaleDateString('es-AR')}</p>
                <p><strong>Hora:</strong> ${hora}hs</p>
                ${document.getElementById('mantenimientoOferta').value ? `<p><strong>Mantenimiento de Oferta:</strong> ${document.getElementById('mantenimientoOferta').value}</p>` : ''}
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th style="text-align: center;">Renglón</th>
                        <th>Monodroga</th>
                        <th>Marca - Presentación</th>
                        <th>Laboratorio</th>
                        <th style="text-align: center;">Cantidad</th>
                        <th style="text-align: right;">Precio Unit.</th>
                        <th style="text-align: right;">Total</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    productosData.forEach((p, index) => {
        const totalRenglon = p.cantidad * p.precio;
        const claseSeleccionado = p.esSeleccionado ? 'seleccionado' : '';
        
        html += `
            <tr class="${claseSeleccionado}">
                <td style="text-align: center; font-weight: bold;">${p.numeroRenglonDisplay}</td>
                <td>${p.monodroga}</td>
                <td>${p.marca} - ${p.presentacion}</td>
                <td>${p.laboratorio}</td>
                <td style="text-align: center;">${p.cantidad}</td>
                <td style="text-align: right;">$${p.precio.toLocaleString('es-AR', {minimumFractionDigits: 2})}</td>
                <td style="text-align: right; font-weight: bold;">$${totalRenglon.toLocaleString('es-AR', {minimumFractionDigits: 2})}</td>
            </tr>
        `;
        if (p.observaciones) {
            html += `
                <tr class="${claseSeleccionado}">
                    <td colspan="7" class="observacion">Obs: ${p.observaciones}</td>
                </tr>
            `;
        }
    });
    
    html += `
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="6" style="text-align: right; padding: 15px;">TOTAL OFERTA:</td>
                        <td style="text-align: right; padding: 15px; font-size: 18px;">$${total.toLocaleString('es-AR', {minimumFractionDigits: 2})}</td>
                    </tr>
                </tfoot>
            </table>
            
            <div class="footer">
                <p>Documento generado por Licitarte</p>
                <p style="font-size: 12px;">Este documento es una vista previa de la oferta</p>
            </div>
        </body>
        </html>
    `;
    
    // Abrir en nueva pestaña
    const ventana = window.open('', '_blank');
    ventana.document.write(html);
    ventana.document.close();
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

function abrirModalNuevoMantenimiento() {
    quickAddTipo = 'mantenimiento';
    document.getElementById('quickAddTitulo').textContent = 'Nuevo Mantenimiento de Oferta';
    document.getElementById('quickAddLabel').textContent = 'Nombre *';
    document.getElementById('quickAddNombre').value = '';
    document.getElementById('modalQuickAdd').style.display = 'block';
}
