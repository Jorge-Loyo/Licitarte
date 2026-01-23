let productoCount = 0;
let catalogoProductos = [];
let clientes = [];
let oferentes = [];
let marcas = [];
let tiposLicitacion = [];

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
            select.innerHTML += `<option value="${c.id}">${c.nombre}</option>`;
        });
    } catch (error) {
        console.error('Error cargando clientes:', error);
    }
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
        <button type="button" class="btn-remove" onclick="eliminarProducto(${productoCount})">✕</button>
        <div class="form-group">
            <label>Marca - Presentación *</label>
            <select class="producto-selector" onchange="seleccionarProducto(this)">
                ${options}
            </select>
        </div>
        <div class="form-group">
            <label>Monodroga</label>
            <input type="text" class="producto-monodroga-display" readonly style="background: #333; cursor: not-allowed;">
        </div>
        <input type="hidden" class="producto-monodroga">
        <input type="hidden" class="producto-marca">
        <input type="hidden" class="producto-presentacion">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div class="form-group">
                <label>Cantidad *</label>
                <input type="number" class="producto-cantidad" required>
            </div>
            <div class="form-group">
                <label>Precio Ofertado *</label>
                <input type="number" step="0.01" class="producto-precio" required>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div class="form-group">
                <label>Resultado *</label>
                <select class="producto-resultado">
                    <option value="Adjudicado">Adjudicado</option>
                    <option value="Parcial">Parcial</option>
                    <option value="No Adjudicado">No Adjudicado</option>
                </select>
            </div>
            <div class="form-group">
                <label>Marca Ofrecida</label>
                <input type="text" class="producto-marca-ofrecida">
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
            <div class="form-group">
                <label>Oferente Ganador</label>
                <select class="producto-oferente-ganador">
                    <option value="">Seleccione...</option>
                    ${oferentes.map(o => `<option value="${o.nombre}">${o.nombre}</option>`).join('')}
                </select>
                <button type="button" onclick="nuevoOferente(this)" class="btn-secondary" style="margin-top: 5px; font-size: 12px;">+ Nuevo</button>
            </div>
            <div class="form-group">
                <label>Marca Ganadora</label>
                <select class="producto-marca-ganadora">
                    <option value="">Seleccione...</option>
                    ${marcas.map(m => `<option value="${m.nombre}">${m.nombre}</option>`).join('')}
                </select>
                <button type="button" onclick="nuevaMarca(this)" class="btn-secondary" style="margin-top: 5px; font-size: 12px;">+ Nuevo</button>
            </div>
            <div class="form-group">
                <label>Precio Ganador</label>
                <input type="number" step="0.01" class="producto-precio-ganador">
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
            precio_ganador: item.querySelector('.producto-precio-ganador').value
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
    const mensaje = document.getElementById('mensaje');
    mensaje.textContent = texto;
    mensaje.className = `mensaje ${tipo}`;
    mensaje.style.display = 'block';
    setTimeout(() => mensaje.style.display = 'none', 5000);
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
    await cargarCatalogo();
    await cargarClientes();
    await cargarOferentes();
    await cargarMarcas();
    await cargarTiposLicitacion();
    agregarProducto();
});
