-- 001_obras_y_personas.sql
--
-- Empresa, obras y trabajadores. Cada obra lleva su perimetro: un punto y
-- un radio en metros. El perimetro vive en la base, no en el telefono: si
-- viviera en el cliente, cambiarlo seria tan facil como editar un fichero.

create extension if not exists cube;
create extension if not exists earthdistance;

create table empresas (
  id          uuid primary key default gen_random_uuid(),
  nombre      text not null
);

create table obras (
  id          uuid primary key default gen_random_uuid(),
  empresa_id  uuid not null references empresas(id),
  nombre      text not null,
  lat         double precision not null,
  lon         double precision not null,
  radio_m     integer not null check (radio_m between 25 and 2000),
  zona        text not null default 'America/Los_Angeles'
);

create table trabajadores (
  id          uuid primary key default gen_random_uuid(),
  empresa_id  uuid not null references empresas(id),
  nombre      text not null,
  rol         text not null check (rol in ('trabajador','mayordomo','admin'))
);

-- Un dispositivo queda ligado a un trabajador. Fichar desde un telefono
-- que no es el suyo es el fraude mas comun: uno marca por todos.
create table dispositivos (
  id              uuid primary key default gen_random_uuid(),
  trabajador_id   uuid not null references trabajadores(id),
  huella          text not null,
  alta_en         timestamptz not null default now(),
  revocado_en     timestamptz,
  unique (huella)
);

create index on obras (empresa_id);
create index on trabajadores (empresa_id);
create index on dispositivos (trabajador_id);
