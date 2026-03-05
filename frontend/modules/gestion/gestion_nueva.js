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
        
        const td1 = document.createElement('td');
        td1.textContent = lic.numero;
        tr.appendChild(td1);
        
        const td2 = document.createElement('td');
        td2.textContent = lic.cliente;
        tr.appendChild(td2);
        
        const td3 = document.createElement('td');
        td3.textContent = `${lic.productos_ganados}/${lic.total_productos}`;
        tr.appendChild(td3);
        
        const td4 = document.createElement('td');
        td4.textContent = formatearMoneda(lic.monto_cotizado);
        tr.appendChild(td4);
        
        const td5 = document.createElement('td');
        td5.textContent = formatearMoneda(lic.monto_adjudicado);
        tr.appendChild(td5);
        
        const td6 = document.createElement('td');
        const button = document.createElement('button');
        button.className = 'btn-primary';
        button.textContent = '📄 Resultado';
        button.addEventListener('click', () => {
            window.location.href = `/resultado-licitacion/${lic.id}`;
        });
        td6.appendChild(button);
        tr.appendChild(td6);
        
        tbody.appendChild(tr);
    });
}
