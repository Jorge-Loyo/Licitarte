let presupuestos = [];
let presupuestosFiltrados = [];
let paginaActual = 1;
const itemsPorPagina = 20;

async function cargarPresupuestos() {
    try {
        const response = await fetch(`/api/presupuestos?limit=100&offset=0`);
        presupuestos = await response.json();
        presupuestosFiltrados = presupuestos;
        renderizarTabla();
    } catch (error) {
        console.error('Error cargando presupuestos:', error);
        document.getElementById('presupuestosBody').innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px; color: var(--danger-color);">
                    Error al cargar presupuestos
                </td>
            </tr>
        `;
    }
}

function renderizarTabla() {
    const tbody = document.getElementById('presupuestosBody');
    
    if (presupuestosFiltrados.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px; color: #999;">
                    No hay presupuestos generados
                </td>
            </tr>
        `;
        return;
    }
    
    const inicio = (paginaActual - 1) * itemsPorPagina;
    const fin = inicio + itemsPorPagina;
    const paginaItems = presupuestosFiltrados.slice(inicio, fin);
    
    tbody.innerHTML = paginaItems.map((p, index) => {
        const bgColor = index % 2 === 0 ? 'var(--bg-dark)' : '#1a1a1a';
        const fecha = new Date(p.fecha).toLocaleString('es-AR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        return `
            <tr style="background: ${bgColor};">
                <td style="padding: 15px; text-align: center; font-weight: bold; color: var(--primary);">${p.numero}</td>
                <td style="padding: 15px;">${p.licitacion || '-'}</td>
                <td style="padding: 15px;">${p.cliente || '-'}</td>
                <td style="padding: 15px; text-align: center;">${fecha}</td>
                <td style="padding: 15px; text-align: center;">
                    <button onclick="verPresupuesto(${p.numero})" class="btn-primary" style="padding: 8px 15px; font-size: 14px;">
                        👁️ Ver
                    </button>
                </td>
            </tr>
        `;
    }).join('');
    
    actualizarPaginacion();
}

function actualizarPaginacion() {
    const totalPaginas = Math.ceil(presupuestosFiltrados.length / itemsPorPagina);
    document.getElementById('infoPagina').textContent = `Página ${paginaActual} de ${totalPaginas}`;
    document.getElementById('btnAnterior').disabled = paginaActual === 1;
    document.getElementById('btnSiguiente').disabled = paginaActual >= totalPaginas;
}

function cargarPagina(pagina) {
    const totalPaginas = Math.ceil(presupuestosFiltrados.length / itemsPorPagina);
    if (pagina < 1 || pagina > totalPaginas) return;
    paginaActual = pagina;
    renderizarTabla();
}

function buscarPresupuestos() {
    const termino = document.getElementById('buscarPresupuesto').value.toLowerCase();
    
    if (!termino) {
        presupuestosFiltrados = presupuestos;
    } else {
        presupuestosFiltrados = presupuestos.filter(p => 
            p.numero.toString().includes(termino) ||
            (p.licitacion && p.licitacion.toLowerCase().includes(termino)) ||
            (p.cliente && p.cliente.toLowerCase().includes(termino))
        );
    }
    
    paginaActual = 1;
    renderizarTabla();
}

async function verPresupuesto(numero) {
    window.open(`/presupuesto/${numero}`, '_blank');
}

document.addEventListener('DOMContentLoaded', () => {
    cargarPresupuestos();
    
    document.getElementById('buscarPresupuesto').addEventListener('input', buscarPresupuestos);
});
