truncate marcas, dispositivos, trabajadores, obras, empresas restart identity cascade;

insert into empresas (id, nombre) values
  ('11111111-1111-1111-1111-111111111111','Golden State Reinforcing');

-- Obra en Oakland, radio de 120 m.
insert into obras (id, empresa_id, nombre, lat, lon, radio_m) values
  ('22222222-2222-2222-2222-222222222222','11111111-1111-1111-1111-111111111111',
   'Broadway Tower', 37.804400, -122.271100, 120);

insert into trabajadores (id, empresa_id, nombre, rol) values
  ('33333333-3333-3333-3333-333333333333','11111111-1111-1111-1111-111111111111','Ramon Ortega','trabajador'),
  ('44444444-4444-4444-4444-444444444444','11111111-1111-1111-1111-111111111111','Javier Mena','mayordomo');

insert into dispositivos (trabajador_id, huella) values
  ('33333333-3333-3333-3333-333333333333','telefono-de-ramon'),
  ('44444444-4444-4444-4444-444444444444','telefono-de-javier');
