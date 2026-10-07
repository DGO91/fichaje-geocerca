-- Coordenadas perfectas, pero el sistema operativo delata que son falsas.
do $$
declare m marcas%rowtype;
begin
  m := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','salida',
              37.804400, -122.271100, 5, true, 'telefono-de-ramon',
              now(), '00000000-0000-0000-0000-0000000000a3');
  assert m.veredicto = 'ubicacion_simulada',
    'Una ubicacion simulada se rechaza aunque caiga en el centro exacto';
  raise notice 'OK  rechazada: %', m.motivo;
end $$;
