// Gestión de alternativas
import { catalogoProductos } from './data-loader.js';

let alternativaCount = 0;

export async function agregarAlternativa(productoId) {
  const producto = document.getElementById(`producto-${productoId}`);
  const container = producto.querySelector('.alternativas-container');
  const monodroga = producto.querySelector('.producto-monodroga').value;
  const selector = producto.querySelector('.producto-seleccionado');

  if (!monodroga) {
    window.mostrarMensaje('Primero seleccione la monodroga del producto principal', 'error');
    return;
  }

  const altId = `alt-${productoId}-${alternativaCount}`;
  const altNumero = alternativaCount + 1;
  alternativaCount++;

  const html = await TemplateLoader.loadAndRender('alternativa-item-template', {
    id: altId,
    productoId: productoId,
    numero: altNumero
  });

  const div = document.createElement('div');
  div.innerHTML = html;
  const altItem = div.firstElementChild;

  altItem.querySelector('.btn-eliminar-alternativa').onclick = () => eliminarAlternativa(altId, productoId);
  altItem.querySelector('.alt-laboratorio-input').oninput = function() { buscarLaboratorioAlternativa(this, monodroga); };
  altItem.querySelector('.alt-selector').onchange = function() { seleccionarAlternativa(this); };
  altItem.querySelector('.alt-costo').oninput = function() { calcularPrecioAlternativa(this); };
  altItem.querySelector('.alt-margen').oninput = function() { calcularPrecioAlternativa(this); };

  container.appendChild(altItem);

  const option = document.createElement('option');
  option.value = altId;
  option.textContent = `Alternativa #${altNumero}`;
  selector.appendChild(option);
}

export function eliminarAlternativa(altId, productoId) {
  const producto = document.getElementById(`producto-${productoId}`);
  const selector = producto.querySelector('.producto-seleccionado');

  document.getElementById(altId).remove();

  const option = selector.querySelector(`option[value="${altId}"]`);
  if (option) option.remove();

  if (selector.value === altId) {
    selector.value = 'principal';
  }

  window.recalcularTotales();
}

async function buscarLaboratorioAlternativa(input, monodroga) {
  const texto = input.value.trim();
  const container = input.closest('.alternativa-item');
  const sugerencias = container.querySelector('.alt-laboratorio-sugerencias');
  const selectorMarca = container.querySelector('.alt-selector');

  if (texto.length === 0) {
    sugerencias.style.display = 'none';
    selectorMarca.innerHTML = '<option value="">Primero seleccione laboratorio...</option>';
    selectorMarca.disabled = true;
    return;
  }

  const params = new URLSearchParams({ monodroga: monodroga, q: texto });
  const response = await fetch(`/api/laboratorios/buscar?${params.toString()}`);
  const laboratorios = await response.json();

  if (laboratorios.length === 0) {
    sugerencias.style.display = 'none';
    return;
  }

  sugerencias.innerHTML = laboratorios.map(lab =>
    `<div onclick="window.seleccionarLaboratorioAlternativa(this, '${lab.nombre.replace(/'/g, "\\'")}')"
          style="padding: 10px; cursor: pointer; border-bottom: 1px solid #333;">
        ${lab.nombre}
     </div>`
  ).join('');

  sugerencias.style.display = 'block';
}

function seleccionarAlternativa(select) {
  const option = select.options[select.selectedIndex];
  const container = select.closest('.alternativa-item');

  container.querySelector('.alt-marca').value = option.dataset.marca || '';
  container.querySelector('.alt-presentacion').value = option.dataset.presentacion || '';
  container.querySelector('.alt-costo').value = option.dataset.costo || '';

  calcularPrecioAlternativa(container.querySelector('.alt-costo'));
}

function calcularPrecioAlternativa(input) {
  const container = input.closest('.alternativa-item');
  const costo = parseFloat(container.querySelector('.alt-costo').value) || 0;
  const margen = parseFloat(container.querySelector('.alt-margen').value) || 0;

  const precio = costo * (1 + margen / 100);
  container.querySelector('.alt-precio').value = precio > 0 ? precio.toFixed(2) : '';

  const productoItem = container.closest('.producto-item');
  const cantidad = parseFloat(productoItem.querySelector('.producto-cantidad').value) || 0;
  const totalRenglon = cantidad * precio;
  container.querySelector('.alt-total-renglon').value = totalRenglon > 0
    ? '$' + totalRenglon.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '';

  window.recalcularTotales();
}

window.seleccionarLaboratorioAlternativa = function(element, laboratorio) {
  const container = element.closest('.alternativa-item');
  const input = container.querySelector('.alt-laboratorio-input');
  const sugerencias = container.querySelector('.alt-laboratorio-sugerencias');
  const hiddenLaboratorio = container.querySelector('.alt-laboratorio');
  const selectorMarca = container.querySelector('.alt-selector');
  const producto = container.closest('.producto-item');
  const monodroga = producto.querySelector('.producto-monodroga').value;

  input.value = laboratorio;
  hiddenLaboratorio.value = laboratorio;
  sugerencias.style.display = 'none';

  const productosFiltrados = catalogoProductos.filter(p =>
    p.monodroga && p.monodroga.toLowerCase() === monodroga.toLowerCase() &&
    p.laboratorio && p.laboratorio.toLowerCase() === laboratorio.toLowerCase()
  );

  selectorMarca.innerHTML = '<option value="">Seleccione marca - presentación...</option>';
  productosFiltrados.forEach(p => {
    selectorMarca.innerHTML += `<option value="${p.numero_registro}" data-marca="${p.marca}" data-presentacion="${p.presentacion}" data-costo="${p.costo_unitario || 0}">
      ${p.marca} - ${p.presentacion}
    </option>`;
  });
  selectorMarca.disabled = false;
};
