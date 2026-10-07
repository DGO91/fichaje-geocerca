-- El trabajador ficha desde casa, a mas de un kilometro.
do $$
declare m marcas%rowtype;
begin
  m := fichar('44444444-4444-4444-4444-444444444444',
              '22222222-2222-2222-2222-222222222222','entrada',
              37.818000, -122.271100, 10, false, 'telefono-de-javier',
              now(), '00000000-0000-0000-0000-0000000000a2');
  assert m.veredicto = 'fuera_de_perimetro', 'Debe rechazarse por distancia';
  raise notice 'OK  rechazada: %', m.motivo;
end $$;
