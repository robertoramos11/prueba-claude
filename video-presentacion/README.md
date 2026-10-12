# Video de presentación · Sistema de Control de Activos (BolDataSat)

`presentacion_control_activos.mp4`: video de presentación y capacitación del personal (1920×1080, 30 fps, unos 4 min 24 s).

## Contenido

| Tiempo | Sección |
|---|---|
| 0:00 | Portada |
| 0:07 | ¿Para qué sirve? (QR, depreciación + UFV, kárdex) |
| 0:18 | Cómo funciona (Google Sheets → Apps Script → aplicación web → etiqueta QR) |
| 0:30 | 01 · Ingreso con usuario y PIN, y los tres roles (Administrador, Editor, Consulta) |
| 0:44 | 02 · Lista de activos fijos, totales y filtros |
| 0:59 | 03 · Registro de un activo nuevo (código automático, comodato, costo sin IVA, foto) |
| 1:15 | 04 · Ficha del activo |
| 1:29 | 05 · Depreciación: vida útil según el DS 24051 y cálculo con UFV paso a paso |
| 1:59 | 06 · Impresión de etiquetas QR |
| 2:13 | 07 · Escaneo con el celular (ficha pública y acceso del personal) |
| 2:28 | 08 · Verificación física y bitácora |
| 2:43 | 09 · Dar de baja |
| 2:52 | Inventarios: existencias y situación (Normal, Reponer, Sin stock) |
| 3:11 | 11 · Movimientos (entrada, salida, ajustes y traspaso) |
| 3:27 | 12 · Kárdex físico valorado (promedio ponderado) |
| 3:43 | 13 · La hoja de cálculo y el menú «Control de activos» |
| 3:57 | 14 · Seis reglas de oro para el personal |
| 4:14 | Cierre |

Las pantallas son capturas reales de `index.html`, cargadas con datos de demostración (`fuente/mock.js`). Ningún dato es real.

## Música

La música de fondo es una composición original creada con código (`fuente/musica.py`): sintetizadores, bajo, arpegio y batería suave a 96 BPM, generados por completo con NumPy. No usa muestras, grabaciones ni obras de terceros, así que **no tiene derechos de autor ajenos** y puede usarse libremente, incluso en redes sociales.

## Cómo regenerarlo

1. `fuente/capturar.js` toma las capturas de la aplicación con Playwright.
2. `fuente/video.html` contiene las escenas animadas y la línea de tiempo.
3. `fuente/render.js` dibuja el video cuadro a cuadro y lo pasa a ffmpeg.
4. Con `python3 fuente/musica.py <duración> musica.wav` se genera la música, y ffmpeg une la música con el video.
