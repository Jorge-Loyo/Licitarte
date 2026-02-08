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
    try {
        const response = await fetch(`/api/presupuestos/${numero}`);
        const result = await response.json();
        
        if (result.success && result.data) {
            // Obtener el ID de licitación desde la tabla presupuestos
            const responsePresupuesto = await fetch(`/api/presupuestos?limit=100&offset=0`);
            const presupuestos = await responsePresupuesto.json();
            const presupuesto = presupuestos.find(p => p.numero === numero);
            
            if (!presupuesto) {
                alert('Error: No se encontró el presupuesto');
                return;
            }
            
            // Obtener datos de la licitación
            const responseLic = await fetch(`/api/licitaciones`);
            const licitaciones = await responseLic.json();
            const licitacion = licitaciones.find(l => l.numero === presupuesto.licitacion);
            
            if (!licitacion) {
                alert('Error: No se encontró la licitación');
                return;
            }
            
            const responseProds = await fetch(`/api/productos/${licitacion.id}`);
            const productos = await responseProds.json();
            
            // Generar HTML del presupuesto
            generarDocumentoPresupuesto(numero, licitacion, productos);
        } else {
            alert('Error al cargar presupuesto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar presupuesto');
    }
}

function generarDocumentoPresupuesto(numeroPresupuesto, licitacion, productos) {
    const total = productos.reduce((sum, p) => sum + (p.cantidad * p.precio_ofertado), 0);
    
    let html = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Presupuesto N° ${numeroPresupuesto}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                @media print { body { margin: 0; } }
            </style>
        </head>
        <body>
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; margin-bottom: 10px;">Presupuesto N° ${numeroPresupuesto}</h1>
            </div>
            
            <div style="margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-left: 4px solid #3498db;">
                <p style="margin: 5px 0;"><strong>Cliente:</strong> ${licitacion.cliente}</p>
                <p style="margin: 5px 0;"><strong>Licitación N°:</strong> ${licitacion.numero}</p>
                <p style="margin: 5px 0;"><strong>Fecha:</strong> ${licitacion.fecha}</p>
            </div>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
                <thead>
                    <tr style="background: #3498db; color: white;">
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Monodroga</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Marca - Presentación</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Laboratorio</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Cantidad</th>
                        <th style="padding: 12px; text-align: right; border: 1px solid #ddd;">Precio Unit.</th>
                        <th style="padding: 12px; text-align: right; border: 1px solid #ddd;">Total</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    productos.forEach((p, index) => {
        const totalProducto = p.cantidad * p.precio_ofertado;
        const bgColor = index % 2 === 0 ? '#ffffff' : '#f8f9fa';
        
        html += `
            <tr style="background: ${bgColor};">
                <td style="padding: 10px; border: 1px solid #ddd;">${p.monodroga}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">${p.marca} - ${p.presentacion}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">${p.marca_ofrecida || '-'}</td>
                <td style="padding: 10px; text-align: center; border: 1px solid #ddd;">${p.cantidad}</td>
                <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">$${p.precio_ofertado.toLocaleString('es-AR', {minimumFractionDigits: 2})}</td>
                <td style="padding: 10px; text-align: right; border: 1px solid #ddd; font-weight: bold;">$${totalProducto.toLocaleString('es-AR', {minimumFractionDigits: 2})}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
                <tfoot>
                    <tr style="background: #2c3e50; color: white; font-weight: bold;">
                        <td colspan="5" style="padding: 15px; text-align: right; border: 1px solid #ddd;">TOTAL OFERTA:</td>
                        <td style="padding: 15px; text-align: right; border: 1px solid #ddd; font-size: 18px;">$${total.toLocaleString('es-AR', {minimumFractionDigits: 2})}</td>
                    </tr>
                </tfoot>
            </table>
            
            <div style="margin-top: 50px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #7f8c8d;">
                <p style="margin: 5px 0;">Documento generado por Licitarte</p>
            </div>
        </body>
        </html>
    `;
    
    // Abrir en nueva ventana
    const ventana = window.open('', '_blank');
    ventana.document.write(html);
    ventana.document.close();
}

document.addEventListener('DOMContentLoaded', () => {
    cargarPresupuestos();
    
    document.getElementById('buscarPresupuesto').addEventListener('input', buscarPresupuestos);
});
