-- Una entrada legitima, a 30 m del centro de la obra.
do $$
declare m marcas%rowtype;
begin
  m := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','entrada',
              37.804650, -122.271100, 12, false, 'telefono-de-ramon',
              now(), '00000000-0000-0000-0000-0000000000a1');
  assert m.veredicto = 'aceptada', 'Una entrada dentro del perimetro debe aceptarse';
  assert m.distancia_m < 120, 'La distancia debe quedar dentro del radio';
  raise notice 'OK  entrada aceptada a % m', round(m.distancia_m);
end $$;
