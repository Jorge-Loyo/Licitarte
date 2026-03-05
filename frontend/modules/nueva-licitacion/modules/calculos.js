// Cálculos y totales
export function calcularMontoPoliza() {
  const productos = document.querySelectorAll('.producto-item');
  let montoTotal = 0;

  productos.forEach(item => {
    const cantidad = parseFloat(item.querySelector('.producto-cantidad').value) || 0;
    const precioPrincipal = parseFloat(item.querySelector('.producto-precio').value) || 0;

    let totalMaximo = cantidad * precioPrincipal;

    const alternativas = item.querySelectorAll('.alternativa-item');
    alternativas.forEach(alt => {
      const precioAlt = parseFloat(alt.querySelector('.alt-precio').value) || 0;
      const totalAlt = cantidad * precioAlt;
      if (totalAlt > totalMaximo) {
        totalMaximo = totalAlt;
      }
    });

    montoTotal += totalMaximo;
  });

  document.getElementById('montoTotalDisplay').value = '$' + montoTotal.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });

  const porcentaje = parseFloat(document.getElementById('porcentajePoliza').value) || 0;
  const montoPoliza = (montoTotal * porcentaje) / 100;

  document.getElementById('montoPolizaDisplay').value = '$' + montoPoliza.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
  document.getElementById('montoPoliza').value = montoPoliza;
}

export function calcularMargenTotal() {
  const tipo = document.getElementById('tipoAdjudicacion').value;
  if (tipo !== 'Total') return;

  const productos = document.querySelectorAll('.producto-item');
  let costoTotal = 0;
  let precioTotal = 0;

  productos.forEach(item => {
    const cantidad = parseFloat(item.querySelector('.producto-cantidad').value) || 0;
    const selector = item.querySelector('.producto-seleccionado');
    const seleccionado = selector.value;

    let costoUnitario = 0;
    let precioOfertado = 0;

    if (seleccionado === 'principal') {
      costoUnitario = parseFloat(item.querySelector('.producto-costo-unitario').value) || 0;
      precioOfertado = parseFloat(item.querySelector('.producto-precio').value) || 0;
    } else {
      const alt = document.getElementById(seleccionado);
      if (alt) {
        costoUnitario = parseFloat(alt.querySelector('.alt-costo').value) || 0;
        precioOfertado = parseFloat(alt.querySelector('.alt-precio').value) || 0;
      }
    }

    costoTotal += cantidad * costoUnitario;
    precioTotal += cantidad * precioOfertado;
  });

  const margenTotal = precioTotal - costoTotal;
  const margenPorcentaje = costoTotal > 0 ? (margenTotal / costoTotal) * 100 : 0;

  document.getElementById('costoTotalDisplay').value = '$' + costoTotal.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
  document.getElementById('precioTotalDisplay').value = '$' + precioTotal.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
  document.getElementById('margenTotalDisplay').value = '$' + margenTotal.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
  document.getElementById('margenTotalPorcentajeDisplay').value = margenPorcentaje.toFixed(2) + '%';
}

export function recalcularTotales() {
  calcularMontoPoliza();
  calcularMargenTotal();
}
