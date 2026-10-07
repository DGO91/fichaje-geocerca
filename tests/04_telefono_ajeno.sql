-- Un companero marca por el, desde su propio telefono.
do $$
declare m marcas%rowtype;
begin
  m := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','salida',
              37.804450, -122.271150, 8, false, 'telefono-de-javier',
              now(), '00000000-0000-0000-0000-0000000000a4');
  assert m.veredicto = 'dispositivo_ajeno',
    'Marcar por otro desde el propio telefono debe rechazarse';
  raise notice 'OK  rechazada: %', m.motivo;
end $$;
