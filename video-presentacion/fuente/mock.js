// Datos de demostración para capturar la interfaz real sin conectarse a Google
const router = `data:image/svg+xml;utf8,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2f8"/><stop offset="1" stop-color="#cfd8e6"/></linearGradient>
<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3e63"/><stop offset="1" stop-color="#13213A"/></linearGradient></defs>
<rect width="400" height="300" fill="url(#g)"/>
<ellipse cx="200" cy="232" rx="150" ry="14" fill="#13213A" opacity=".15"/>
<rect x="110" y="70" width="8" height="90" rx="4" fill="#13213A"/><rect x="282" y="70" width="8" height="90" rx="4" fill="#13213A"/>
<rect x="60" y="150" width="280" height="78" rx="16" fill="url(#b)"/>
<rect x="60" y="150" width="280" height="10" rx="5" fill="#3a5080"/>
<circle cx="100" cy="196" r="6" fill="#3ddc84"/><circle cx="124" cy="196" r="6" fill="#3ddc84"/><circle cx="148" cy="196" r="6" fill="#E11B22"/><circle cx="172" cy="196" r="6" fill="#3ddc84"/>
<rect x="230" y="186" width="80" height="20" rx="4" fill="#0b1528"/>
</svg>`)}`;

const categorias = [
  ['Edificaciones','EDI',40,'Sí'],['Muebles y enseres de oficina','MUE',10,'Sí'],['Maquinaria en general','MAQ',8,'Sí'],
  ['Equipos e instalaciones','EQI',8,'Sí'],['Vehículos automotores','VEH',5,'Sí'],['Herramientas en general','HER',4,'Sí'],
  ['Equipos de computación','ECO',4,'Sí'],['Routers en comodato','RTC',4,'Sí'],['Terrenos','TER',0,'No']
].map(([nombre, prefijo, vida, d]) => ({ nombre, prefijo, vida, deprecia: d === 'Sí' }));

const listas = {
  categorias,
  ubicaciones: ['Oficina Central','Casa José','Depósito Río Seco','Depósito Busch','Depósito Nantes','En comodato'],
  responsables: ['Ana Quispe','Carlos Mamani','Lucía Vargas','Jorge Condori','Rosa Choque'],
  catInventario: ['Equipos de red','Cableado','Conectores y accesorios','Herramientas menores'],
  unidades: ['Unidad','Metro','Rollo','Caja','Paquete'],
  estados: ['Operativo','En mantenimiento','En desuso','Dado de baja'],
  tiposMov: ['Entrada','Salida','Ajuste positivo','Ajuste negativo','Traspaso'],
  comodato: 'En comodato'
};

const A = (codigo, categoria, descripcion, marca, modelo, serie, ubicacion, responsable, estado, costo, valorLibros, cliente='') =>
  ({ codigo, categoria, descripcion, marca, modelo, serie, ubicacion, cliente, responsable, estado, costo,
     costoAct: +(costo * 1.0412).toFixed(2), valorLibros, depAcum: 0, tieneFoto: true });

const activos = [
  A('ECO-0001','Equipos de computación','Laptop para contabilidad','Lenovo','ThinkPad E14','PF3K9Z21','Oficina Central','Ana Quispe','Operativo',7850,2894.75),
  A('ECO-0002','Equipos de computación','Servidor de monitoreo de red','Dell','PowerEdge T150','8XQ2M73','Oficina Central','Carlos Mamani','Operativo',18400,12655.80),
  A('EQI-0001','Equipos e instalaciones','OLT de fibra óptica 8 puertos PON','Huawei','MA5800-X2','21023519','Depósito Río Seco','Jorge Condori','Operativo',42600,35118.40),
  A('HER-0001','Herramientas en general','Empalmadora de fibra óptica','Fujikura','70S+','FS70-5521','Depósito Busch','Jorge Condori','En mantenimiento',23900,15386.10),
  A('RTC-0001','Routers en comodato','Router ONT doble banda','ZTE','F670L','ZTEG8C21A9','En comodato','Lucía Vargas','Operativo',540,421.20,'Familia Gutiérrez'),
  A('RTC-0002','Routers en comodato','Router ONT doble banda','ZTE','F670L','ZTEG8C21B4','En comodato','Lucía Vargas','Operativo',540,421.20,'Ferretería El Sol'),
  A('VEH-0001','Vehículos automotores','Camioneta de instalaciones','Toyota','Hilux 4x4','MR0FB8CD2N','Casa José','Carlos Mamani','Operativo',245000,186240.00),
  A('MUE-0001','Muebles y enseres de oficina','Escritorio ejecutivo en L','Muebles Kantuta','EL-160','—','Oficina Central','Ana Quispe','Operativo',2350,1984.60),
  A('EQI-0002','Equipos e instalaciones','Switch de distribución 24 puertos','MikroTik','CRS326-24G','HD8A09QWE','Depósito Nantes','Rosa Choque','Operativo',3120,2470.90),
  A('ECO-0003','Equipos de computación','Impresora multifuncional','Epson','L6270','X8JK004512','Oficina Central','Rosa Choque','En desuso',2190,610.25),
];

const detalle = {
  ...activos[0], costoAct: 8173.42, fechaAdq: '2024-03-15', residual: 0, proveedor: 'CompuTec S.R.L.', factura: '004512',
  direccion: '', observaciones: 'Incluye cargador y mochila.', foto: router, fechaBaja: '', motivoBaja: '',
  registradoPor: 'Ana Quispe (aquispe)', fechaRegistro: '15/03/2024 10:42', fechaCalculo: '2026-10-12', ufvActiva: true,
  dep: { costoHist: 7850, factor: 1.04120, costoAct: 8173.42, vidaMeses: 48, vidaAnios: 4, meses: 31, depAcum: 5278.67,
         depGestion: 1702.80, valorLibros: 2894.75, avisos: [] },
  verificaciones: [
    { fecha: '02/10/2026 09:15', ubicacion: 'Oficina Central', coincide: 'Sí', obs: 'Conteo anual', por: 'Rosa Choque (rchoque)' },
    { fecha: '14/04/2026 16:02', ubicacion: 'Casa José', coincide: 'No', obs: 'Llevada para trabajo remoto', por: 'Carlos Mamani (cmamani)' }
  ],
  historial: [
    { fecha: '20/04/2026 08:30', campo: 'Ubicación', antes: 'Casa José', despues: 'Oficina Central', usuario: 'Ana Quispe (aquispe)', origen: 'Aplicación' },
    { fecha: '10/01/2025 11:12', campo: 'Responsable', antes: 'Jorge Condori', despues: 'Ana Quispe', usuario: 'Administrador (admin)', origen: 'Hoja de cálculo' }
  ]
};
detalle.foto = router;
// Foto de laptop para la ficha principal
detalle.foto = `data:image/svg+xml;utf8,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2f8"/><stop offset="1" stop-color="#cfd8e6"/></linearGradient></defs>
<rect width="400" height="300" fill="url(#g)"/><ellipse cx="200" cy="240" rx="165" ry="12" fill="#13213A" opacity=".15"/>
<rect x="95" y="60" width="210" height="140" rx="10" fill="#13213A"/><rect x="105" y="70" width="190" height="118" rx="4" fill="#2b3e63"/>
<rect x="118" y="84" width="90" height="10" rx="3" fill="#E11B22"/><rect x="118" y="102" width="150" height="6" rx="3" fill="#8fa3c6"/>
<rect x="118" y="116" width="120" height="6" rx="3" fill="#8fa3c6"/><rect x="118" y="130" width="160" height="40" rx="4" fill="#3a5080"/>
<path d="M60 200 h280 l-20 30 h-240z" fill="#1c2c4a"/><rect x="170" y="206" width="60" height="6" rx="3" fill="#3a5080"/></svg>`)}`;

const inv = {
  listas,
  items: [
    { codigo:'INV-0001', descripcion:'Cable de fibra óptica drop 1 hilo', categoria:'Cableado', unidad:'Metro', stockMin:2000, stock:6450, prom:1.18, valor:7611.00, situacion:'Normal', porUbicacion:{'Depósito Río Seco':4200,'Depósito Busch':2250} },
    { codigo:'INV-0002', descripcion:'Conector rápido SC/APC', categoria:'Conectores y accesorios', unidad:'Unidad', stockMin:300, stock:240, prom:4.35, valor:1044.00, situacion:'Reponer', porUbicacion:{'Depósito Río Seco':240} },
    { codigo:'INV-0003', descripcion:'Router ONT ZTE F670L (nuevo)', categoria:'Equipos de red', unidad:'Unidad', stockMin:20, stock:64, prom:538.75, valor:34480.00, situacion:'Normal', porUbicacion:{'Depósito Río Seco':40,'Depósito Nantes':24} },
    { codigo:'INV-0004', descripcion:'Patch cord UTP cat. 6 de 1 m', categoria:'Cableado', unidad:'Unidad', stockMin:50, stock:0, prom:0, valor:0, situacion:'Sin stock', porUbicacion:{} },
    { codigo:'INV-0005', descripcion:'Caja de distribución NAP 16 puertos', categoria:'Equipos de red', unidad:'Unidad', stockMin:10, stock:37, prom:212.40, valor:7858.80, situacion:'Normal', porUbicacion:{'Depósito Busch':37} },
    { codigo:'INV-0006', descripcion:'Precinto plástico 30 cm', categoria:'Conectores y accesorios', unidad:'Paquete', stockMin:15, stock:42, prom:12.50, valor:525.00, situacion:'Normal', porUbicacion:{'Depósito Nantes':42} },
  ]
};

const kardex = [
  { fecha:'2026-08-04', numero:'M-000112', tipo:'Entrada', ubicacion:'Depósito Río Seco', destino:'', cantidad:50, documento:'Factura 1876', motivo:'', cuAplicado:530.00, importe:26500.00, saldoCant:50, saldoValor:26500.00, alerta:'' },
  { fecha:'2026-08-21', numero:'M-000131', tipo:'Salida', ubicacion:'Depósito Río Seco', destino:'', cantidad:12, documento:'', motivo:'Instalación a clientes zona sur', cuAplicado:530.00, importe:6360.00, saldoCant:38, saldoValor:20140.00, alerta:'' },
  { fecha:'2026-09-02', numero:'M-000140', tipo:'Entrada', ubicacion:'Depósito Río Seco', destino:'', cantidad:30, documento:'Factura 1931', motivo:'', cuAplicado:550.00, importe:16500.00, saldoCant:68, saldoValor:36640.00, alerta:'' },
  { fecha:'2026-09-15', numero:'M-000152', tipo:'Traspaso', ubicacion:'Depósito Río Seco', destino:'Depósito Nantes', cantidad:24, documento:'', motivo:'Stock para zona norte', cuAplicado:538.82, importe:12931.76, saldoCant:68, saldoValor:36640.00, alerta:'' },
  { fecha:'2026-10-01', numero:'M-000168', tipo:'Salida', ubicacion:'Depósito Río Seco', destino:'', cantidad:4, documento:'', motivo:'OT 2291 · clientes El Alto', cuAplicado:538.82, importe:2155.29, saldoCant:64, saldoValor:34484.71, alerta:'' },
];

module.exports = {
  iniciarSesion: () => ({ token: 'demo', nombre: 'Ana Quispe', rol: 'Administrador', usuario: 'aquispe' }),
  datosIniciales: () => ({ sesion: { usuario:'aquispe', nombre:'Ana Quispe', rol:'Administrador' }, empresa:'BolDataSat Technologies S.R.L.',
    url:'https://boldatasat.github.io/activos/', listas, activos, fechaCalculo:'2026-10-12', ufv:true }),
  detalleActivo: () => detalle,
  fichaPublica: () => ({ empresa:'BolDataSat Technologies S.R.L.', codigo:'RTC-0001', descripcion:'Router ONT doble banda', categoria:'Routers en comodato',
    marca:'ZTE', modelo:'F670L', serie:'ZTEG8C21A9', ubicacion:'En comodato', responsable:'Lucía Vargas', estado:'Operativo', foto: router }),
  etiquetas: (t, cods) => ({ empresa:'BolDataSat Technologies S.R.L.', url:'https://boldatasat.github.io/activos/',
    items: activos.filter(a => cods.includes(a.codigo)).map(a => ({ codigo:a.codigo, descripcion:a.descripcion, ubicacion:a.ubicacion })) }),
  inventario: () => inv,
  kardexItem: () => kardex,
  cerrarSesion: () => true,
};
