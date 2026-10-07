'use strict';

/**
 * Servidor de la demostración.
 *
 * No valida nada por su cuenta: recibe lo que dice el teléfono y se lo pasa
 * a fichar(), que es quien decide. Esa es justamente la idea que demuestra
 * el proyecto, así que el servidor tiene que ser fino a propósito.
 */

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
    || 'postgres://postgres:dev_only_not_a_secret@localhost:55433/fichaje',
  max: 4,
});

const PUERTO = Number(process.env.PORT) || 4100;

function json(res, codigo, cuerpo) {
  const texto = JSON.stringify(cuerpo);
  res.writeHead(codigo, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(texto),
  });
  res.end(texto);
}

async function leerCuerpo(req) {
  const trozos = [];
  for await (const t of req) trozos.push(t);
  return JSON.parse(Buffer.concat(trozos).toString('utf8') || '{}');
}

/** Contexto de la demostración: la obra y los dos trabajadores sembrados. */
async function contexto() {
  const { rows: [obra] } = await pool.query(
    'select id, nombre, lat, lon, radio_m from obras order by nombre limit 1');
  const { rows: personas } = await pool.query(`
    select t.id, t.nombre, t.rol, d.huella
      from trabajadores t
      join dispositivos d on d.trabajador_id = t.id and d.revocado_en is null
     order by (t.rol = 'trabajador') desc, t.nombre`);
  return { obra, personas };
}

/**
 * Las horas se muestran siempre en la zona de la obra, no en la del
 * navegador ni en la del servidor. Un capataz en Oakland y una oficina en
 * Madrid tienen que leer la misma hora para la misma marca.
 */
async function marcasDeHoy(trabajadorId) {
  const { rows } = await pool.query(`
    select m.id, m.tipo, m.veredicto, m.motivo,
           to_char(m.registrada_en at time zone o.zona, 'HH24:MI:SS') as hora,
           round(m.distancia_m)::int as distancia_m
      from marcas m
      join obras o on o.id = m.obra_id
     where m.trabajador_id = $1
       and (m.registrada_en at time zone o.zona)::date
           = (now() at time zone o.zona)::date
     order by m.registrada_en desc
     limit 12`, [trabajadorId]);
  return rows;
}

const rutas = {
  async 'GET /api/contexto'(req, res) {
    json(res, 200, await contexto());
  },

  async 'GET /api/marcas'(req, res, url) {
    const id = url.searchParams.get('trabajador');
    if (!id) return json(res, 400, { error: 'Falta el trabajador' });
    json(res, 200, { marcas: await marcasDeHoy(id) });
  },

  async 'POST /api/fichar'(req, res) {
    const c = await leerCuerpo(req);
    try {
      const { rows: [marca] } = await pool.query(
        `select * from fichar($1,$2,$3::tipo_marca,$4,$5,$6,$7,$8,$9,$10)`,
        [c.trabajador, c.obra, c.tipo, c.lat, c.lon, c.precision_m,
         c.simulada, c.huella, c.hora_cliente, c.clave_cliente]);
      const { rows: [{ hora }] } = await pool.query(
        `select to_char($1::timestamptz at time zone o.zona, 'HH24:MI:SS') as hora
           from obras o where o.id = $2`, [marca.registrada_en, c.obra]);
      json(res, 200, {
        veredicto: marca.veredicto,
        motivo: marca.motivo,
        hora,
        distancia_m: marca.distancia_m === null ? null : Math.round(marca.distancia_m),
        desfase_s: marca.desfase_s,
        marcas: await marcasDeHoy(c.trabajador),
      });
    } catch (err) {
      json(res, 400, { error: err.message });
    }
  },

  async 'POST /api/reiniciar'(req, res) {
    // Deja la jornada en blanco para volver a probar. El disparador impide
    // borrar marcas, así que se desactiva solo para esta operación.
    await pool.query(`
      alter table marcas disable trigger marcas_sin_delete;
      delete from marcas;
      alter table marcas enable trigger marcas_sin_delete;`);
    json(res, 200, { ok: true });
  },
};

const servidor = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const clave = `${req.method} ${url.pathname}`;

  if (rutas[clave]) {
    try { return await rutas[clave](req, res, url); }
    catch (err) { return json(res, 500, { error: err.message }); }
  }

  const fichero = url.pathname === '/' ? 'index.html' : url.pathname.slice(1);
  const destino = path.join(__dirname, 'publico', fichero);
  if (!destino.startsWith(path.join(__dirname, 'publico'))) {
    res.writeHead(403); return res.end('No');
  }
  fs.readFile(destino, (err, datos) => {
    if (err) { res.writeHead(404); return res.end('No encontrado'); }
    const tipo = fichero.endsWith('.css') ? 'text/css'
      : fichero.endsWith('.js') ? 'text/javascript' : 'text/html';
    res.writeHead(200, { 'content-type': `${tipo}; charset=utf-8` });
    res.end(datos);
  });
});

servidor.listen(PUERTO, () => {
  console.log(`Demostración en http://localhost:${PUERTO}`);
});
