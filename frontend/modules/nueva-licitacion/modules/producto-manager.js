// Módulo para gestión de productos
import { catalogoProductos } from './ingreso-data-loader.js';

export let productoCount = 0;

export function capitalizarTexto(texto) {
  if (!texto) return '';
  return texto.toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
}

export async function agregarProducto() {
  const container = document.getElementById('productosContainer');
  const currentCount = productoCount;
  
  const html = await TemplateLoader.loadAndRender('producto-item-template', {
    id: currentCount,
    numero: currentCount + 1
  });
  
  const div = document.createElement('div');
  div.innerHTML = html;
  const productoItem = div.firstElementChild;
  
  productoItem.querySelector('.btn-remove').onclick = () => eliminarProducto(currentCount);
  productoItem.querySelector('.producto-numero-renglon').oninput = function() { validarNumeroRenglon(this); };
  productoItem.querySelector('.producto-monodroga-input').oninput = function() { buscarMonodroga(this); };
  productoItem.querySelector('.producto-laboratorio-input').oninput = function() { buscarLaboratorio(this); };
  productoItem.querySelector('.producto-selector-marca-presentacion').onchange = function() { seleccionarProducto(this); };
  productoItem.querySelector('.producto-cantidad').oninput = function() { calcularTotalRenglon(this); };
  productoItem.querySelector('.producto-costo-unitario').oninput = function() { calcularPrecioOfertado(this); };
  productoItem.querySelector('.producto-margen-deseado').oninput = function() { calcularPrecioOfertado(this); };
  productoItem.querySelector('.btn-agregar-alternativa').onclick = () => window.agregarAlternativa(currentCount);
  productoItem.querySelector('.producto-seleccionado').onchange = () => window.recalcularTotales();
  
  container.appendChild(productoItem);
  productoCount++;
}

export function eliminarProducto(id) {
  document.getElementById(`producto-${id}`).remove();
  window.calcularMontoPoliza();
  window.calcularMargenTotal();
}

export async function buscarMonodroga(input) {
  const texto = input.value.trim();
  const container = input.closest('.producto-item');
  const sugerencias = container.querySelector('.monodroga-sugerencias');

  if (texto.length < 3) {
    sugerencias.style.display = 'none';
    return;
  }

  const params = new URLSearchParams({ q: texto });
  const response = await fetch(`/api/monodrogas/buscar?${params.toString()}`);
  const monodrogas = await response.json();

  if (monodrogas.length === 0) {
    sugerencias.style.display = 'none';
    return;
  }

  sugerencias.innerHTML = monodrogas.map(m =>
    `<div onclick="window.seleccionarMonodroga(this, '${m.nombre.replace(/'/g, "\\'")}')"
          style="padding: 10px; cursor: pointer; border-bottom: 1px solid #333;">
        ${capitalizarTexto(m.nombre)}
     </div>`
  ).join('');

  sugerencias.style.display = 'block';
}

export function seleccionarProducto(select) {
  const option = select.options[select.selectedIndex];
  const container = select.closest('.producto-item');

  const marca = option.dataset.marca || '';
  const presentacion = option.dataset.presentacion || '';
  const laboratorio = option.dataset.laboratorio || '';
  const costoUnitario = option.dataset.costo || 0;

  container.querySelector('.producto-marca').value = marca;
  container.querySelector('.producto-presentacion').value = presentacion;
  container.querySelector('.producto-marca-ofrecida').value = laboratorio;
  container.querySelector('.producto-costo-unitario').value = costoUnitario;
  container.dataset.costoUnitario = costoUnitario;

  calcularPrecioOfertado(container.querySelector('.producto-costo-unitario'));
}

export function calcularPrecioOfertado(input) {
  const container = input.closest('.producto-item');
  const costoUnitario = parseFloat(container.querySelector('.producto-costo-unitario').value) || 0;
  const margenPorcentaje = parseFloat(container.querySelector('.producto-margen-deseado').value) || 0;

  const precioOfertado = costoUnitario * (1 + margenPorcentaje / 100);
  const precioInput = container.querySelector('.producto-precio');
  precioInput.value = precioOfertado > 0 ? precioOfertado.toFixed(2) : '';

  calcularTotalRenglon(container.querySelector('.producto-cantidad'));
}

export function calcularTotalRenglon(input) {
  const container = input.closest('.producto-item');
  const cantidad = parseFloat(container.querySelector('.producto-cantidad').value) || 0;
  const precioOfertado = parseFloat(container.querySelector('.producto-precio').value) || 0;

  const totalRenglon = cantidad * precioOfertado;
  container.querySelector('.producto-total-renglon').value = totalRenglon > 0
    ? '$' + totalRenglon.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '';

  const alternativas = container.querySelectorAll('.alternativa-item');
  alternativas.forEach(alt => {
    const precioAlt = parseFloat(alt.querySelector('.alt-precio').value) || 0;
    const totalAlt = cantidad * precioAlt;
    alt.querySelector('.alt-total-renglon').value = totalAlt > 0
      ? '$' + totalAlt.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : '';
  });

  window.calcularMontoPoliza();
  window.calcularMargenTotal();
}

export function validarNumeroRenglon(input) {
  const numeroRenglon = input.value.trim();
  const container = input.closest('.producto-item');
  const errorMsg = container.querySelector('.renglon-error');

  if (!numeroRenglon) {
    errorMsg.style.display = 'none';
    return;
  }

  const productos = document.querySelectorAll('.producto-item');
  let duplicado = false;

  productos.forEach(item => {
    if (item !== container) {
      const otroNumero = item.querySelector('.producto-numero-renglon').value.trim();
      if (otroNumero === numeroRenglon) {
        duplicado = true;
      }
    }
  });

  if (duplicado) {
    errorMsg.style.display = 'block';
    input.style.borderColor = 'var(--danger-color)';
  } else {
    errorMsg.style.display = 'none';
    input.style.borderColor = '';
  }
}
