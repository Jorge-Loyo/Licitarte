document.addEventListener('DOMContentLoaded', function() {
    cargarRankingPerdidas();
    cargarDiferencias();
});

async function cargarDiferencias() {
    try {
        const response = await fetch('/api/diferencias-promedio');
        const data = await response.json();
        
        document.getElementById('diferenciaPesos').textContent = formatearMoneda(data.diferencia_pesos);
        document.getElementById('diferenciaPorcentaje').textContent = data.diferencia_porcentaje.toFixed(2) + '%';
    } catch (error) {
        console.error('Error cargando diferencias:', error);
    }
}

function formatearMoneda(valor) {
    if (valor >= 1000000) {
        return '$' + (valor / 1000000).toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' MILL';
    }
    return '$' + valor.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

async function cargarRankingPerdidas() {
    try {
        const response = await fetch('/api/ranking-perdidas');
        const data = await response.json();
        
        const tbody = document.getElementById('rankingBody');
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 40px;">No hay datos de pérdidas registradas</td></tr>';
            return;
        }
        
        const total = data.reduce((sum, item) => sum + item.cantidad, 0);
        
        tbody.innerHTML = data.map((item, index) => `
            <tr>
                <td style="text-align: center; font-weight: bold; color: var(--primary-color);">${index + 1}</td>
                <td>${item.motivo}</td>
                <td style="text-align: center; font-weight: bold;">${item.cantidad}</td>
                <td style="text-align: center;">${((item.cantidad / total) * 100).toFixed(1)}%</td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error cargando ranking:', error);
        document.getElementById('rankingBody').innerHTML = 
            '<tr><td colspan="4" style="text-align: center; padding: 40px; color: var(--danger-color);">Error al cargar datos</td></tr>';
    }
}
