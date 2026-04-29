# Retrospectiva y Kaizen — Sprint 1

## Lo que funcionó bien

- Tener `docker compose up --build` funcionando desde el día 1 evitó el problema
  de "en mi máquina sí corre".
- Dividir el backend por módulos (`animals`, `news`, `events`, `registrations`)
  hizo el código fácil de navegar y de asignar tareas.
- El pipeline de CI bloqueó dos PRs con el linter caído antes de mezclar.

## Problema observado

Las pruebas locales del backend corrían contra **SQLite** en memoria
(más rápido), pero al desplegar en Docker con **MySQL 8** aparecieron errores
de tipos:

- El campo `estado` (ENUM) se comportaba distinto.
- Los formatos de fecha se serializaban diferente.

Eso costó aproximadamente medio sprint corregirlo.

## Causa raíz (5 ¿por qué?)

1. **¿Por qué fallaron las pruebas en producción?** Porque la BD real es MySQL.
2. **¿Por qué no se detectó antes?** Porque las pruebas usan SQLite.
3. **¿Por qué se eligió SQLite?** Para que las pruebas sean rápidas.
4. **¿Por qué no se agregó una capa de pruebas con MySQL?** Por simplicidad.
5. **¿Por qué eso fue un error?** Porque las diferencias de tipos
   (ENUM, fechas, charset) sólo se ven contra el motor real.

## Acción concreta para el Sprint 2 (Kaizen)

- [ ] Crear `docker-compose.test.yml` con un servicio `db-test` (MySQL 8).
- [ ] Añadir un job de "integration tests" en GitHub Actions que levante
      ese servicio y ejecute `pytest -m integration` contra él.
- [ ] Marcar las pruebas que requieren MySQL con `@pytest.mark.integration`.
- [ ] Documentar en el README cómo levantar el entorno de pruebas localmente.

## Beneficio esperado

Detectar incompatibilidades de BD **antes** del despliegue, no después.
Estimación: ahorra al menos medio día de debugging en cada sprint.
