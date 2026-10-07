'use strict';

/* La app no decide nada. Recoge una situación, la manda al servidor y
   muestra el veredicto que devuelve fichar(). Los textos de rechazo son
   los de la base de datos, no están escritos aquí. */

let ctx = null;       // obra y trabajadores
let escenario = null;
let lang = 'es';

const T = {
  entrada:           { es:'Entrada',             en:'Clock in' },
  salida:            { es:'Salida',              en:'Clock out' },
  inicio_descanso:   { es:'Inicio de descanso',  en:'Break start' },
  fin_descanso:      { es:'Fin de descanso',     en:'Break end' },
  aceptada:          { es:'Aceptada',            en:'Accepted' },
  rechazada:         { es:'Rechazada',           en:'Rejected' },
  sinMarcas:         { es:'Todavía no has fichado hoy.', en:'No marks yet today.' },
  registrar:         { es:'Registrar ',          en:'Register ' },
};

/* Cada escenario es una posición y un estado del teléfono. El de "otro
   teléfono" usa la huella del compañero a propósito. */
const ESCENARIOS = [
  { id:'obra',     x:52, y:44, lat:37.804650, lon:-122.271100, precision:12, simulada:false, suHuella:true,
    es:'Estoy en la obra', en:'I am on site',
    esSub:'A unos 28 m del centro', enSub:'About 28 m from the centre' },
  { id:'casa',     x:14, y:16, lat:37.818000, lon:-122.271100, precision:10, simulada:false, suHuella:true,
    es:'Desde casa', en:'From home',
    esSub:'A 1,5 km de la obra', enSub:'1.5 km from the site' },
  { id:'simulada', x:50, y:50, lat:37.804400, lon:-122.271100, precision:5,  simulada:true,  suHuella:true,
    es:'Con ubicación simulada', en:'With a fake location',
    esSub:'Coordenadas perfectas, falsas', enSub:'Perfect coordinates, faked' },
  { id:'ajeno',    x:54, y:47, lat:37.804500, lon:-122.271050, precision:9,  simulada:false, suHuella:false,
    es:'Desde el teléfono de un compañero', en:"From a workmate's phone",
    esSub:'En la obra, pero no es su aparato', enSub:'On site, but not his device' },
  { id:'impreciso',x:58, y:38, lat:37.804800, lon:-122.271400, precision:140, simulada:false, suHuella:true,
    es:'Con mala señal', en:'With poor signal',
    esSub:'Precisión de 140 m', enSub:'Accuracy of 140 m' },
];

const $ = (id) => document.getElementById(id);

function idioma(l) {
  lang = l;
  document.documentElement.lang = l;
  document.querySelectorAll('[data-es]').forEach(el => {
    const v = el.getAttribute('data-' + l);
    if (v !== null) el.textContent = v;
  });
  document.querySelectorAll('.idioma button').forEach(b =>
    b.classList.toggle('on', b.textContent.toLowerCase() === l));
  pintarEscenarios();
  pintarMarcas(ultimasMarcas);
  pintarBoton();
}

function pintarEscenarios() {
  $('escenarios').innerHTML = ESCENARIOS.map(e => `
    <button class="${e.id === escenario?.id ? 'on' : ''}" onclick="elegir('${e.id}')">
      ${e[lang]}<small>${e[lang + 'Sub']}</small>
    </button>`).join('');
}

function elegir(id) {
  escenario = ESCENARIOS.find(e => e.id === id);
  const yo = $('yo');
  yo.style.left = escenario.x + '%';
  yo.style.top = escenario.y + '%';
  yo.style.background = escenario.id === 'obra' ? '#0ca30c' : '#c2410c';

  const d = distancia(escenario.lat, escenario.lon, ctx.obra.lat, ctx.obra.lon);
  $('distancia').textContent = Math.round(d) + ' m';
  $('precision').textContent = escenario.precision + ' m';
  $('telefono').textContent = escenario.suHuella
    ? (lang === 'es' ? 'el suyo' : 'his own')
    : (lang === 'es' ? 'de otro' : "someone else's");
  $('veredicto').hidden = true;
  pintarEscenarios();
  pintarBoton();
}

/* Haversine, solo para enseñar la distancia en pantalla. La que cuenta la
   calcula Postgres con earthdistance. */
function distancia(lat1, lon1, lat2, lon2) {
  const R = 6371000, r = Math.PI / 180;
  const a = Math.sin((lat2 - lat1) * r / 2) ** 2
          + Math.cos(lat1 * r) * Math.cos(lat2 * r) * Math.sin((lon2 - lon1) * r / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

/* El siguiente tipo de marca sale de la última aceptada, igual que en la base. */
let ultimasMarcas = [];
function siguienteTipo() {
  const ultima = ultimasMarcas.find(m => m.veredicto === 'aceptada');
  if (!ultima || ultima.tipo === 'salida') return 'entrada';
  if (ultima.tipo === 'entrada') return 'inicio_descanso';
  if (ultima.tipo === 'inicio_descanso') return 'fin_descanso';
  return 'salida';
}

function pintarBoton() {
  const b = $('fichar');
  b.disabled = !escenario;
  b.textContent = T.registrar[lang] + T[siguienteTipo()][lang].toLowerCase();
}

function pintarMarcas(marcas) {
  ultimasMarcas = marcas || [];
  $('hoy').innerHTML = ultimasMarcas.length === 0
    ? `<div class="vacio">${T.sinMarcas[lang]}</div>`
    : ultimasMarcas.map(m => {
        const ok = m.veredicto === 'aceptada';
        return `<div class="marca">
          <span>${T[m.tipo][lang]}</span>
          <span class="hora">${m.hora}</span>
          <span class="estado ${ok ? 'aceptada' : 'rechazada'}">${(ok ? T.aceptada : T.rechazada)[lang]}</span>
        </div>`;
      }).join('');
}

async function fichar() {
  const r = await fetch('/api/fichar', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      trabajador: ctx.personas[0].id,
      obra: ctx.obra.id,
      tipo: siguienteTipo(),
      lat: escenario.lat,
      lon: escenario.lon,
      precision_m: escenario.precision,
      simulada: escenario.simulada,
      huella: escenario.suHuella ? ctx.personas[0].huella : ctx.personas[1].huella,
      hora_cliente: new Date().toISOString(),
      clave_cliente: crypto.randomUUID(),
    }),
  });
  const d = await r.json();
  if (d.error) return alert(d.error);

  const ok = d.veredicto === 'aceptada';
  const caja = $('veredicto');
  caja.hidden = false;
  caja.className = 'tarjeta veredicto ' + (ok ? 'aceptada' : 'rechazada');
  $('vTitulo').textContent = ok
    ? (lang === 'es' ? 'Marca aceptada' : 'Mark accepted')
    : (lang === 'es' ? 'Marca rechazada' : 'Mark rejected');
  $('vMotivo').textContent = d.motivo
    || (lang === 'es'
        ? `Hora del servidor ${d.hora}, hora de la obra. A ${d.distancia_m} m del centro.`
        : `Server time ${d.hora}, site time. ${d.distancia_m} m from the centre.`);

  pintarMarcas(d.marcas);
  pintarBoton();
}

async function reiniciar() {
  await fetch('/api/reiniciar', { method: 'POST' });
  $('veredicto').hidden = true;
  pintarMarcas([]);
  pintarBoton();
}

(async function arrancar() {
  ctx = await (await fetch('/api/contexto')).json();
  $('quien').textContent = ctx.personas[0].nombre;
  $('obra').firstChild.textContent = ctx.obra.nombre;
  $('obraSub').textContent = `Oakland, CA · ${lang === 'es' ? 'radio' : 'radius'} ${ctx.obra.radio_m} m`;
  const { marcas } = await (await fetch('/api/marcas?trabajador=' + ctx.personas[0].id)).json();
  pintarMarcas(marcas);
  elegir('obra');
})();
