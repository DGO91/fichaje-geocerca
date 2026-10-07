-- 003_fichar.sql
--
-- La unica puerta de entrada. El movil no hace INSERT: llama a fichar() y
-- recibe un veredicto. Asi la regla vive en un solo sitio y no puede
-- esquivarse escribiendo directo en la tabla.
--
-- Orden de las comprobaciones, de mas barata a mas cara, y de mas grave a
-- menos: un telefono que miente la ubicacion se rechaza antes de calcular
-- distancias.

create or replace function fichar(
  p_trabajador    uuid,
  p_obra          uuid,
  p_tipo          tipo_marca,
  p_lat           double precision,
  p_lon           double precision,
  p_precision_m   double precision,
  p_simulada      boolean,
  p_huella        text,
  p_hora_cliente  timestamptz,
  p_clave_cliente uuid
) returns marcas
language plpgsql as $$
declare
  v_obra        obras%rowtype;
  v_distancia   double precision;
  v_veredicto   veredicto;
  v_motivo      text;
  v_ya          marcas%rowtype;
  v_ultima      tipo_marca;
  v_fila        marcas%rowtype;
begin
  -- Reintento tras perder cobertura: devuelve la marca que ya existe.
  select * into v_ya from marcas where clave_cliente = p_clave_cliente;
  if found then return v_ya; end if;

  select * into v_obra from obras where id = p_obra;
  if not found then
    raise exception 'La obra no existe' using errcode = 'foreign_key_violation';
  end if;

  v_distancia := earth_distance(ll_to_earth(v_obra.lat, v_obra.lon),
                                ll_to_earth(p_lat, p_lon));

  if p_simulada then
    v_veredicto := 'ubicacion_simulada';
    v_motivo := 'El dispositivo declaró una ubicación simulada.';
  elsif not exists (select 1 from dispositivos
                    where huella = p_huella
                      and trabajador_id = p_trabajador
                      and revocado_en is null) then
    v_veredicto := 'dispositivo_ajeno';
    v_motivo := 'El teléfono no está dado de alta para este trabajador.';
  elsif p_precision_m > 75 then
    v_veredicto := 'precision_insuficiente';
    v_motivo := format('Precisión de %s m, por encima del límite de 75 m.',
                       round(p_precision_m));
  elsif v_distancia > v_obra.radio_m then
    v_veredicto := 'fuera_de_perimetro';
    v_motivo := format('A %s m del centro, fuera del radio de %s m.',
                       round(v_distancia), v_obra.radio_m);
  else
    -- Coherencia de la jornada: no se entra dos veces sin salir.
    select tipo into v_ultima from marcas
     where trabajador_id = p_trabajador and veredicto = 'aceptada'
     order by registrada_en desc limit 1;

    if p_tipo = 'entrada' and v_ultima = 'entrada' then
      v_veredicto := 'anulada';
      v_motivo := 'Ya hay una entrada abierta sin su salida.';
    elsif p_tipo = 'salida' and (v_ultima is null or v_ultima = 'salida') then
      v_veredicto := 'anulada';
      v_motivo := 'No hay ninguna entrada abierta que cerrar.';
    else
      v_veredicto := 'aceptada';
    end if;
  end if;

  insert into marcas (trabajador_id, obra_id, tipo, hora_cliente, lat, lon,
                      precision_m, ubicacion_simulada, huella_dispositivo,
                      veredicto, distancia_m, motivo, clave_cliente)
  values (p_trabajador, p_obra, p_tipo, p_hora_cliente, p_lat, p_lon,
          p_precision_m, p_simulada, p_huella,
          v_veredicto, v_distancia, v_motivo, p_clave_cliente)
  returning * into v_fila;

  return v_fila;
end $$;

-- Horas trabajadas, contando solo marcas aceptadas y restando descansos.
create or replace function horas_del_dia(p_trabajador uuid, p_dia date)
returns interval language sql stable as $$
  with m as (
    select tipo, registrada_en from marcas
     where trabajador_id = p_trabajador
       and veredicto = 'aceptada'
       and registrada_en::date = p_dia
     order by registrada_en
  ), pares as (
    select tipo, registrada_en,
           lead(registrada_en) over (order by registrada_en) as siguiente
      from m
  )
  select coalesce(
    sum(siguiente - registrada_en) filter (where tipo = 'entrada')
    - coalesce(sum(siguiente - registrada_en) filter (where tipo = 'inicio_descanso'),
               interval '0'),
    interval '0')
  from pares;
$$;
