#!/usr/bin/env python3
"""
Genera las pantallas del esqueleto.

Todas comparten cabecera, navegacion, hoja de estilo y mecanismo de idioma,
asi que se escriben desde una plantilla unica. Si el ritmo o los radios
cambian, cambian en los ocho sitios a la vez.
"""
import pathlib

SALIDA = pathlib.Path(__file__).parent / "publico"

NAV = [
    ("index.html",      "Fichar",     "Clock in"),
    ("obras.html",      "Obras",      "Jobs"),
    ("seguridad.html",  "Seguridad",  "Safety"),
    ("cyb.html",        "CYB",        "CYB"),
    ("reporte.html",    "Reporte",    "Report"),
    ("correo.html",     "Correo",     "Email"),
    ("formacion.html",  "Formación",  "Training"),
]

def t(es, en):
    """Texto con sus dos idiomas, listo para el conmutador."""
    return f'<span data-es="{es}" data-en="{en}">{es}</span>'

def pagina(fichero, titulo_es, titulo_en, cuerpo, muestra=True):
    nav = "".join(
        f'<a href="{f}" class="{"on" if f == fichero else ""}" '
        f'data-es="{e}" data-en="{i}">{e}</a>'
        for f, e, i in NAV)

    aviso = ("""
 <p class="muestra" data-es="Pantalla de ejemplo. Los datos son de muestra; el fichaje es el único que consulta la base de datos real."
    data-en="Sample screen. The data is illustrative; clock-in is the only one that queries the real database.">Pantalla de ejemplo. Los datos son de muestra; el fichaje es el único que consulta la base de datos real.</p>"""
        if muestra else "")

    html = f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{titulo_es} · Golden State</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="estilo.css"/>
</head><body>

<div class="telefono">

 <header>
  <div>
   <div class="quien">Javier Mena</div>
   <div class="rol" data-es="Mayordomo · Broadway Tower" data-en="Foreman · Broadway Tower">Mayordomo · Broadway Tower</div>
  </div>
  <span class="idioma">
   <button class="on" onclick="idioma('es')">ES</button>
   <button onclick="idioma('en')">EN</button>
  </span>
 </header>

 <nav class="menu">{nav}</nav>

{cuerpo}
{aviso}
</div>

<script src="idioma.js"></script>
</body></html>
"""
    (SALIDA / fichero).write_text(html)
    print("  ", fichero)

# ───────────────────────────────────────────────── Obras
obras = [
    ("Broadway Tower", "Oakland, CA", "8 en obra", "activa", "al día"),
    ("Mission Bay Lot 4", "San Francisco, CA", "5 en obra", "activa", "pendiente"),
    ("Alameda Logistics", "Alameda, CA", "0 en obra", "parada", "al día"),
]
filas = "".join(f"""
   <a class="fila" href="obra.html">
    <div><div class="n">{n}</div><div class="s">{d} · {g}</div></div>
    <div class="der">
     <span class="chip {'chip-ok' if r=='al día' else 'chip-aviso'}"
      data-es="{'reporte al día' if r=='al día' else 'reporte pendiente'}"
      data-en="{'report up to date' if r=='al día' else 'report pending'}">{'reporte al día' if r=='al día' else 'reporte pendiente'}</span>
    </div>
   </a>""" for n, d, g, e, r in obras)

pagina("obras.html", "Obras", "Jobs", f"""
 <section class="tarjeta">
  <div class="rotulo" data-es="Archivo por trabajo" data-en="File per job">Archivo por trabajo</div>
  <div class="lista">{filas}</div>
 </section>

 <button class="fichar secundario" data-es="Crear obra" data-en="New job">Crear obra</button>
""")

# ───────────────────────────────────────────────── Ficha de obra
fotos = "".join(f'<div class="foto f{i}"><span>{h}</span></div>'
                for i, h in enumerate(["07:12", "09:40", "11:05", "13:22", "15:48", "16:30"], 1))

pagina("obra.html", "Broadway Tower", "Broadway Tower", f"""
 <div class="columnas">
 <div class="col">

 <section class="tarjeta">
  <div class="rotulo" data-es="Obra" data-en="Job">Obra</div>
  <div class="obra">Broadway Tower<small>1200 Broadway, Oakland, CA · {t("cuadrilla de 8","crew of 8")}</small></div>
  <div class="datos">
   <div>{t("Contratista","General contractor")}<b>Swinerton</b></div>
   <div>{t("Vertido previsto","Pour scheduled")}<b>12 nov</b></div>
   <div>{t("Tonelaje colocado","Tonnage placed")}<b class="num">18,4 t</b></div>
  </div>
 </section>

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Seguridad de hoy" data-en="Today's safety">Seguridad de hoy</div></div>
  <div class="chips">
   <span class="chip chip-ok">{t("JHA firmado","JHA signed")}</span>
   <span class="chip chip-aviso">{t("Montacargas pendiente","Forklift pending")}</span>
   <span class="chip chip-ok">{t("Tailgate hecho","Tailgate done")}</span>
  </div>
 </section>

 </div>
 <div class="col">

 <section class="tarjeta">
  <div class="chead">
   <div class="rotulo" data-es="Progreso de hoy" data-en="Today's progress">Progreso de hoy</div>
   <span class="apunte">6 {t("fotos","photos")}</span>
  </div>
  <div class="galeria">{fotos}</div>
  <button class="fichar" style="margin-top:14px" data-es="Añadir foto" data-en="Add photo">Añadir foto</button>
 </section>

 <section class="tarjeta">
  <div class="rotulo" data-es="Documentos" data-en="Documents">Documentos</div>
  <div class="lista">
   <div class="fila"><div><div class="n">{t("Planos estructurales S-204","Structural drawings S-204")}</div>
     <div class="s">PDF · 4,2 MB · {t("rev. C","rev. C")}</div></div></div>
   <div class="fila"><div><div class="n">{t("Permiso de vertido","Pour permit")}</div>
     <div class="s">PDF · 320 KB</div></div></div>
  </div>
 </section>

 </div>
 </div>
""")

# ───────────────────────────────────────────────── Seguridad diaria
jha = [
    ("Descarga de varilla con grúa", "Unloading rebar with crane",
     "Carga suspendida sobre la cuadrilla", "Suspended load over the crew",
     "Zona acordonada y señalero asignado", "Area roped off, signaller assigned"),
    ("Corte y doblado", "Cutting and bending",
     "Proyección de partículas", "Flying particles",
     "Gafas y pantalla facial", "Goggles and face shield"),
    ("Atado en altura", "Tying at height",
     "Caída a distinto nivel", "Fall from height",
     "Arnés anclado a línea de vida", "Harness anchored to lifeline"),
]
pasos = "".join(f"""
   <div class="paso">
    <div class="n">{t(a,b)}</div>
    <div class="par"><span class="et">{t("Riesgo","Hazard")}</span><span>{t(c,d)}</span></div>
    <div class="par"><span class="et">{t("Control","Control")}</span><span>{t(e,f)}</span></div>
   </div>""" for a,b,c,d,e,f in jha)

monta = [("Niveles de aceite y fugas","Oil levels and leaks",True),
         ("Horquillas y cadena","Forks and chain",True),
         ("Frenos y claxon","Brakes and horn",True),
         ("Neumáticos","Tyres",False),
         ("Extintor y cinturón","Extinguisher and belt",True)]
items = "".join(f"""
   <label class="check">
    <input type="checkbox" {'checked' if ok else ''}/>
    <span>{t(a,b)}</span>
   </label>""" for a,b,ok in monta)

pagina("seguridad.html", "Seguridad", "Safety", f"""
 <div class="columnas">
 <div class="col">

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Análisis de seguridad (JHA)" data-en="Job hazard analysis (JHA)">Análisis de seguridad (JHA)</div>
   <span class="chip chip-ok">{t("firmado 06:52","signed 06:52")}</span></div>
  {pasos}
  <div class="firma">{t("Firmado por Javier Mena y 8 miembros de la cuadrilla","Signed by Javier Mena and 8 crew members")}</div>
 </section>

 </div>
 <div class="col">

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Inspección de montacargas" data-en="Forklift inspection">Inspección de montacargas</div>
   <span class="chip chip-aviso">{t("pendiente","pending")}</span></div>
  {items}
  <button class="fichar" style="margin-top:16px" data-es="Firmar inspección" data-en="Sign inspection">Firmar inspección</button>
 </section>

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Reunión de seguridad" data-en="Tailgate meeting">Reunión de seguridad</div>
   <span class="chip chip-ok">{t("hecha 07:05","done 07:05")}</span></div>
  <div class="datos">
   <div>{t("Tema","Topic")}<b>{t("Prevención de golpes de calor","Heat illness prevention")}</b></div>
   <div>{t("Duración","Duration")}<b class="num">11 min</b></div>
   <div>{t("Asistentes","Attendees")}<b class="num">8 de 8</b></div>
  </div>
 </section>

 </div>
 </div>
""")

# ───────────────────────────────────────────────── Registro CYB
cyb = [
    ("07:40","Replanteo de columnas C4 a C9","Layout of columns C4 to C9","foto","0:00"),
    ("09:15","El contratista cambia la secuencia de vertido","GC changes the pour sequence","audio","1:24"),
    ("11:02","Varilla #8 llega doblada de fábrica","#8 bar arrives bent from the mill","foto","0:00"),
    ("13:30","Espera de 40 min por la bomba","40 min wait for the pump","audio","0:48"),
]
entradas = "".join(f"""
   <div class="fila cyb">
    <div class="hora num">{h}</div>
    <div class="cuerpo">
     <div class="n">{t(a,b)}</div>
     <div class="s">{('Nota de audio · ' + d) if k=='audio' else 'Fotografía'}</div>
    </div>
    <div class="marca-tipo">{'audio' if k=='audio' else 'foto'}</div>
   </div>""" for h,a,b,k,d in cyb)

pagina("cyb.html", "Registro CYB", "CYB log", f"""
 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Registro del día" data-en="Today's log">Registro del día</div>
   <span class="apunte">4 {t("entradas","entries")}</span></div>
  <div class="lista">{entradas}</div>
 </section>

 <section class="tarjeta">
  <div class="rotulo" data-es="Nueva entrada" data-en="New entry">Nueva entrada</div>
  <p class="s" style="margin-top:8px">{t("Cada entrada guarda su hora exacta en el momento de crearla.","Every entry stores its exact time the moment it is created.")}</p>
  <div class="acciones">
   <button class="accion"><b>{t("Foto","Photo")}</b></button>
   <button class="accion"><b>{t("Audio","Audio")}</b></button>
   <button class="accion"><b>{t("Nota","Note")}</b></button>
  </div>
 </section>
""")

# ───────────────────────────────────────────────── Reporte diario
pagina("reporte.html", "Reporte diario", "Daily report", f"""
 <div class="columnas">
 <div class="col">

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Reporte del 7 de octubre" data-en="Report for 7 October">Reporte del 7 de octubre</div>
   <span class="chip chip-aviso">{t("borrador","draft")}</span></div>
  <p class="s" style="margin-bottom:14px">{t("Lo que ya se sabe viene relleno. El mayordomo solo escribe lo que falta.","What is already known comes pre-filled. The foreman only writes what is missing.")}</p>
  <div class="datos">
   <div>{t("Obra","Job")}<b>Broadway Tower</b></div>
   <div>{t("Cuadrilla","Crew")}<b class="num">8</b></div>
   <div>{t("Horas de la cuadrilla","Crew hours")}<b class="num">62,5</b></div>
   <div>{t("Tonelaje colocado","Tonnage placed")}<b class="num">18,4 t</b></div>
   <div>{t("Entradas CYB","CYB entries")}<b class="num">4</b></div>
  </div>
 </section>

 </div>
 <div class="col">

 <section class="tarjeta">
  <div class="rotulo" data-es="Trabajo realizado" data-en="Work completed">Trabajo realizado</div>
  <div class="campo">{t("Atado de columnas C4 a C9. Empezada la losa del nivel 3 por el lado este.","Tied columns C4 to C9. Started level 3 deck on the east side.")}</div>
 </section>

 <section class="tarjeta">
  <div class="rotulo" data-es="Retrasos e incidencias" data-en="Delays and issues">Retrasos e incidencias</div>
  <div class="campo">{t("40 minutos de espera por la bomba. Varilla #8 recibida doblada: reclamada al proveedor.","40 minute wait for the pump. #8 bar received bent: claimed to the supplier.")}</div>
 </section>

 <section class="tarjeta">
  <div class="rotulo" data-es="Mañana" data-en="Tomorrow">Mañana</div>
  <div class="campo">{t("Cerrar la losa del nivel 3. Se necesitan dos atadores más.","Close level 3 deck. Two more tiers needed.")}</div>
 </section>

 <button class="fichar" data-es="Enviar reporte" data-en="Send report">Enviar reporte</button>

 </div>
 </div>
""")

# ───────────────────────────────────────────────── Asistente de correo
pagina("correo.html", "Correo", "Email", f"""
 <div class="columnas">
 <div class="col">

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Recibido" data-en="Received">Recibido</div>
   <span class="apunte">Swinerton · 14:02</span></div>
  <div class="correo">We need the rebar inspection signed off before Thursday's pour. Can your crew be ready by Wednesday noon? Also confirm the tonnage placed this week.</div>
  <div class="traduccion">
   <div class="rotulo" data-es="En español" data-en="In Spanish">En español</div>
   <p>{t("Necesitamos la inspección de varilla firmada antes del vertido del jueves. ¿Puede estar lista tu cuadrilla el miércoles a mediodía? Confirma también el tonelaje colocado esta semana.","We need the rebar inspection signed off before Thursday's pour. Can your crew be ready by Wednesday noon? Also confirm the tonnage placed this week.")}</p>
  </div>
 </section>

 </div>
 <div class="col">

 <section class="tarjeta">
  <div class="rotulo" data-es="Escribe en español" data-en="Write in Spanish">Escribe en español</div>
  <div class="campo">{t("Sí, el miércoles a las 11 está lista. Esta semana llevamos 18,4 toneladas. La inspección la firmo mañana por la mañana.","Yes, ready Wednesday at 11. We have placed 18.4 tonnes this week. I will sign the inspection tomorrow morning.")}</div>
  <div class="chips" style="margin-top:12px">
   <span class="chip">{t("Tono directo","Direct tone")}</span>
   <span class="chip chip-apagado">{t("Tono formal","Formal tone")}</span>
  </div>
 </section>

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Borrador en inglés" data-en="English draft">Borrador en inglés</div>
   <span class="apunte">{t("revisa antes de enviar","review before sending")}</span></div>
  <div class="correo">Yes, we will be ready Wednesday at 11:00. We have placed 18.4 tons this week. I will sign off the rebar inspection tomorrow morning.</div>
  <button class="fichar" style="margin-top:14px" data-es="Enviar" data-en="Send">Enviar</button>
 </section>

 </div>
 </div>
""")

# ───────────────────────────────────────────────── Formación
MODULOS = [
 ("Lectura de planos","Reading drawings",100),
 ("Comparación con planos estructurales","Comparing against structural drawings",100),
 ("Planificación de cargas de trabajo","Planning workloads",60),
 ("Evitar la inactividad del equipo","Avoiding crew downtime",60),
 ("Control de calidad antes del vertido","QC before each pour",40),
 ("Relación con el contratista","Working with the GC",40),
 ("Cálculo de coste de cuadrilla","Crew cost",0),
 ("Tag work y time & material","Tag work and T&M",0),
 ("Accesorios y cables postensados","Accessories and PT cables",0),
 ("Planificación de mano de obra","Manpower planning",0),
 ("Cálculo de tarifas","Rates",0),
 ("Codificación por colores de la varilla","Rebar colour coding",0),
 ("Aparejos y equipo de izado","Rigging and picks",0),
 ("Gestión del tiempo personal","Personal time management",0),
 ("Cálculo de tonelaje","Tonnage calculation",0),
 ("Seguridad en el sitio","Jobsite safety",0),
 ("Tabla de pesos de varilla","Rebar weight table",0),
 ("Tolerancias ACI 117","ACI 117 tolerances",0),
 ("Prevención de golpes de calor","Heat illness prevention",0),
 ("Prevención del acoso sexual","Sexual harassment prevention",0),
 ("Prevención del abuso de sustancias","Substance abuse prevention",0),
]
tarjetas = "".join(f"""
  <div class="modulo">
   <div class="n">{t(a,b)}</div>
   <div class="bar"><i style="width:{p}%"></i></div>
   <div class="s">{'completado' if p==100 else (str(p)+'% ' if p else 'sin empezar')}</div>
  </div>""" for a,b,p in MODULOS)

pagina("formacion.html", "Formación", "Training", f"""
 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Módulos para mayordomos" data-en="Foreman training">Módulos para mayordomos</div>
   <span class="apunte">21 {t("temas","topics")}</span></div>
  <p class="s" style="margin-bottom:16px">{t("Cada módulo está en español e inglés, y guarda el avance por persona.","Every module is in Spanish and English, and tracks progress per person.")}</p>
  <div class="modulos">{tarjetas}</div>
 </section>

 <section class="tarjeta">
  <div class="chead"><div class="rotulo" data-es="Lector de planos con IA" data-en="AI drawing reader">Lector de planos con IA</div>
   <span class="chip chip-apagado">{t("fuera de la fase 1","out of phase 1")}</span></div>
  <p class="s">{t("Se estudia aparte: leer un plano estructural y compararlo con lo ejecutado es un desarrollo propio, no un módulo más.","Scoped separately: reading a structural drawing and comparing it with what was built is its own product, not one more module.")}</p>
 </section>
""")
