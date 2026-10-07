-- El telefono afirma una hora adelantada dos horas. Se guarda, pero no se
-- usa: la hora buena es la del servidor y el desfase queda a la vista.
do $$
declare m marcas%rowtype;
begin
  m := fichar('33333333-3333-3333-3333-333333333333',
              '22222222-2222-2222-2222-222222222222','entrada',
              37.804420, -122.271080, 7, false, 'telefono-de-ramon',
              now() + interval '2 hours', '00000000-0000-0000-0000-0000000000a6');
  assert m.veredicto = 'aceptada', 'La marca es valida; lo que miente es el reloj';
  assert m.registrada_en < m.hora_cliente, 'La hora del servidor manda';
  assert m.desfase_s < -7000, 'El desfase debe quedar registrado';
  raise notice 'OK  hora del servidor %, el telefono decia %, desfase % s',
    m.registrada_en::time(0), m.hora_cliente::time(0), m.desfase_s;
end $$;
