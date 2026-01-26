let historicoCompleto = [];
let historicoPagina = 1;
const historicoPorPagina = 5;

let adjudicadosCompleto = [];
let adjudicadosPagina = 1;
const adjudicadosPorPagina = 5;

function formatearMoneda(valor) {
    if (valor >= 1000000) {
        return '$' + (valor / 1000000).toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' MILL';
    }
    return '$' + valor.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

async function actualizarDashboard() {
    await cargarEstadisticas();
    await cargarProductosAdjudicados();
    await cargarHistorico();
}

async function cargarEstadisticas() {
    const response = await fetch('/api/estadisticas');
    const stats = await response.json();
    
    document.getElementById('unidadesCotizadas').textContent = stats.unidades_cotizadas.toLocaleString('es-AR');
    document.getElementById('unidadesGanadas').textContent = stats.unidades_ganadas.toLocaleString('es-AR');
    document.getElementById('porcentajeUnidades').textContent = stats.porcentaje_unidades.toFixed(2) + '%';
    document.getElementById('totalCotizado').textContent = formatearMoneda(stats.total_cotizado);
    document.getElementById('totalGanado').textContent = formatearMoneda(stats.total_ganado);
    document.getElementById('porcentajeDinero').textContent = stats.porcentaje_dinero.toFixed(2) + '%';
}

async function cargarProductosAdjudicados() {
    const response = await fetch('/api/productos-adjudicados');
    adjudicadosCompleto = await response.json();
    adjudicadosPagina = 1;
    mostrarProductosAdjudicados();
}

function mostrarProductosAdjudicados() {
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';
    
    const inicio = (adjudicadosPagina - 1) * adjudicadosPorPagina;
    const fin = inicio + adjudicadosPorPagina;
    const productosPagina = adjudicadosCompleto.slice(inicio, fin);
    
    productosPagina.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.numero_licitacion}</td>
            <td>${p.tipo_licitacion}</td>
            <td>${p.cliente}</td>
            <td>${p.marca} - ${p.presentacion}</td>
            <td>${p.cantidad}</td>
            <td>${formatearMoneda(p.precio)}</td>
            <td>${p.fecha}</td>
        `;
        tbody.appendChild(tr);
    });
    
    const totalPaginas = Math.ceil(adjudicadosCompleto.length / adjudicadosPorPagina);
    document.getElementById('paginaInfoAdj').textContent = `Página ${adjudicadosPagina} de ${totalPaginas || 1}`;
    document.getElementById('btnAnteriorAdj').disabled = adjudicadosPagina === 1;
    document.getElementById('btnSiguienteAdj').disabled = adjudicadosPagina >= totalPaginas;
}

function cambiarPaginaAdjudicados(direccion) {
    adjudicadosPagina += direccion;
    mostrarProductosAdjudicados();
}

async function cargarHistorico(filtro = '') {
    try {
        const response = await fetch('/api/historico', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ monodroga: filtro })
        });
        
        historicoCompleto = await response.json();
        historicoPagina = 1;
        mostrarHistorico();
    } catch (error) {
        console.error('Error:', error);
    }
}

function mostrarHistorico() {
    const tbody = document.getElementById('historicoBody');
    tbody.innerHTML = '';
    
    const inicio = (historicoPagina - 1) * historicoPorPagina;
    const fin = inicio + historicoPorPagina;
    const productosPagina = historicoCompleto.slice(inicio, fin);
    
    productosPagina.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.numero_licitacion}</td>
            <td>${p.tipo_licitacion}</td>
            <td>${p.marca} - ${p.presentacion}</td>
            <td>${p.cantidad}</td>
            <td>${formatearMoneda(p.precio)}</td>
            <td>${p.fecha}</td>
        `;
        tbody.appendChild(tr);
    });
    
    const totalPaginas = Math.ceil(historicoCompleto.length / historicoPorPagina);
    document.getElementById('paginaInfo').textContent = `Página ${historicoPagina} de ${totalPaginas || 1}`;
    document.getElementById('btnAnterior').disabled = historicoPagina === 1;
    document.getElementById('btnSiguiente').disabled = historicoPagina >= totalPaginas;
}

function cambiarPagina(direccion) {
    historicoPagina += direccion;
    mostrarHistorico();
}

async function buscarHistorico() {
    const filtro = document.getElementById('productoSearch').value.trim();
    await cargarHistorico(filtro);
}

function limpiarBusqueda() {
    document.getElementById('productoSearch').value = '';
    cargarHistorico();
}

document.addEventListener('DOMContentLoaded', actualizarDashboard);
