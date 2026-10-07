PSQL = docker exec -i fichaje_demo_db psql -U postgres -d fichaje -v ON_ERROR_STOP=1

up:
	@docker compose up -d >/dev/null 2>&1
	@until docker exec fichaje_demo_db psql -U postgres -d fichaje -c 'select 1' >/dev/null 2>&1; do sleep 1; done

down:
	@docker compose down -v >/dev/null 2>&1

migrate: up
	@$(PSQL) -q -c "set client_min_messages = warning; create table if not exists schema_migrations (version text primary key, applied_at timestamptz not null default now())"
	@for f in migrations/*.sql; do \
	  v=$$(basename $$f .sql); \
	  n=$$($(PSQL) -tA -c "select count(*) from schema_migrations where version='$$v'"); \
	  if [ "$$n" = "0" ]; then printf '  aplicando  %s\n' "$$v"; \
	    $(PSQL) -q -f - < $$f && $(PSQL) -q -c "insert into schema_migrations (version) values ('$$v')"; \
	  else printf '  ya estaba  %s\n' "$$v"; fi; done

test: migrate
	@for f in tests/*.sql; do printf '\n== %s\n' "$$(basename $$f)"; $(PSQL) -q -f - < $$f; done
	@printf '\nTodas las invariantes se sostienen.\n'

psql: up
	@docker exec -it fichaje_demo_db psql -U postgres -d fichaje

.PHONY: up down migrate test psql
