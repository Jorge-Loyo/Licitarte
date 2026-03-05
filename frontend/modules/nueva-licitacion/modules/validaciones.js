// Validaciones del formulario
export function validarFormularioCompleto() {
  const errores = [];

  if (!document.getElementById('numeroLicitacion').value)
    errores.push('Número de licitación requerido');
  if (!document.getElementById('clienteSelect').value)
    errores.push('Cliente requerido');
  if (!document.getElementById('fecha').value)
    errores.push('Fecha requerida');

  const productos = document.querySelectorAll('.producto-item');
  if (productos.length === 0) {
    errores.push('Debe agregar al menos un producto');
    return errores;
  }

  const numerosRenglon = new Set();
  let productosValidos = 0;

  productos.forEach((item, index) => {
    const numeroRenglon = item.querySelector('.producto-numero-renglon').value.trim();
    const monodroga = item.querySelector('.producto-monodroga').value;
    const cantidad = item.querySelector('.producto-cantidad').value;
    const precio = item.querySelector('.producto-precio').value;

    if (monodroga) {
      productosValidos++;

      if (!numeroRenglon) {
        errores.push(`Producto ${index + 1}: falta número de renglón`);
      } else if (numerosRenglon.has(numeroRenglon)) {
        errores.push(`Número de renglón duplicado: ${numeroRenglon}`);
      } else {
        numerosRenglon.add(numeroRenglon);
      }

      if (!cantidad) errores.push(`Producto ${index + 1}: falta cantidad`);
      if (!precio) errores.push(`Producto ${index + 1}: falta precio`);
    }
  });

  if (productosValidos === 0) {
    errores.push('Debe completar al menos un producto');
  }

  return errores;
}

export async function verificarLicitacionExistente() {
  const numero = document.getElementById('numeroLicitacion').value;
  const clienteId = document.getElementById('clienteSelect').value;

  if (!numero || !clienteId) return false;

  const response = await fetch(`/api/licitaciones/verificar?numero=${encodeURIComponent(numero)}&cliente_id=${clienteId}`);
  const result = await response.json();
  return result.existe;
}
