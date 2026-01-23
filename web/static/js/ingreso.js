let productoCount = 0;
let catalogoProductos = [];
let clientes = [];

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

function nuevoCliente() {
    const nombre = prompt('Nombre del cliente:');
    if (!nombre) return;
    
    fetch('/api/clientes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            cargarClientes();
            mostrarMensaje('Cliente agregado', 'success');
        } else {
            mostrarMensaje('Error: ' + result.error, 'error');
        }
    });
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
            marca_ofrecida: item.querySelector('.producto-marca-ofrecida').value
        });
    });
    
    if (productos.length === 0) {
        mostrarMensaje('Agregue al menos un producto y complete todos los campos', 'error');
        return;
    }
    
    const data = {
        numero: document.getElementById('numeroLicitacion').value,
        cliente_id: document.getElementById('clienteSelect').value,
        fecha: document.getElementById('fecha').value,
        oferente: document.getElementById('oferenteGanador').value,
        marca_ganadora: document.getElementById('marcaGanadora').value,
        precio_ganador: document.getElementById('precioGanador').value,
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

document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('fecha').valueAsDate = new Date();
    await cargarCatalogo();
    await cargarClientes();
    agregarProducto();
});
