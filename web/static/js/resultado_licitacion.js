let licitacionId = null;
let productos = [];
let productosOriginales = []; // Guardar datos originales
let alternativasPorProducto = {};
let productoSeleccionado = null;
let oferentes = [];
let laboratorios = [];
let ofertasTemp = []; // Ofertas temporales antes de guardar
let contadorOfertas = 0;
let productoNoAdjudicado = null; // Para modal de ganador

document.addEventListener('DOMContentLoaded', function() {
    licitacionId = parseInt(window.location.pathname.split('/').pop());
    cargarDatos();
});

function cargarDatos() {
    Promise.all([
        fetch(`/api/licitaciones/${licitacionId}`).then(r => r.json()),
        fetch(`/api/productos/${licitacionId}`).then(r => r.json()),
        fetch('/api/oferentes').then(r => r.json())
    ]).then(([licitacion, prods, ofes]) => {
        mostrarInfoLicitacion(licitacion);
        productos = prods;
        productosOriginales = JSON.parse(JSON.stringify(prods)); // Copia profunda
        oferentes = ofes;
        cargarAlternativas();
    }).catch(error => console.error('Error:', error));
}

function mostrarInfoLicitacion(lic) {
    document.getElementById('infoLicitacion').innerHTML = 
        `<strong>Licitación:</strong> ${lic.numero} | <strong>Cliente:</strong> ${lic.cliente || '-'}`;
}

function cargarAlternativas() {
    // Primero cargar el catálogo una sola vez
    fetch('/api/catalogo')
        .then(r => r.json())
        .then(catalogo => {
            // Extraer laboratorios únicos
            laboratorios = [...new Set(catalogo.map(c => c.laboratorio).filter(l => l))];
            
            const promesas = productos.map(p => {
                // Buscar laboratorio en catálogo (búsqueda flexible)
                const prodCatalogo = catalogo.find(c => 
                    c.monodroga?.toLowerCase().trim() === p.monodroga?.toLowerCase().trim() && 
                    c.marca?.toLowerCase().trim() === p.marca?.toLowerCase().trim() && 
                    c.presentacion?.toLowerCase().trim() === p.presentacion?.toLowerCase().trim()
                );
                p.laboratorio = prodCatalogo?.laboratorio || 'Celtyc';
                
                // Cargar alternativas
                return fetch(`/api/alternativas/${p.id}`)
                    .then(r => r.json())
                    .then(alts => { 
                        alternativasPorProducto[p.id] = alts;
                        // Agregar laboratorio a cada alternativa
                        alts.forEach(alt => {
                            if (!alt.laboratorio) {
                                const altCatalogo = catalogo.find(c => 
                                    c.monodroga?.toLowerCase().trim() === p.monodroga?.toLowerCase().trim() && 
                                    c.marca?.toLowerCase().trim() === alt.marca?.toLowerCase().trim() && 
                                    c.presentacion?.toLowerCase().trim() === alt.presentacion?.toLowerCase().trim()
                                );
                                alt.laboratorio = altCatalogo?.laboratorio || 'Celtyc';
                            }
                        });
                    });
            });
            
            Promise.all(promesas).then(() => mostrarProductos());
        })
        .catch(error => {
            console.error('Error cargando catálogo:', error);
            mostrarProductos();
        });
}

function formatearMoneda(valor) {
    if (valor >= 1000000) {
        return '$' + (valor / 1000000).toFixed(2) + ' MILL';
    }
    return '$' + valor.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

function mostrarProductos() {
    const tbody = document.getElementById('listaProductos');
    tbody.innerHTML = '';
    
    productos.forEach(prod => {
        const tieneAlternativas = alternativasPorProducto[prod.id]?.length > 0;
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${prod.monodroga}</td>
            <td>
                ${tieneAlternativas ? `<button class="btn-alt" onclick="abrirModalAlternativas(${prod.id})">🔄</button>` : ''}
            </td>
            <td>${prod.marca} - ${prod.presentacion}</td>
            <td>${prod.laboratorio || '-'}</td>
            <td>${prod.cantidad}</td>
            <td>${formatearMoneda(prod.precio_ofertado)}</td>
            <td>
                <select class="resultado-select" data-producto-id="${prod.id}" onchange="cambioResultado(${prod.id}, this.value)">
                    <option value="Parcial" ${prod.resultado === 'Parcial' ? 'selected' : ''}>Parcial</option>
                    <option value="Adjudicado" ${prod.resultado === 'Adjudicado' ? 'selected' : ''}>Adjudicado</option>
                    <option value="No Adjudicado" ${prod.resultado === 'No Adjudicado' ? 'selected' : ''}>No Adjudicado</option>
                </select>
            </td>
            <td>
                <button class="btn-oferentes" onclick="abrirModalOfertas(${prod.id})">💰 Oferentes</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function cambioResultado(productoId, nuevoResultado) {
    if (nuevoResultado === 'No Adjudicado') {
        productoNoAdjudicado = productos.find(p => p.id === productoId);
        abrirModalGanador();
    }
}

function abrirModalGanador() {
    document.getElementById('infoProductoGanador').innerHTML = 
        `<strong>Producto:</strong> ${productoNoAdjudicado.monodroga} - ${productoNoAdjudicado.marca} ${productoNoAdjudicado.presentacion}`;
    
    // Cargar ofertas del producto
    fetch(`/api/ofertas/${productoNoAdjudicado.id}`)
        .then(r => r.json())
        .then(ofertas => {
            const select = document.getElementById('selectGanador');
            select.innerHTML = '<option value="">Seleccionar oferente...</option>';
            
            if (ofertas.length === 0) {
                select.innerHTML += '<option value="" disabled>No hay ofertas cargadas</option>';
            } else {
                ofertas.forEach(oferta => {
                    select.innerHTML += `<option value="${oferta.oferente}|${oferta.precio}">${oferta.oferente} - ${formatearMoneda(oferta.precio)}</option>`;
                });
            }
        })
        .catch(error => console.error('Error:', error));
    
    document.getElementById('modalSeleccionarGanador').style.display = 'block';
}

function cerrarModalGanador() {
    // Revertir select a valor anterior
    const select = document.querySelector(`[data-producto-id="${productoNoAdjudicado.id}"]`);
    select.value = productoNoAdjudicado.resultado;
    productoNoAdjudicado = null;
    document.getElementById('modalSeleccionarGanador').style.display = 'none';
}

function confirmarGanador() {
    const selectGanador = document.getElementById('selectGanador');
    const valor = selectGanador.value;
    
    if (!valor) {
        alert('Debe seleccionar un oferente ganador');
        return;
    }
    
    const [oferente, precio] = valor.split('|');
    
    // Actualizar producto
    productoNoAdjudicado.resultado = 'No Adjudicado';
    productoNoAdjudicado.oferente_ganador = oferente;
    productoNoAdjudicado.precio_ganador = parseFloat(precio);
    
    document.getElementById('modalSeleccionarGanador').style.display = 'none';
    productoNoAdjudicado = null;
}

function abrirModalAlternativas(productoId) {
    productoSeleccionado = productos.find(p => p.id === productoId);
    const productoOriginal = productosOriginales.find(p => p.id === productoId);
    const alternativas = alternativasPorProducto[productoId];
    
    document.getElementById('productoActual').innerHTML = 
        `<strong>Producto actual:</strong> ${productoSeleccionado.marca} - ${productoSeleccionado.presentacion} (${formatearMoneda(productoSeleccionado.precio_ofertado)})`;
    
    const listaDiv = document.getElementById('listaAlternativas');
    
    // Determinar cuál opción está seleccionada actualmente
    const esPrincipal = !productoSeleccionado.producto_cotizar || productoSeleccionado.producto_cotizar === 'principal';
    
    listaDiv.innerHTML = `
        <div style="margin-bottom: 10px;">
            <button class="${esPrincipal ? 'btn-primary' : 'btn-secondary'}" onclick="seleccionarAlternativa('principal')" style="width: 100%; text-align: left; padding: 15px;">
                ${esPrincipal ? '✅' : ''} Principal: ${productoOriginal.marca} - ${productoOriginal.presentacion}<br>
                <small style="color: #333;">Precio: ${formatearMoneda(productoOriginal.precio_ofertado)}</small>
            </button>
        </div>
    `;
    
    alternativas.forEach((alt, idx) => {
        const altKey = `alt-${productoId}-${idx}`;
        const esSeleccionada = productoSeleccionado.producto_cotizar === altKey;
        const obs = alt.observaciones ? `<br><small style="color: #333;">Obs: ${alt.observaciones}</small>` : '';
        
        listaDiv.innerHTML += `
            <div style="margin-bottom: 10px;">
                <button class="${esSeleccionada ? 'btn-primary' : 'btn-secondary'}" onclick="seleccionarAlternativa(${idx})" style="width: 100%; text-align: left; padding: 15px;">
                    ${esSeleccionada ? '✅' : ''} Alternativa ${idx + 1}: ${alt.marca} - ${alt.presentacion}<br>
                    <small style="color: #333;">Precio: ${formatearMoneda(alt.precio_ofertado)}</small>${obs}
                </button>
            </div>
        `;
    });
    
    document.getElementById('modalAlternativas').style.display = 'block';
}

function seleccionarAlternativa(opcion) {
    const productoOriginal = productosOriginales.find(p => p.id === productoSeleccionado.id);
    
    if (opcion === 'principal') {
        productoSeleccionado.producto_cotizar = 'principal';
        productoSeleccionado.marca = productoOriginal.marca;
        productoSeleccionado.presentacion = productoOriginal.presentacion;
        productoSeleccionado.precio_ofertado = productoOriginal.precio_ofertado;
        productoSeleccionado.laboratorio = productoOriginal.laboratorio;
    } else {
        const alt = alternativasPorProducto[productoSeleccionado.id][opcion];
        productoSeleccionado.producto_cotizar = `alt-${productoSeleccionado.id}-${opcion}`;
        productoSeleccionado.marca = alt.marca;
        productoSeleccionado.presentacion = alt.presentacion;
        productoSeleccionado.precio_ofertado = alt.precio_ofertado;
        productoSeleccionado.laboratorio = alt.laboratorio || '-';
    }
    
    cerrarModalAlternativas();
    mostrarProductos();
}

function cerrarModalAlternativas() {
    document.getElementById('modalAlternativas').style.display = 'none';
}

function abrirModalOfertas(productoId) {
    productoSeleccionado = productos.find(p => p.id === productoId);
    ofertasTemp = [];
    contadorOfertas = 0;
    
    document.getElementById('infoProductoOferta').innerHTML = 
        `<strong>Producto:</strong> ${productoSeleccionado.monodroga} - ${productoSeleccionado.marca} ${productoSeleccionado.presentacion}`;
    
    document.getElementById('listaOfertas').innerHTML = '';
    
    // Cargar ofertas existentes
    fetch(`/api/ofertas/${productoId}`)
        .then(r => r.json())
        .then(ofertas => {
            ofertas.forEach(oferta => {
                agregarOferta(oferta);
            });
        })
        .catch(error => console.error('Error cargando ofertas:', error));
    
    document.getElementById('modalOfertas').style.display = 'block';
}

function agregarOferta(ofertaExistente = null) {
    const id = contadorOfertas++;
    const div = document.createElement('div');
    div.id = `oferta-${id}`;
    div.style.cssText = 'background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); border: 2px solid #4dd0e1; padding: 20px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: all 0.3s;';
    
    const opcionesOferentes = oferentes.map(o => `<option value="${o.nombre}">${o.nombre}</option>`).join('');
    
    div.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #4dd0e1;">
            <strong style="color: #333; font-size: 16px;">💼 Oferta ${id + 1}</strong>
            <button class="btn-danger" onclick="eliminarOferta(${id})" style="padding: 6px 12px; border-radius: 5px;">✕ Eliminar</button>
        </div>
        <div style="display: grid; gap: 15px;">
            <div>
                <label style="display: block; margin-bottom: 5px; color: #333; font-weight: 600;">👥 Oferente:</label>
                <div style="display: flex; gap: 5px;">
                    <select id="oferente-${id}" style="flex: 1; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px;" required>
                        <option value="">Seleccionar oferente...</option>
                        ${opcionesOferentes}
                    </select>
                    <button class="btn-primary" onclick="abrirModalNuevoOferente(${id})" style="padding: 10px 15px; border-radius: 5px;">➕</button>
                </div>
            </div>
            <div>
                <label style="display: block; margin-bottom: 5px; color: #333; font-weight: 600;">🏭 Laboratorio:</label>
                <input type="text" id="laboratorio-${id}" placeholder="Escriba 3+ letras para buscar..." list="laboratorios-${id}" required style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px;">
                <datalist id="laboratorios-${id}"></datalist>
            </div>
            <div>
                <label style="display: block; margin-bottom: 5px; color: #333; font-weight: 600;">💵 Precio:</label>
                <input type="number" id="precio-${id}" placeholder="0.00" step="0.01" required style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px;">
            </div>
        </div>
    `;
    
    document.getElementById('listaOfertas').appendChild(div);
    
    // Si hay datos existentes, rellenar
    if (ofertaExistente) {
        document.getElementById(`oferente-${id}`).value = ofertaExistente.oferente;
        document.getElementById(`laboratorio-${id}`).value = ofertaExistente.laboratorio;
        document.getElementById(`precio-${id}`).value = ofertaExistente.precio;
    }
    
    // Agregar filtrado de laboratorios
    const inputLab = document.getElementById(`laboratorio-${id}`);
    inputLab.addEventListener('input', function() {
        const valor = this.value;
        const datalist = document.getElementById(`laboratorios-${id}`);
        
        if (valor.length >= 3) {
            const filtrados = laboratorios.filter(l => 
                l.toLowerCase().includes(valor.toLowerCase())
            );
            datalist.innerHTML = filtrados.map(l => `<option value="${l}">`).join('');
        } else {
            datalist.innerHTML = '';
        }
    });
    
    // Efecto hover
    div.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
        this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    });
    div.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
    });
}

function eliminarOferta(id) {
    document.getElementById(`oferta-${id}`)?.remove();
}

function cerrarModalOfertas() {
    document.getElementById('modalOfertas').style.display = 'none';
}

function guardarOfertas() {
    const ofertas = [];
    document.querySelectorAll('[id^="oferta-"]').forEach(div => {
        const id = div.id.split('-')[1];
        const oferente = document.getElementById(`oferente-${id}`)?.value;
        const laboratorio = document.getElementById(`laboratorio-${id}`)?.value;
        const precio = document.getElementById(`precio-${id}`)?.value;
        
        if (oferente && laboratorio && precio) {
            ofertas.push({ oferente, laboratorio, precio: parseFloat(precio) });
        }
    });
    
    fetch(`/api/ofertas/${productoSeleccionado.id}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ ofertas })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(`${ofertas.length} oferta(s) guardada(s) correctamente`);
            cerrarModalOfertas();
        } else {
            alert('Error al guardar ofertas: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al guardar ofertas');
    });
}

function abrirModalNuevoOferente(ofertaId) {
    document.getElementById('formNuevoOferente').dataset.ofertaId = ofertaId;
    document.getElementById('nuevoOferenteNombre').value = '';
    document.getElementById('modalNuevoOferente').style.display = 'block';
}

function cerrarModalNuevoOferente() {
    document.getElementById('modalNuevoOferente').style.display = 'none';
}

// Manejar envío del formulario de nuevo oferente
document.addEventListener('DOMContentLoaded', function() {
    const formOferente = document.getElementById('formNuevoOferente');
    if (formOferente) {
        formOferente.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nombre = document.getElementById('nuevoOferenteNombre').value;
            const ofertaId = this.dataset.ofertaId;
            
            fetch('/api/oferentes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ nombre })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    oferentes.push({ id: data.id, nombre });
                    
                    // Actualizar select
                    const select = document.getElementById(`oferente-${ofertaId}`);
                    const option = document.createElement('option');
                    option.value = nombre;
                    option.text = nombre;
                    option.selected = true;
                    select.appendChild(option);
                    
                    cerrarModalNuevoOferente();
                } else {
                    alert('Error al crear oferente: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al crear oferente');
            });
        });
    }
});

function guardarResultados() {
    const selects = document.querySelectorAll('.resultado-select');
    const actualizaciones = [];
    
    selects.forEach(select => {
        const productoId = parseInt(select.dataset.productoId);
        const producto = productos.find(p => p.id === productoId);
        
        actualizaciones.push(
            fetch(`/api/productos/${productoId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    monodroga: producto.monodroga,
                    marca: producto.marca,
                    presentacion: producto.presentacion,
                    cantidad: producto.cantidad,
                    precio_ofertado: producto.precio_ofertado,
                    resultado: select.value,
                    precio_ganador: producto.precio_ganador || null,
                    oferente: producto.oferente_ganador || '',
                    marca_ofrecida: producto.marca_ofrecida || '',
                    marca_ganadora: producto.marca_ganadora || '',
                    motivo_perdida: producto.motivo_perdida || '',
                    numero_renglon: producto.numero_renglon || '',
                    costo_unitario: producto.costo_unitario || null,
                    margen_porcentaje: producto.margen_porcentaje || null,
                    observaciones: producto.observaciones || '',
                    producto_cotizar: producto.producto_cotizar || 'principal'
                })
            })
        );
    });
    
    Promise.all(actualizaciones)
        .then(() => {
            alert('Resultados guardados correctamente');
            window.location.href = '/gestion-nueva';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al guardar los resultados');
        });
}
