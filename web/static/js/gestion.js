let licitaciones = [];
let licitacionActual = null;

async function cargarLicitaciones() {
    const response = await fetch('/api/licitaciones');
    licitaciones = await response.json();
    mostrarLicitaciones(licitaciones);
}

function mostrarLicitaciones(data) {
    const tbody = document.getElementById('licitacionesBody');
    tbody.innerHTML = '';
    
    data.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${l.id}</td>
            <td>${l.numero}</td>
            <td>${l.fecha}</td>
            <td>${l.oferente || '-'}</td>
            <td>
                <button onclick="verDetalle(${l.id})" class="btn-primary">Ver Detalle</button>
                <button onclick="eliminar(${l.id})" class="btn-danger">Eliminar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filtrarLicitaciones() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const filtradas = licitaciones.filter(l => 
        l.numero.toLowerCase().includes(search) || 
        (l.oferente && l.oferente.toLowerCase().includes(search))
    );
    mostrarLicitaciones(filtradas);
}

async function verDetalle(id) {
    licitacionActual = id;
    const response = await fetch(`/api/productos/${id}`);
    const productos = await response.json();
    
    const tbody = document.getElementById('productosBody');
    tbody.innerHTML = '';
    
    productos.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.monodroga}</td>
            <td>${p.marca} - ${p.presentacion}</td>
            <td>${p.cantidad}</td>
            <td>$${p.precio_ofertado.toFixed(2)}</td>
            <td>${p.resultado}</td>
            <td>${p.precio_ganador ? '$' + p.precio_ganador.toFixed(2) : '-'}</td>
            <td>${p.marca_ofrecida || '-'}</td>
            <td>
                <button onclick="editarProducto(${p.id}, ${JSON.stringify(p).replace(/"/g, '&quot;')})" class="btn-primary">Editar</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    document.getElementById('modalDetalle').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalDetalle').style.display = 'none';
}

function editarProducto(id, producto) {
    document.getElementById('editProductoId').value = id;
    document.getElementById('editMonodroga').value = producto.monodroga;
    document.getElementById('editMarca').value = producto.marca;
    document.getElementById('editPresentacion').value = producto.presentacion;
    document.getElementById('editCantidad').value = producto.cantidad;
    document.getElementById('editPrecio').value = producto.precio_ofertado;
    document.getElementById('editResultado').value = producto.resultado;
    document.getElementById('editPrecioGanador').value = producto.precio_ganador || '';
    document.getElementById('editMarcaOfrecida').value = producto.marca_ofrecida || '';
    
    document.getElementById('modalEditar').style.display = 'block';
}

function cerrarModalEditar() {
    document.getElementById('modalEditar').style.display = 'none';
}

document.getElementById('editarForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('editProductoId').value;
    const data = {
        monodroga: document.getElementById('editMonodroga').value,
        marca: document.getElementById('editMarca').value,
        presentacion: document.getElementById('editPresentacion').value,
        cantidad: document.getElementById('editCantidad').value,
        precio_ofertado: document.getElementById('editPrecio').value,
        resultado: document.getElementById('editResultado').value,
        precio_ganador: document.getElementById('editPrecioGanador').value,
        oferente: '',
        marca_ofrecida: document.getElementById('editMarcaOfrecida').value
    };
    
    const response = await fetch(`/api/productos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    if (result.success) {
        alert('Producto actualizado');
        cerrarModalEditar();
        verDetalle(licitacionActual);
    } else {
        alert('Error: ' + result.error);
    }
});

async function eliminar(id) {
    if (!confirm('¿Eliminar esta licitación?')) return;
    
    const response = await fetch(`/api/licitaciones/${id}`, { method: 'DELETE' });
    const result = await response.json();
    
    if (result.success) {
        alert('Licitación eliminada');
        cargarLicitaciones();
    } else {
        alert('Error: ' + result.error);
    }
}

document.addEventListener('DOMContentLoaded', cargarLicitaciones);
