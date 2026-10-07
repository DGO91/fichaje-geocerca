-- Ni el administrador puede reescribir una marca. Una correccion es una
-- fila nueva que anula la anterior.
do $$
declare bloqueado boolean := false; correccion marcas%rowtype; id_original bigint;
begin
  select id into id_original from marcas where veredicto = 'aceptada' order by id limit 1;

  begin
    update marcas set registrada_en = now() where id = id_original;
  exception when integrity_constraint_violation then bloqueado := true;
  end;
  assert bloqueado, 'Un UPDATE sobre marcas debe fallar';

  bloqueado := false;
  begin
    delete from marcas where id = id_original;
  exception when integrity_constraint_violation then bloqueado := true;
  end;
  assert bloqueado, 'Un DELETE sobre marcas debe fallar';

  insert into marcas (trabajador_id, obra_id, tipo, lat, lon, precision_m,
                      huella_dispositivo, veredicto, anula_a, motivo, clave_cliente)
  select trabajador_id, obra_id, tipo, lat, lon, precision_m, huella_dispositivo,
         'anulada', id, 'Corregida por el mayordomo: el trabajador entro 10 min antes.',
         gen_random_uuid()
    from marcas where id = id_original
  returning * into correccion;

  assert correccion.anula_a = id_original, 'La correccion debe apuntar a la marca original';
  raise notice 'OK  update y delete bloqueados; correccion % anula a %',
    correccion.id, id_original;
end $$;
