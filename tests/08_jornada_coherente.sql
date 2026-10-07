-- No se entra dos veces sin salir, ni se sale sin haber entrado.
do $$
declare m marcas%rowtype;
begin
  m := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','entrada',
              37.804430, -122.271090, 6, false, 'telefono-de-ramon',
              now(), '00000000-0000-0000-0000-0000000000a8');
  assert m.veredicto = 'anulada', 'Una segunda entrada sin salida debe rechazarse';
  raise notice 'OK  rechazada: %', m.motivo;
end $$;
