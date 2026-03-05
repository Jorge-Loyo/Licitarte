import './admin/admin-utils.js';
import * as Clientes from './admin/clientes.js';
import * as Oferentes from './admin/oferentes.js';
import * as Marcas from './admin/marcas.js';
import * as Tipos from './admin/tipos.js';
import * as Organismos from './admin/organismos.js';
import * as Portales from './admin/portales.js';
import * as Modalidades from './admin/modalidades.js';
import * as FormasPago from './admin/formas-pago.js';
import * as MotivosPerdida from './admin/motivos-perdida.js';
import * as Mantenimientos from './admin/mantenimientos.js';
import * as Laboratorios from './admin/laboratorios.js';
import * as Monodrogas from './admin/monodrogas.js';
import * as Catalogo from './admin/catalogo.js';

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const tab = e.target.dataset.tab;
      mostrarTab(tab);
    });
  });

  // Clientes
  document.getElementById('btnNuevoCliente')?.addEventListener('click', Clientes.nuevoCliente);
  document.getElementById('btnCargarExcelClientes')?.addEventListener('click', () => document.getElementById('excelClientes').click());
  document.getElementById('excelClientes')?.addEventListener('change', Clientes.subirExcelClientes);
  document.getElementById('clienteForm')?.addEventListener('submit', Clientes.guardarCliente);

  // Oferentes
  document.getElementById('btnNuevoOferente')?.addEventListener('click', Oferentes.nuevoOferente);
  document.getElementById('btnCargarExcelOferentes')?.addEventListener('click', () => document.getElementById('excelOferentes').click());
  document.getElementById('excelOferentes')?.addEventListener('change', Oferentes.subirExcelOferentes);
  document.getElementById('oferenteForm')?.addEventListener('submit', Oferentes.guardarOferente);

  // Marcas
  document.getElementById('btnNuevaMarca')?.addEventListener('click', Marcas.nuevaMarca);
  document.getElementById('btnCargarExcelMarcas')?.addEventListener('click', () => document.getElementById('excelMarcas').click());
  document.getElementById('excelMarcas')?.addEventListener('change', Marcas.subirExcelMarcas);
  document.getElementById('marcaForm')?.addEventListener('submit', Marcas.guardarMarca);

  // Tipos
  document.getElementById('btnNuevoTipo')?.addEventListener('click', Tipos.nuevoTipo);
  document.getElementById('btnCargarExcelTipos')?.addEventListener('click', () => document.getElementById('excelTipos').click());
  document.getElementById('excelTipos')?.addEventListener('change', Tipos.subirExcelTipos);
  document.getElementById('tipoForm')?.addEventListener('submit', Tipos.guardarTipo);

  // Organismos
  document.getElementById('btnNuevoOrganismo')?.addEventListener('click', Organismos.nuevoOrganismo);
  document.getElementById('organismoForm')?.addEventListener('submit', Organismos.guardarOrganismo);

  // Portales
  document.getElementById('btnNuevoPortal')?.addEventListener('click', Portales.nuevoPortal);
  document.getElementById('portalForm')?.addEventListener('submit', Portales.guardarPortal);

  // Modalidades
  document.getElementById('btnNuevaModalidad')?.addEventListener('click', Modalidades.nuevaModalidad);
  document.getElementById('modalidadForm')?.addEventListener('submit', Modalidades.guardarModalidad);

  // Formas de Pago
  document.getElementById('btnNuevaFormaPago')?.addEventListener('click', FormasPago.nuevaFormaPago);
  document.getElementById('formaPagoForm')?.addEventListener('submit', FormasPago.guardarFormaPago);

  // Motivos Perdida
  document.getElementById('btnNuevoMotivoPerdida')?.addEventListener('click', MotivosPerdida.nuevoMotivoPerdida);
  document.getElementById('motivoPerdidaForm')?.addEventListener('submit', MotivosPerdida.guardarMotivoPerdida);

  // Mantenimientos
  document.getElementById('btnNuevoMantenimiento')?.addEventListener('click', Mantenimientos.nuevoMantenimiento);
  document.getElementById('mantenimientoForm')?.addEventListener('submit', Mantenimientos.guardarMantenimiento);

  // Laboratorios
  document.getElementById('btnNuevoLaboratorio')?.addEventListener('click', Laboratorios.nuevoLaboratorio);
  document.getElementById('btnCargarExcelLaboratorios')?.addEventListener('click', () => document.getElementById('excelLaboratorios').click());
  document.getElementById('excelLaboratorios')?.addEventListener('change', Laboratorios.subirExcelLaboratorios);
  document.getElementById('laboratorioForm')?.addEventListener('submit', Laboratorios.guardarLaboratorio);

  // Monodrogas
  document.getElementById('btnNuevaMonodroga')?.addEventListener('click', Monodrogas.nuevaMonodroga);
  document.getElementById('btnCargarExcelMonodrogas')?.addEventListener('click', () => document.getElementById('excelMonodrogas').click());
  document.getElementById('excelMonodrogas')?.addEventListener('change', Monodrogas.subirExcelMonodrogas);
  document.getElementById('btnBuscarMonodroga')?.addEventListener('click', Monodrogas.buscarMonodroga);
  document.getElementById('monodrogaForm')?.addEventListener('submit', Monodrogas.guardarMonodroga);

  // Catalogo
  document.getElementById('btnNuevoProductoCatalogo')?.addEventListener('click', Catalogo.nuevoProductoCatalogo);
  document.getElementById('btnCargarExcelCatalogo')?.addEventListener('click', () => document.getElementById('excelFile').click());
  document.getElementById('excelFile')?.addEventListener('change', Catalogo.subirExcel);
  document.getElementById('btnBuscarCatalogo')?.addEventListener('click', Catalogo.buscarCatalogo);
  document.getElementById('productoCatalogoForm')?.addEventListener('submit', Catalogo.guardarProductoCatalogo);

  // Cerrar modales
  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.getElementById(e.target.dataset.close).style.display = 'none';
    });
  });

  Clientes.cargarClientes();
});

function mostrarTab(tab) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

  document.getElementById(`tab-${tab}`).classList.add('active');
  document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

  if (tab === 'clientes') Clientes.cargarClientes();
  if (tab === 'oferentes') Oferentes.cargarOferentes();
  if (tab === 'marcas') Marcas.cargarMarcas();
  if (tab === 'tipos') Tipos.cargarTipos();
  if (tab === 'organismos') Organismos.cargarOrganismos();
  if (tab === 'portales') Portales.cargarPortales();
  if (tab === 'modalidades') Modalidades.cargarModalidades();
  if (tab === 'formas') FormasPago.cargarFormasPago();
  if (tab === 'motivos') MotivosPerdida.cargarMotivosPerdida();
  if (tab === 'mantenimientos') Mantenimientos.cargarMantenimientos();
  if (tab === 'laboratorios') Laboratorios.cargarLaboratorios();
  if (tab === 'monodrogas') Monodrogas.cargarMonodrogas();
  if (tab === 'catalogo') Catalogo.cargarCatalogo();
}
