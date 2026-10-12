// Captura pantallas reales de index.html con datos de demostración
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const mock = require('./mock');
const OUT = path.join(__dirname, 'shots');
fs.mkdirSync(OUT, { recursive: true });
const BASE = 'http://127.0.0.1:8765/index.html';

async function nueva(browser, opts) {
  const ctx = await browser.newContext(opts);
  await ctx.route('https://script.google.com/**', async r => {
    const { fn, args } = JSON.parse(r.request().postData());
    await new Promise(res => setTimeout(res, 30));
    r.fulfill({ status: 200, headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
      body: JSON.stringify({ ok: true, data: mock[fn](...args) }) });
  });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.error('ERR', e.message));
  return page;
}
const shot = (p, n, full) => p.screenshot({ path: path.join(OUT, n + '.png'), fullPage: !!full });
const espera = p => p.waitForTimeout(500);

(async () => {
  const browser = await chromium.launch({ args: ['--lang=es-BO'], env: { ...process.env, LANG: 'es_BO.UTF-8', LANGUAGE: 'es' } }).catch(() => chromium.launch());
  const desk = { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, locale: 'es-BO' };

  // Login
  let p = await nueva(browser, desk);
  await p.goto(BASE); await espera(p);
  await p.fill('#lU', 'aquispe'); await p.fill('#lP', '123456'); await p.locator('#lP').blur();
  await shot(p, '01_login');
  await p.click('#bIn'); await p.waitForSelector('.kpis'); await espera(p);
  await shot(p, '02_activos');
  // Filtro y selección
  for (const c of ['ECO-0001', 'RTC-0001', 'EQI-0001']) await p.click(`.sel[data-c="${c}"]`);
  await espera(p); await shot(p, '03_seleccion');
  // Formulario nuevo
  await p.click('#bNuevo'); await espera(p);
  await p.selectOption('#aCat', 'Routers en comodato'); await p.dispatchEvent('#aCat', 'change');
  await p.fill('#aDes', 'Router ONT doble banda'); await p.fill('#aMar', 'ZTE'); await p.fill('#aMod', 'F670L');
  await p.fill('#aSer', 'ZTEG8C21C7'); await p.selectOption('#aRes', 'Lucía Vargas');
  await p.fill('#aCli', 'Librería San Andrés'); await p.fill('#aDir', 'Av. 6 de Agosto 2450, La Paz');
  await p.fill('#aFec', '2026-10-05'); await p.fill('#aCos', '540'); await p.fill('#aPro', 'Distribuidora Andina'); await p.fill('#aFac', '000981');
  await p.locator('#aFac').blur();
  await p.evaluate(() => { const f = document.getElementById('aFoto'); f.style.display = 'none';
    f.insertAdjacentHTML('afterend', '<span style="display:inline-flex;gap:8px;align-items:center;margin-top:8px;font-size:14px;font-weight:400;text-transform:none;letter-spacing:0;color:#13213A"><span style="border:1px solid #767676;background:#EFEFEF;border-radius:3px;padding:1px 6px">Seleccionar archivo</span>Ningún archivo seleccionado</span>'); });
  await espera(p);
  await shot(p, '04_nuevo', true);
  // Ficha
  await p.click('#bCanc'); await espera(p);
  await p.click('tr.clic[data-c="ECO-0001"] td:nth-child(3)'); await p.waitForSelector('.cuadroDep'); await p.waitForTimeout(900);
  await shot(p, '05_ficha', true);
  // Etiquetas
  await p.click('#bVolver'); await espera(p);
  await p.click('#bEt'); await p.waitForSelector('.et'); await p.waitForTimeout(900);
  await shot(p, '06_etiquetas', true);
  await p.selectOption('#eTam', 'pequena'); await p.waitForTimeout(600);
  // Inventario
  await p.click('#tabs button[data-t="inventario"]'); await p.waitForSelector('#iLista table'); await espera(p);
  await shot(p, '07_inventario');
  await p.click('#bMov'); await espera(p);
  await p.selectOption('#mCod', 'INV-0003'); await p.selectOption('#mUbi', 'Depósito Río Seco'); await p.dispatchEvent('#mUbi', 'change');
  await p.fill('#mCan', '30'); await p.fill('#mCos', '550'); await p.fill('#mDoc', 'Factura 1931'); await p.fill('#mMot', 'Compra mensual');
  await p.selectOption('#mRes', 'Jorge Condori'); await p.locator('#mMot').blur(); await espera(p);
  await shot(p, '08_movimiento');
  await p.click('#bCM'); await espera(p);
  await p.click('#iLista tr.clic[data-c="INV-0003"]'); await p.waitForSelector('.hist'); await espera(p);
  await shot(p, '09_kardex', true);
  await p.context().close();

  // Vista pública en el celular
  p = await nueva(browser, { viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, locale: 'es-BO' });
  await p.goto(BASE + '?c=RTC-0001'); await p.waitForSelector('.publica h1'); await espera(p);
  await shot(p, '10_publica');
  await p.context().close();

  await browser.close();
})();
