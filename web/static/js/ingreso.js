let productoCount = 0;

function agregarProducto() {
    const container = document.getElementById('productosContainer');
    const div = document.createElement('div');
    div.className = 'producto-item';
    div.id = `producto-${productoCount}`;
    
    div.innerHTML = `
        <button type="button" class="btn-remove" onclick="eliminarProducto(${productoCount})">✕</button>
        <div class="form-group">
            <label>Ítem/Producto *</label>
            <input type="text" class="producto-item-input" required>
        </div>
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
                <label>Lab. Ganador</label>
                <input type="text" class="producto-laboratorio">
            </div>
        </div>
    `;
    
    container.appendChild(div);
    productoCount++;
}

function eliminarProducto(id) {
    document.getElementById(`producto-${id}`).remove();
}

document.getElementById('licitacionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const productos = [];
    document.querySelectorAll('.producto-item').forEach(item => {
        productos.push({
            item: item.querySelector('.producto-item-input').value,
            cantidad: item.querySelector('.producto-cantidad').value,
            precio: item.querySelector('.producto-precio').value,
            resultado: item.querySelector('.producto-resultado').value,
            laboratorio: item.querySelector('.producto-laboratorio').value
        });
    });
    
    if (productos.length === 0) {
        mostrarMensaje('Agregue al menos un producto', 'error');
        return;
    }
    
    const data = {
        numero: document.getElementById('numeroLicitacion').value,
        fecha: document.getElementById('fecha').value,
        laboratorio: document.getElementById('laboratorioGanador').value,
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

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('fecha').valueAsDate = new Date();
    agregarProducto();
});
