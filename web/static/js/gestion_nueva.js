// Módulo Gestión
let licitaciones = [];

document.addEventListener('DOMContentLoaded', function() {
    cargarLicitaciones();
});

function cargarLicitaciones() {
    fetch('/api/licitaciones-resumen')
        .then(response => response.json())
        .then(data => {
            licitaciones = data;
            mostrarLicitaciones();
        })
        .catch(error => console.error('Error:', error));
}

function formatearMoneda(valor) {
    if (valor >= 1000000) {
        return '$' + (valor / 1000000).toFixed(2) + ' MILL';
    }
    return '$' + valor.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

function mostrarLicitaciones() {
    const tbody = document.getElementById('listaLicitaciones');
    tbody.innerHTML = '';
    
    licitaciones.forEach(lic => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${lic.numero}</td>
            <td>${lic.cliente}</td>
            <td>${lic.productos_ganados}/${lic.total_productos}</td>
            <td>${formatearMoneda(lic.monto_cotizado)}</td>
            <td>${formatearMoneda(lic.monto_adjudicado)}</td>
            <td>
                <button class="btn-primary" onclick="window.location.href='/resultado-licitacion/${lic.id}'">📄 Resultado</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
