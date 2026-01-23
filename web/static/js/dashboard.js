async function actualizarDashboard() {
    await cargarEstadisticas();
    await cargarProductosAdjudicados();
}

async function cargarEstadisticas() {
    const response = await fetch('/api/estadisticas');
    const stats = await response.json();
    
    document.getElementById('totalLicitaciones').textContent = stats.total_licitaciones;
    document.getElementById('licitacionesGanadas').textContent = stats.licitaciones_ganadas;
    document.getElementById('totalUnidades').textContent = stats.total_unidades.toLocaleString();
    document.getElementById('precioProm').textContent = '$' + stats.precio_promedio_ponderado.toFixed(2);
}

async function cargarProductosAdjudicados() {
    const response = await fetch('/api/productos-adjudicados');
    const productos = await response.json();
    
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';
    
    productos.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.numero_licitacion}</td>
            <td>${p.producto}</td>
            <td>${p.cantidad}</td>
            <td>$${p.precio.toFixed(2)}</td>
            <td>${p.fecha}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function buscarHistorico() {
    const producto = document.getElementById('productoSearch').value;
    if (!producto) return;
    
    const response = await fetch(`/api/historico/${encodeURIComponent(producto)}`);
    const data = await response.json();
    
    const resultDiv = document.getElementById('historicoResult');
    if (data) {
        resultDiv.innerHTML = `
            <strong>Última licitación ganada de "${producto}":</strong><br>
            • N° Licitación: ${data.numero_licitacion}<br>
            • Precio Ganador: $${data.precio.toFixed(2)}<br>
            • Laboratorio: ${data.laboratorio}<br>
            • Fecha: ${data.fecha}
        `;
    } else {
        resultDiv.innerHTML = `No se encontró historial para "${producto}"`;
    }
}

document.addEventListener('DOMContentLoaded', actualizarDashboard);
