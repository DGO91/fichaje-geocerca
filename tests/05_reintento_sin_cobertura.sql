-- El movil envia, pierde la red antes de la respuesta, y reintenta con la
-- misma clave. No debe crear una marca nueva.
do $$
declare a marcas%rowtype; b marcas%rowtype; n int;
begin
  a := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','salida',
              37.804500, -122.271000, 9, false, 'telefono-de-ramon',
              now(), '00000000-0000-0000-0000-0000000000a5');
  b := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','salida',
              37.804500, -122.271000, 9, false, 'telefono-de-ramon',
              now(), '00000000-0000-0000-0000-0000000000a5');
  assert a.id = b.id, 'El reintento debe devolver la misma marca';
  select count(*) into n from marcas where clave_cliente = '00000000-0000-0000-0000-0000000000a5';
  assert n = 1, 'No puede haber dos filas para la misma clave de cliente';
  raise notice 'OK  reintento idempotente, una sola marca (id %)', a.id;
end $$;
