let licitacionId = null;
let productos = [];
let productosOriginales = [];
let alternativasPorProducto = {};
let productoSeleccionado = null;
let oferentes = [];
let laboratorios = [];
let ofertasTemp = [];
let contadorOfertas = 0;
let productoNoAdjudicado = null;

document.addEventListener("DOMContentLoaded", function () {
  const pathId = window.location.pathname.split("/").pop();
  licitacionId = parseInt(pathId, 10);
  if (!Number.isInteger(licitacionId) || licitacionId <= 0) {
    console.error("Invalid licitación ID");
    return;
  }
  cargarDatos();
});

function cargarDatos() {
  Promise.all([
    fetch(`/api/licitaciones/${licitacionId}`).then((r) => r.json()),
    fetch(`/api/productos/${licitacionId}`).then((r) => r.json()),
    fetch("/api/oferentes").then((r) => r.json()),
  ])
    .then(([licitacion, prods, ofes]) => {
      mostrarInfoLicitacion(licitacion);
      productos = prods;
      productosOriginales = JSON.parse(JSON.stringify(prods));
      oferentes = ofes;
      cargarAlternativas();
    })
    .catch((error) => console.error("Error:", error));
}

function mostrarInfoLicitacion(lic) {
  const infoDiv = document.getElementById("infoLicitacion");
  infoDiv.textContent = "";
  const strong1 = document.createElement("strong");
  strong1.textContent = "Licitación:";
  const strong2 = document.createElement("strong");
  strong2.textContent = " Cliente:";
  infoDiv.appendChild(strong1);
  infoDiv.appendChild(document.createTextNode(` ${lic.numero} | `));
  infoDiv.appendChild(strong2);
  infoDiv.appendChild(document.createTextNode(` ${lic.cliente || "-"}`));
}

function cargarAlternativas() {
  fetch("/api/catalogo")
    .then((r) => r.json())
    .then((catalogo) => {
      laboratorios = [
        ...new Set(catalogo.map((c) => c.laboratorio).filter((l) => l)),
      ];

      const promesas = productos.map((p) => {
        const prodCatalogo = catalogo.find(
          (c) =>
            c.monodroga?.toLowerCase().trim() ===
              p.monodroga?.toLowerCase().trim() &&
            c.marca?.toLowerCase().trim() === p.marca?.toLowerCase().trim() &&
            c.presentacion?.toLowerCase().trim() ===
              p.presentacion?.toLowerCase().trim(),
        );
        p.laboratorio = prodCatalogo?.laboratorio || "Celtyc";

        return fetch(`/api/alternativas/${p.id}`)
          .then((r) => r.json())
          .then((alts) => {
            if (p.id && typeof p.id === "number") {
              Object.defineProperty(alternativasPorProducto, String(p.id), {
                value: alts,
                writable: true,
                enumerable: true,
                configurable: true
              });
            }
            alts.forEach((alt) => {
              if (!alt.laboratorio) {
                const altCatalogo = catalogo.find(
                  (c) =>
                    c.monodroga?.toLowerCase().trim() ===
                      p.monodroga?.toLowerCase().trim() &&
                    c.marca?.toLowerCase().trim() ===
                      alt.marca?.toLowerCase().trim() &&
                    c.presentacion?.toLowerCase().trim() ===
                      alt.presentacion?.toLowerCase().trim(),
                );
                alt.laboratorio = altCatalogo?.laboratorio || "Celtyc";
              }
            });
          });
      });

      Promise.all(promesas).then(() => mostrarProductos());
    })
    .catch((error) => {
      console.error("Error cargando catálogo:", error);
      mostrarProductos();
    });
}

function formatearMoneda(valor) {
  if (valor >= 1000000) {
    return "$" + (valor / 1000000).toFixed(2) + " MILL";
  }
  return (
    "$" +
    valor.toLocaleString("es-AR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  );
}

function mostrarProductos() {
  const tbody = document.getElementById("listaProductos");
  tbody.textContent = "";

  productos.forEach((prod) => {
    const tieneAlternativas = alternativasPorProducto[prod.id]?.length > 0;
    const tr = document.createElement("tr");

    const td1 = document.createElement("td");
    td1.textContent = prod.monodroga;
    tr.appendChild(td1);

    const td2 = document.createElement("td");
    if (tieneAlternativas) {
      const btn = document.createElement("button");
      btn.className = "btn-alt";
      btn.textContent = "🔄";
      btn.onclick = () => abrirModalAlternativas(prod.id);
      td2.appendChild(btn);
    }
    tr.appendChild(td2);

    const td3 = document.createElement("td");
    td3.textContent = `${prod.marca} - ${prod.presentacion}`;
    tr.appendChild(td3);

    const td4 = document.createElement("td");
    td4.textContent = prod.laboratorio || "-";
    tr.appendChild(td4);

    const td5 = document.createElement("td");
    td5.textContent = prod.cantidad;
    tr.appendChild(td5);

    const td6 = document.createElement("td");
    td6.textContent = formatearMoneda(prod.precio_ofertado);
    tr.appendChild(td6);

    const td7 = document.createElement("td");
    const select = document.createElement("select");
    select.className = "resultado-select";
    select.dataset.productoId = prod.id;
    select.onchange = (e) => cambioResultado(prod.id, e.target.value);
    ["Parcial", "Adjudicado", "No Adjudicado"].forEach((opt) => {
      const option = document.createElement("option");
      option.value = opt;
      option.textContent = opt;
      option.selected = prod.resultado === opt;
      select.appendChild(option);
    });
    td7.appendChild(select);
    tr.appendChild(td7);

    const td8 = document.createElement("td");
    const btnOfertas = document.createElement("button");
    btnOfertas.className = "btn-oferentes";
    btnOfertas.textContent = "💰 Oferentes";
    btnOfertas.onclick = () => abrirModalOfertas(prod.id);
    td8.appendChild(btnOfertas);
    tr.appendChild(td8);

    tbody.appendChild(tr);
  });
}

function cambioResultado(productoId, nuevoResultado) {
  if (nuevoResultado === "No Adjudicado") {
    productoNoAdjudicado = productos.find((p) => p.id === productoId);
    abrirModalGanador();
  }
}

function abrirModalGanador() {
  const infoDiv = document.getElementById("infoProductoGanador");
  infoDiv.textContent = "";
  const strong = document.createElement("strong");
  strong.textContent = "Producto:";
  infoDiv.appendChild(strong);
  infoDiv.appendChild(
    document.createTextNode(
      ` ${productoNoAdjudicado.monodroga} - ${productoNoAdjudicado.marca} ${productoNoAdjudicado.presentacion}`,
    ),
  );

  fetch(`/api/ofertas/${productoNoAdjudicado.id}`)
    .then((r) => r.json())
    .then((ofertas) => {
      const select = document.getElementById("selectGanador");
      select.textContent = "";
      const defaultOpt = document.createElement("option");
      defaultOpt.value = "";
      defaultOpt.textContent = "Seleccionar oferente...";
      select.appendChild(defaultOpt);

      if (ofertas.length === 0) {
        const noOpt = document.createElement("option");
        noOpt.value = "";
        noOpt.disabled = true;
        noOpt.textContent = "No hay ofertas cargadas";
        select.appendChild(noOpt);
      } else {
        ofertas.forEach((oferta) => {
          const opt = document.createElement("option");
          opt.value = `${oferta.oferente}|${oferta.precio}`;
          opt.textContent = `${oferta.oferente} - ${formatearMoneda(oferta.precio)}`;
          select.appendChild(opt);
        });
      }
    })
    .catch((error) => console.error("Error:", error));

  document.getElementById("modalSeleccionarGanador").style.display = "block";
}

function cerrarModalGanador() {
  const select = document.querySelector(
    `[data-producto-id="${productoNoAdjudicado.id}"]`,
  );
  select.value = productoNoAdjudicado.resultado;
  productoNoAdjudicado = null;
  document.getElementById("modalSeleccionarGanador").style.display = "none";
}

function confirmarGanador() {
  const selectGanador = document.getElementById("selectGanador");
  const valor = selectGanador.value;

  if (!valor) {
    mostrarNotificacion("Debe seleccionar un oferente ganador", "error");
    return;
  }

  const [oferente, precio] = valor.split("|");

  productoNoAdjudicado.resultado = "No Adjudicado";
  productoNoAdjudicado.oferente_ganador = oferente;
  productoNoAdjudicado.precio_ganador = parseFloat(precio);

  document.getElementById("modalSeleccionarGanador").style.display = "none";
  productoNoAdjudicado = null;
}

function abrirModalAlternativas(productoId) {
  // Validate productoId is a safe positive integer
  if (!Number.isInteger(productoId) || productoId <= 0) {
    console.error("Invalid producto ID");
    return;
  }

  productoSeleccionado = productos.find((p) => p.id === productoId);
  const productoOriginal = productosOriginales.find((p) => p.id === productoId);
  const alternativas = alternativasPorProducto[productoId];

  const infoDiv = document.getElementById("productoActual");
  infoDiv.textContent = "";
  const strong = document.createElement("strong");
  strong.textContent = "Producto actual:";
  infoDiv.appendChild(strong);
  infoDiv.appendChild(
    document.createTextNode(
      ` ${productoSeleccionado.marca} - ${productoSeleccionado.presentacion} (${formatearMoneda(productoSeleccionado.precio_ofertado)})`,
    ),
  );

  const listaDiv = document.getElementById("listaAlternativas");
  listaDiv.textContent = "";

  const esPrincipal =
    !productoSeleccionado.producto_cotizar ||
    productoSeleccionado.producto_cotizar === "principal";

  const divPrincipal = document.createElement("div");
  divPrincipal.style.marginBottom = "10px";
  const btnPrincipal = document.createElement("button");
  btnPrincipal.className = esPrincipal ? "btn-primary" : "btn-secondary";
  btnPrincipal.onclick = () => seleccionarAlternativa("principal");
  btnPrincipal.style.cssText = "width: 100%; text-align: left; padding: 15px;";
  btnPrincipal.textContent = `${esPrincipal ? "✅ " : ""}Principal: ${productoOriginal.marca} - ${productoOriginal.presentacion}\nPrecio: ${formatearMoneda(productoOriginal.precio_ofertado)}`;
  divPrincipal.appendChild(btnPrincipal);
  listaDiv.appendChild(divPrincipal);

  alternativas.forEach((alt, idx) => {
    const altKey = `alt-${productoId}-${idx}`;
    const esSeleccionada = productoSeleccionado.producto_cotizar === altKey;
    const divAlt = document.createElement("div");
    divAlt.style.marginBottom = "10px";
    const btnAlt = document.createElement("button");
    btnAlt.className = esSeleccionada ? "btn-primary" : "btn-secondary";
    btnAlt.onclick = () => seleccionarAlternativa(idx);
    btnAlt.style.cssText = "width: 100%; text-align: left; padding: 15px;";
    btnAlt.textContent = `${esSeleccionada ? "✅ " : ""}Alternativa ${idx + 1}: ${alt.marca} - ${alt.presentacion}\nPrecio: ${formatearMoneda(alt.precio_ofertado)}${alt.observaciones ? "\nObs: " + alt.observaciones : ""}`;
    divAlt.appendChild(btnAlt);
    listaDiv.appendChild(divAlt);
  });

  document.getElementById("modalAlternativas").style.display = "block";
}

function seleccionarAlternativa(opcion) {
  const productoOriginal = productosOriginales.find(
    (p) => p.id === productoSeleccionado.id,
  );

  if (opcion === "principal") {
    productoSeleccionado.producto_cotizar = "principal";
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
    productoSeleccionado.laboratorio = alt.laboratorio || "-";
  }

  cerrarModalAlternativas();
  mostrarProductos();
}

function cerrarModalAlternativas() {
  document.getElementById("modalAlternativas").style.display = "none";
}

function abrirModalOfertas(productoId) {
  // Validate productoId is a safe positive integer
  if (!Number.isInteger(productoId) || productoId <= 0) {
    console.error("Invalid producto ID");
    return;
  }

  productoSeleccionado = productos.find((p) => p.id === productoId);
  ofertasTemp = [];
  contadorOfertas = 0;

  const infoDiv = document.getElementById("infoProductoOferta");
  infoDiv.textContent = "";
  const strong = document.createElement("strong");
  strong.textContent = "Producto:";
  infoDiv.appendChild(strong);
  infoDiv.appendChild(
    document.createTextNode(
      ` ${productoSeleccionado.monodroga} - ${productoSeleccionado.marca} ${productoSeleccionado.presentacion}`,
    ),
  );

  document.getElementById("listaOfertas").textContent = "";

  fetch(`/api/ofertas/${productoId}`)
    .then((r) => r.json())
    .then((ofertas) => {
      ofertas.forEach((oferta) => {
        agregarOferta(oferta);
      });
    })
    .catch((error) => console.error("Error cargando ofertas:", error));

  document.getElementById("modalOfertas").style.display = "block";
}

function agregarOferta(ofertaExistente = null) {
  const id = contadorOfertas++;
  const div = document.createElement("div");
  div.id = `oferta-${id}`;
  div.style.cssText =
    "background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); border: 2px solid #4dd0e1; padding: 20px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: all 0.3s;";

  const header = document.createElement("div");
  header.style.cssText =
    "display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #4dd0e1;";
  const title = document.createElement("strong");
  title.style.cssText = "color: #333; font-size: 16px;";
  title.textContent = `💼 Oferta ${id + 1}`;
  const btnEliminar = document.createElement("button");
  btnEliminar.className = "btn-danger";
  btnEliminar.textContent = "✕ Eliminar";
  btnEliminar.style.cssText = "padding: 6px 12px; border-radius: 5px;";
  btnEliminar.onclick = () => eliminarOferta(id);
  header.appendChild(title);
  header.appendChild(btnEliminar);
  div.appendChild(header);

  const grid = document.createElement("div");
  grid.style.cssText = "display: grid; gap: 15px;";

  const divOferente = document.createElement("div");
  const labelOferente = document.createElement("label");
  labelOferente.style.cssText =
    "display: block; margin-bottom: 5px; color: #333; font-weight: 600;";
  labelOferente.textContent = "👥 Oferente:";
  const flexOferente = document.createElement("div");
  flexOferente.style.cssText = "display: flex; gap: 5px;";
  const selectOferente = document.createElement("select");
  selectOferente.id = `oferente-${id}`;
  selectOferente.style.cssText =
    "flex: 1; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px;";
  selectOferente.required = true;
  const defaultOpt = document.createElement("option");
  defaultOpt.value = "";
  defaultOpt.textContent = "Seleccionar oferente...";
  selectOferente.appendChild(defaultOpt);
  oferentes.forEach((o) => {
    const opt = document.createElement("option");
    opt.value = o.nombre;
    opt.textContent = o.nombre;
    selectOferente.appendChild(opt);
  });
  const btnNuevo = document.createElement("button");
  btnNuevo.className = "btn-primary";
  btnNuevo.textContent = "➕";
  btnNuevo.style.cssText = "padding: 10px 15px; border-radius: 5px;";
  btnNuevo.onclick = () => abrirModalNuevoOferente(id);
  flexOferente.appendChild(selectOferente);
  flexOferente.appendChild(btnNuevo);
  divOferente.appendChild(labelOferente);
  divOferente.appendChild(flexOferente);
  grid.appendChild(divOferente);

  const divLab = document.createElement("div");
  const labelLab = document.createElement("label");
  labelLab.style.cssText =
    "display: block; margin-bottom: 5px; color: #333; font-weight: 600;";
  labelLab.textContent = "🏭 Laboratorio:";
  const inputLab = document.createElement("input");
  inputLab.type = "text";
  inputLab.id = `laboratorio-${id}`;
  inputLab.placeholder = "Escriba 3+ letras para buscar...";
  inputLab.setAttribute("list", `laboratorios-${id}`);
  inputLab.required = true;
  inputLab.style.cssText =
    "width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px;";
  const datalist = document.createElement("datalist");
  datalist.id = `laboratorios-${id}`;
  divLab.appendChild(labelLab);
  divLab.appendChild(inputLab);
  divLab.appendChild(datalist);
  grid.appendChild(divLab);

  const divPrecio = document.createElement("div");
  const labelPrecio = document.createElement("label");
  labelPrecio.style.cssText =
    "display: block; margin-bottom: 5px; color: #333; font-weight: 600;";
  labelPrecio.textContent = "💵 Precio:";
  const inputPrecio = document.createElement("input");
  inputPrecio.type = "number";
  inputPrecio.id = `precio-${id}`;
  inputPrecio.placeholder = "0.00";
  inputPrecio.step = "0.01";
  inputPrecio.required = true;
  inputPrecio.style.cssText =
    "width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px;";
  divPrecio.appendChild(labelPrecio);
  divPrecio.appendChild(inputPrecio);
  grid.appendChild(divPrecio);

  div.appendChild(grid);
  document.getElementById("listaOfertas").appendChild(div);

  if (ofertaExistente) {
    document.getElementById(`oferente-${id}`).value = ofertaExistente.oferente;
    document.getElementById(`laboratorio-${id}`).value =
      ofertaExistente.laboratorio;
    document.getElementById(`precio-${id}`).value = ofertaExistente.precio;
  }

  inputLab.addEventListener("input", function () {
    const valor = this.value;
    const datalist = document.getElementById(`laboratorios-${id}`);

    if (valor.length >= 3) {
      const filtrados = laboratorios.filter((l) =>
        l.toLowerCase().includes(valor.toLowerCase()),
      );
      datalist.textContent = "";
      filtrados.forEach((l) => {
        const opt = document.createElement("option");
        opt.value = l;
        datalist.appendChild(opt);
      });
    } else {
      datalist.textContent = "";
    }
  });

  div.addEventListener("mouseenter", function () {
    this.style.transform = "translateY(-2px)";
    this.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
  });
  div.addEventListener("mouseleave", function () {
    this.style.transform = "translateY(0)";
    this.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
  });
}

function eliminarOferta(id) {
  document.getElementById(`oferta-${id}`)?.remove();
}

function cerrarModalOfertas() {
  document.getElementById("modalOfertas").style.display = "none";
}

function guardarOfertas() {
  const ofertas = [];
  document.querySelectorAll('[id^="oferta-"]').forEach((div) => {
    const id = div.id.split("-")[1];
    const oferente = document.getElementById(`oferente-${id}`)?.value;
    const laboratorio = document.getElementById(`laboratorio-${id}`)?.value;
    const precio = document.getElementById(`precio-${id}`)?.value;

    if (oferente && laboratorio && precio) {
      ofertas.push({ oferente, laboratorio, precio: parseFloat(precio) });
    }
  });

  fetch(`/api/ofertas/${productoSeleccionado.id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ofertas }),
  })
    .then((r) => r.json())
    .then((data) => {
      if (data.success) {
        mostrarNotificacion(
          `${ofertas.length} oferta(s) guardada(s) correctamente`,
          "success",
        );
        cerrarModalOfertas();
      } else {
        mostrarNotificacion("Error al guardar ofertas: " + data.error, "error");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      mostrarNotificacion("Error al guardar ofertas", "error");
    });
}

function abrirModalNuevoOferente(ofertaId) {
  document.getElementById("formNuevoOferente").dataset.ofertaId = ofertaId;
  document.getElementById("nuevoOferenteNombre").value = "";
  document.getElementById("modalNuevoOferente").style.display = "block";
}

function cerrarModalNuevoOferente() {
  document.getElementById("modalNuevoOferente").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
  const formOferente = document.getElementById("formNuevoOferente");
  if (formOferente) {
    formOferente.addEventListener("submit", function (e) {
      e.preventDefault();

      const nombre = document.getElementById("nuevoOferenteNombre").value;
      const ofertaId = this.dataset.ofertaId;

      fetch("/api/oferentes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre }),
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.success) {
            oferentes.push({ id: data.id, nombre });

            const select = document.getElementById(`oferente-${ofertaId}`);
            const option = document.createElement("option");
            option.value = nombre;
            option.text = nombre;
            option.selected = true;
            select.appendChild(option);

            cerrarModalNuevoOferente();
          } else {
            mostrarNotificacion(
              "Error al crear oferente: " + data.error,
              "error",
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          mostrarNotificacion("Error al crear oferente", "error");
        });
    });
  }
});

function guardarResultados() {
  const selects = document.querySelectorAll(".resultado-select");
  const actualizaciones = [];

  selects.forEach((select) => {
    const productoId = parseInt(select.dataset.productoId);
    
    // Validate productoId is a safe positive integer
    if (!Number.isInteger(productoId) || productoId <= 0) {
      console.error("Invalid producto ID");
      return;
    }
    
    const producto = productos.find((p) => p.id === productoId);

    actualizaciones.push(
      fetch(`/api/productos/${productoId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          monodroga: producto.monodroga,
          marca: producto.marca,
          presentacion: producto.presentacion,
          cantidad: producto.cantidad,
          precio_ofertado: producto.precio_ofertado,
          resultado: select.value,
          precio_ganador: producto.precio_ganador || null,
          oferente: producto.oferente_ganador || "",
          marca_ofrecida: producto.marca_ofrecida || "",
          marca_ganadora: producto.marca_ganadora || "",
          motivo_perdida: producto.motivo_perdida || "",
          numero_renglon: producto.numero_renglon || "",
          costo_unitario: producto.costo_unitario || null,
          margen_porcentaje: producto.margen_porcentaje || null,
          observaciones: producto.observaciones || "",
          producto_cotizar: producto.producto_cotizar || "principal",
        }),
      }),
    );
  });

  Promise.all(actualizaciones)
    .then(() => {
      mostrarNotificacion("Resultados guardados correctamente", "success");
      setTimeout(() => {
        window.location.href = "/gestion-nueva";
      }, 1000);
    })
    .catch((error) => {
      console.error("Error:", error);
      mostrarNotificacion("Error al guardar los resultados", "error");
    });
}

function mostrarNotificacion(mensaje, tipo) {
  const notif = document.createElement("div");
  notif.textContent = mensaje;
  notif.style.cssText = `position: fixed; top: 20px; right: 20px; padding: 15px 20px; border-radius: 5px; z-index: 10000; background: ${tipo === "success" ? "#4caf50" : "#f44336"}; color: white; font-weight: bold;`;
  document.body.appendChild(notif);
  setTimeout(() => notif.remove(), 3000);
}
