# Definición de Terminado (DoD)

Una historia se considera **terminada** cuando cumple **todos** estos criterios:

1. El código está mezclado en `main` y revisado por al menos un compañero
   (PR aprobado).
2. Tiene al menos una prueba automatizada (unitaria o de componente).
3. Pasa el pipeline de CI completo: **lint + tests + build**.
4. Está documentada en el README o en `docs/`.
5. Funciona ejecutando `docker compose up --build` desde un entorno limpio.
6. Cumple los criterios de aceptación definidos en la historia.

## Notas

- Si una historia se cierra sin cumplir alguno de estos puntos, se debe crear
  una *deuda técnica* en el backlog y aceptarla explícitamente en el daily.
- El criterio 5 evita el clásico "en mi máquina sí corre".
