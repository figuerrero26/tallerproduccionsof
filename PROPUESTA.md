# Propuesta de Solución — Sistema Web Fundación de Rescate Animal

**Curso:** Producción de Software
**Tipo de entregable:** Propuesta práctica (laboratorio)
**Stack:** React (frontend) · FastAPI (backend) · MySQL (BD)

---

## 1. Contexto

La fundación gestiona la información de manera manual (redes sociales + hojas de
cálculo), lo que dificulta el seguimiento de animales, registros de interesados y
comunicación de eventos. Se necesita un sistema web sencillo que centralice:

- Animales en adopción
- Noticias institucionales
- Eventos / jornadas de adopción
- Registros de personas interesadas

El sistema debe ser fácil de mantener, dockerizado y con pruebas automatizadas.

---

## 2. Arquitectura propuesta

### Decisión: **Monolito modular**

Se descarta microservicios porque añadiría complejidad sin beneficios reales para
este tamaño de problema.

| Criterio | Monolito modular ✅ | Microservicios ❌ |
|---|---|---|
| Tamaño del problema | 4 módulos pequeños y muy relacionados | Pensados para sistemas grandes |
| Equipo | Pocos estudiantes | Necesita varios equipos |
| Despliegue | Un solo contenedor backend | N contenedores + orquestación |
| Curva de aprendizaje | Baja | Alta (gateway, service discovery, colas) |
| Costos de operación | Mínimos | Altos |

Como los módulos comparten datos (un *registro* apunta a un *animal* y posiblemente
a un *evento*), conviene tener una única base y un único backend dividido por
módulos internos: `animals`, `news`, `events`, `registrations`.

### Diagrama lógico

```
   [ Navegador ]
        │ HTTPS
        ▼
  [ Frontend React ] ──── llamadas REST ────► [ Backend FastAPI ]
                                                       │
                                                       ▼
                                                 [ MySQL 8 ]
```

Los tres componentes corren como contenedores Docker en la misma red.

---

## 3. Estructura del proyecto

```
talleranimales/
├── backend/
│   ├── app/
│   │   ├── main.py              # punto de entrada FastAPI
│   │   ├── database.py          # conexión a MySQL (SQLAlchemy)
│   │   ├── models/              # modelos ORM
│   │   │   ├── animal.py
│   │   │   ├── news.py
│   │   │   ├── event.py
│   │   │   └── registration.py
│   │   ├── schemas/             # Pydantic (validación de entrada/salida)
│   │   ├── routers/             # endpoints por módulo
│   │   │   ├── animals.py
│   │   │   ├── news.py
│   │   │   ├── events.py
│   │   │   └── registrations.py
│   │   └── crud/                # operaciones de BD reutilizables
│   ├── tests/                   # pytest
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/          # reutilizables
│   │   │   ├── AnimalCard.jsx
│   │   │   ├── NewsItem.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/               # vistas / rutas
│   │   │   ├── Home.jsx
│   │   │   ├── Animales.jsx
│   │   │   ├── Noticias.jsx
│   │   │   ├── Eventos.jsx
│   │   │   └── RegistrarAnimal.jsx
│   │   ├── services/api.js      # llamadas a la API
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── tests/                   # Vitest + Testing Library
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .github/workflows/frontend-ci.yml
└── docs/
    ├── historias-usuario.md
    ├── definicion-terminado.md
    └── kaizen.md
```

**Idea clave:** el backend está dividido por módulos (carpetas `models/`,
`routers/`, etc.) pero se despliega como una sola aplicación FastAPI. Eso es lo
que se llama "monolito modular".

---

## 4. Diseño de la API

API REST bajo el prefijo `/api/v1`. Todos los recursos retornan JSON.

### Animales — `/api/v1/animales`
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/animales` | Listar (filtro opcional por `estado`) |
| GET | `/animales/{id}` | Obtener detalle |
| POST | `/animales` | Crear |
| PUT | `/animales/{id}` | Editar |
| DELETE | `/animales/{id}` | Eliminar |

### Noticias — `/api/v1/noticias`
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/noticias` | Listar (orden descendente por fecha) |
| GET | `/noticias/{id}` | Detalle |
| POST | `/noticias` | Publicar |
| PUT | `/noticias/{id}` | Editar |
| DELETE | `/noticias/{id}` | Eliminar |

### Eventos — `/api/v1/eventos`
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/eventos` | Listar próximos eventos |
| GET | `/eventos/{id}` | Detalle |
| POST | `/eventos` | Crear |
| PUT | `/eventos/{id}` | Editar |
| DELETE | `/eventos/{id}` | Eliminar |

### Registros — `/api/v1/registros`
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/registros` | Listar interesados (admin) |
| GET | `/registros/{id}` | Detalle |
| POST | `/registros` | Registrar interés en un animal |
| DELETE | `/registros/{id}` | Eliminar |

### Ejemplo — `POST /api/v1/animales`
```json
{
  "nombre": "Luna",
  "especie": "perro",
  "edad": 3,
  "estado": "disponible",
  "descripcion": "Mestiza, vacunada y esterilizada"
}
```

Respuesta `201 Created`:
```json
{
  "id": 12,
  "nombre": "Luna",
  "especie": "perro",
  "edad": 3,
  "estado": "disponible",
  "descripcion": "Mestiza, vacunada y esterilizada",
  "created_at": "2026-04-28T10:30:00"
}
```

---

## 5. Modelo de base de datos (MySQL)

### Tablas

**animals**
| Campo | Tipo | Notas |
|---|---|---|
| id | INT, PK, auto | |
| nombre | VARCHAR(80) | obligatorio |
| especie | VARCHAR(40) | perro, gato, otro |
| edad | INT | en años |
| estado | ENUM | `disponible`, `en_proceso`, `adoptado` |
| descripcion | TEXT | |
| foto_url | VARCHAR(255) | |
| created_at | DATETIME | default `NOW()` |

**news**
| Campo | Tipo |
|---|---|
| id | INT, PK |
| titulo | VARCHAR(150) |
| contenido | TEXT |
| autor | VARCHAR(80) |
| fecha_publicacion | DATETIME |

**events**
| Campo | Tipo |
|---|---|
| id | INT, PK |
| nombre | VARCHAR(120) |
| descripcion | TEXT |
| fecha | DATETIME |
| lugar | VARCHAR(120) |
| cupo | INT |

**registrations**
| Campo | Tipo | Notas |
|---|---|---|
| id | INT, PK | |
| animal_id | INT, FK → animals.id | obligatoria |
| event_id | INT, FK → events.id | opcional |
| nombre | VARCHAR(100) | del interesado |
| email | VARCHAR(120) | |
| telefono | VARCHAR(30) | |
| mensaje | TEXT | |
| fecha | DATETIME | default `NOW()` |

### Relaciones

```
 animals (1) ─────< (N) registrations (N) >───── (1) events
 news    (independiente)
```

- Un animal puede tener varios registros de interesados.
- Un registro puede asociarse opcionalmente a un evento (ej. jornada de adopción).
- Las noticias no se relacionan con las demás tablas: son independientes.

### DDL básico (extracto)

```sql
CREATE TABLE animals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  especie VARCHAR(40) NOT NULL,
  edad INT,
  estado ENUM('disponible','en_proceso','adoptado') DEFAULT 'disponible',
  descripcion TEXT,
  foto_url VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registrations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  animal_id INT NOT NULL,
  event_id INT NULL,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL,
  telefono VARCHAR(30),
  mensaje TEXT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (animal_id) REFERENCES animals(id),
  FOREIGN KEY (event_id) REFERENCES events(id)
);
```
(`news` y `events` siguen el mismo patrón.)

---

## 6. Dockerización

### `docker-compose.yml`

```yaml
services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: fundacion
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "33306:3306"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: mysql+pymysql://root:root@db:3306/fundacion
    depends_on:
      - db
    ports:
      - "8080:8000"

  frontend:
    build: ./frontend
    environment:
      VITE_API_URL: http://localhost:8080/api/v1
    depends_on:
      - backend
    ports:
      - "5173:5173"

volumes:
  db_data:
```

### Explicación de cada servicio

| Servicio | Imagen / build | Función | Puerto |
|---|---|---|---|
| **db** | `mysql:8` | Almacena las 4 tablas. Usa volumen para persistencia. | 33306 (host) → 3306 (contenedor) |
| **backend** | `./backend` (FastAPI) | Expone la API REST. Se conecta a `db` por el nombre de servicio. | 8080 (host) → 8000 (contenedor) |
| **frontend** | `./frontend` (React + Vite) | Sirve la SPA. Llama al backend por `VITE_API_URL`. | 5173 |

Para levantar todo el sistema:
```bash
docker compose up --build
```

---

## 7. CI/CD básico (frontend) — GitHub Actions

`.github/workflows/frontend-ci.yml`:

```yaml
name: Frontend CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Instalar dependencias
        run: npm ci

      - name: Linter
        run: npm run lint

      - name: Pruebas
        run: npm test -- --run

      - name: Build de producción
        run: npm run build
```

**Qué hace:** en cada `push` o pull request a `main`/`develop` se instala
dependencias, se ejecuta el linter, las pruebas (Vitest + Testing Library) y el
build. Si algo falla, el PR se bloquea y no puede mezclarse.

---

## 8. Agilidad

### 8.1 Historias de usuario

**HU-01 — Listar animales en adopción**
> *Como* visitante del sitio,
> *quiero* ver el listado de animales disponibles con su nombre, especie, edad y estado,
> *para* identificar cuáles podría adoptar.
>
> **Criterios de aceptación:**
> - Solo se muestran animales con estado `disponible`.
> - Cada tarjeta muestra foto, nombre, especie y edad.
> - Si hay más de 12 animales, se aplica paginación.

**HU-02 — Registrar un animal nuevo (admin)**
> *Como* administrador de la fundación,
> *quiero* registrar un animal mediante un formulario,
> *para* que aparezca publicado en el listado de adopciones.
>
> **Criterios de aceptación:**
> - Campos obligatorios: nombre, especie, edad, estado.
> - Validación tanto en frontend como en backend.
> - Mensaje de confirmación al guardar.

**HU-03 — Publicar una noticia**
> *Como* administrador,
> *quiero* publicar una noticia con título, contenido y fecha,
> *para* mantener informada a la comunidad.
>
> **Criterios de aceptación:**
> - Las noticias aparecen ordenadas por fecha (más reciente primero).
> - Solo administradores pueden publicar.
> - Se muestra un previo de 200 caracteres en la lista.

### 8.2 Definición de Terminado (DoD)

Una historia se considera **terminada** cuando:

1. El código está en `main` y fue revisado por al menos un compañero (PR aprobado).
2. Existe al menos una prueba automatizada (unitaria o de componente).
3. Pasa el pipeline de CI (lint + tests + build).
4. Está documentada en el README o en `docs/`.
5. Funciona ejecutando `docker compose up --build`.
6. Cumple todos los criterios de aceptación de la historia.

### 8.3 Ejemplo de mejora Kaizen

**Observación al final del sprint 1:**
> Las pruebas locales corrían contra SQLite (más rápido), pero al desplegar en
> Docker con MySQL aparecieron errores de tipos (ENUM y formatos de fecha).
> Eso se detectó tarde y costó medio sprint corregirlo.

**Causa identificada:**
Diferencia entre la BD usada en desarrollo y la BD real de producción.

**Acción concreta para el sprint 2:**
- Añadir un servicio `db-test` (MySQL) en `docker-compose.test.yml`.
- Ejecutar las pruebas de integración del backend contra ese servicio en GitHub Actions.
- Documentar en el README cómo levantar el entorno de pruebas.

**Beneficio esperado:**
Detectar incompatibilidades de BD antes del despliegue, no después. El equipo
deja de perder tiempo en errores que solo aparecen "en producción".

---

## Resumen ejecutivo

| Aspecto | Decisión |
|---|---|
| Arquitectura | Monolito modular |
| Stack | React + FastAPI + MySQL |
| Despliegue | Docker Compose (3 servicios) |
| CI/CD | GitHub Actions (lint + tests + build) |
| Metodología | Scrum simplificado con backlog, DoD y Kaizen |

La solución prioriza **simplicidad y velocidad de entrega** sobre escalabilidad
teórica, lo cual es coherente con el tamaño del problema y el carácter de
laboratorio del taller. Si la fundación crece, el monolito puede dividirse en
servicios más adelante sin reescribirse desde cero (ya está modularizado).
