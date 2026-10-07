# Fichaje con geocerca

Núcleo de datos para control de asistencia en obra. Demuestra, con pruebas
que se ejecutan, que un fichaje no se puede falsear desde el teléfono.

```bash
make test
```

Levanta Postgres en Docker, aplica las migraciones y corre las ocho
comprobaciones. Se puede ejecutar las veces que haga falta: una tabla
`schema_migrations` lleva la cuenta de lo aplicado, de modo que cada
migración corre una sola vez y la segunda ejecución no produce errores.

## La aplicación de prueba

```bash
make app
```

Levanta la base, aplica las migraciones y sirve una pantalla en
`http://localhost:4100`. No es una maqueta: cada botón llama a `fichar()`
y lo que aparece en el veredicto es lo que devuelve la base de datos.

Cinco situaciones para probar, sin mover el teléfono de sitio:

| Situación | Lo que ocurre |
|---|---|
| Estoy en la obra | Se acepta, a 28 m del centro |
| Desde casa | Se rechaza, a 1514 m |
| Con ubicación simulada | Se rechaza, aunque las coordenadas sean perfectas |
| Desde el teléfono de un compañero | Se rechaza, el aparato no es suyo |
| Con mala señal | Se rechaza por precisión insuficiente |

Las horas se muestran en la zona de la obra, no en la del navegador: un
capataz en Oakland y una oficina en Madrid tienen que leer la misma hora
para la misma marca.

## La idea

El teléfono siempre puede mentir: la hora se cambia en ajustes, las
coordenadas se simulan con una app gratuita, y el aparato se presta.

Lo que no se puede manipular es lo que la base de datos acepta. Por eso
el móvil no escribe en la tabla: llama a una función y recibe un
veredicto.

## Lo que se comprueba

| Prueba | Qué demuestra |
|---|---|
| `01_dentro_del_perimetro` | Una entrada legítima a 28 m se acepta |
| `02_fuera_del_perimetro` | Fichar desde casa, a 1514 m, se rechaza |
| `03_ubicacion_simulada` | Coordenadas perfectas pero falsas se rechazan |
| `04_telefono_ajeno` | Marcar por un compañero desde otro teléfono se rechaza |
| `05_reintento_sin_cobertura` | El reintento tras perder red no duplica la marca |
| `06_hora_del_servidor` | Un reloj adelantado 2 h no altera la hora registrada |
| `07_solo_anadir` | Ni UPDATE ni DELETE sobre una marca; la corrección es fila nueva |
| `08_jornada_coherente` | No se entra dos veces sin salir |

## Las cuatro decisiones de diseño

**La hora la pone el servidor.** La del teléfono se guarda aparte y se
calcula el desfase: un reloj adelantado dos horas queda a la vista sin
contaminar el cómputo.

**El perímetro vive en la base.** Si viviera en el cliente, cambiarlo
sería editar un fichero. La distancia se calcula con `earthdistance`
contra el punto y el radio de la obra.

**La tabla es solo-añadir.** Un disparador bloquea UPDATE y DELETE,
incluso para el administrador. Corregir una marca es insertar otra con
`anula_a` apuntando a la original, así el histórico sigue siendo
histórico.

**Las migraciones se pueden repetir.** Versionada no es lo mismo que
aplicada, y descubrirlo tarde cuesta días. El registro de migraciones
evita que un despliegue repetido rompa una base que ya está en
producción.

**El identificador lo genera el móvil.** `clave_cliente` es única, de
modo que un reintento después de perder cobertura devuelve la marca que
ya existe en vez de crear otra. En una obra sin señal eso no es un
detalle: es la diferencia entre una jornada bien contada y una
duplicada.

## Lo que un rechazo guarda

Una marca rechazada **no se descarta**. Se guarda con su veredicto, su
distancia y su motivo, porque el patrón importa: tres intentos de
ubicación simulada en una semana es información para el mayordomo.

## Qué no cubre

Es el núcleo de datos, no la aplicación. No incluye la interfaz móvil, el
alta de dispositivos por el administrador, ni la atestación del sistema
operativo (Play Integrity y App Attest), que es la capa que confirma que
el aparato no está manipulado. Esas van en el proyecto, no en la
demostración.

`app-pantalla.png` y `pantalla-fichaje.png` muestran cómo se ve en el
teléfono. Los textos de rechazo son los que devuelve la base de datos, no
maquetación.

## Cómo trabajo

Uso Claude Code como herramienta de desarrollo. Las decisiones de
arquitectura son mías: qué se valida en el servidor y qué en el cliente,
por qué la tabla es solo-añadir, dónde vive el perímetro y qué pasa con
una marca rechazada. Y respondo de cada una.

Las pruebas de este repositorio existen precisamente por eso. No pido que
se confíe en el código ni en quién lo escribió: se clona, se ejecuta
`make test` y se ve qué se sostiene.
