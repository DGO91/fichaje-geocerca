-- 002_marcas_solo_anadir.sql
--
-- El registro de fichajes. Tres decisiones que lo sostienen todo:
--
-- 1. La hora la pone el servidor. La del telefono se guarda, pero solo
--    como dato a contrastar: un desfase grande es una senal, no una hora.
-- 2. La tabla es solo-anadir. Una correccion es una marca nueva que anula
--    la anterior, nunca un UPDATE. Lo que paso, paso.
-- 3. La validacion del perimetro ocurre aqui dentro. El telefono manda
--    coordenadas; quien decide si valen es la base.

create type tipo_marca as enum ('entrada','salida','inicio_descanso','fin_descanso');
create type veredicto  as enum ('aceptada','fuera_de_perimetro','ubicacion_simulada',
                                'dispositivo_ajeno','precision_insuficiente','anulada');

create table marcas (
  id              bigserial primary key,
  trabajador_id   uuid not null references trabajadores(id),
  obra_id         uuid not null references obras(id),
  tipo            tipo_marca not null,

  -- Hora del servidor. Sin valor por defecto que venga de fuera.
  registrada_en   timestamptz not null default now(),
  -- Lo que afirmaba el telefono, para contrastar.
  hora_cliente    timestamptz,
  desfase_s       integer generated always as
                    (extract(epoch from (registrada_en - hora_cliente))::integer) stored,

  lat             double precision not null,
  lon             double precision not null,
  precision_m     double precision not null,
  ubicacion_simulada boolean not null default false,
  huella_dispositivo text not null,

  veredicto       veredicto not null,
  distancia_m     double precision,
  anula_a         bigint references marcas(id),
  motivo          text,

  -- Idempotencia: el movil genera el identificador antes de enviar, asi un
  -- reintento tras perder cobertura no crea una marca nueva.
  clave_cliente   uuid not null,
  unique (clave_cliente)
);

create index on marcas (trabajador_id, registrada_en desc);
create index on marcas (obra_id, registrada_en desc);

-- Nadie modifica ni borra una marca. Una correccion entra como fila nueva
-- con anula_a apuntando a la anterior.
create or replace function marcas_solo_anadir() returns trigger
language plpgsql as $$
begin
  raise exception 'Las marcas no se modifican ni se borran. Registra una correccion con anula_a.'
    using errcode = 'integrity_constraint_violation';
end $$;

create trigger marcas_sin_update before update on marcas
  for each row execute function marcas_solo_anadir();
create trigger marcas_sin_delete before delete on marcas
  for each row execute function marcas_solo_anadir();
