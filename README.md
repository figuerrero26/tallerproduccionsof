# Fundación Rescate Animal — Sistema Web

Sistema institucional para gestionar animales en adopción, noticias, eventos y
registros de interesados.

> Para la propuesta completa del taller (arquitectura, modelo de datos,
> agilidad, Kaizen) ver **[PROPUESTA.md](PROPUESTA.md)**.

## Stack

- **Frontend:** React 18 + Vite + React Router
- **Backend:** FastAPI + SQLAlchemy
- **BD:** MySQL 8
- **Infra:** Docker Compose
- **CI:** GitHub Actions

## Cómo correr el proyecto

**Requisitos:** Docker Desktop instalado.

```bash
docker compose up --build
```

Servicios disponibles:

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Documentación interactiva (Swagger) | http://localhost:8000/docs |
| MySQL | localhost:3306 (`root` / `root`) |

Para detener todo:

```bash
docker compose down
```

Para borrar también los datos de MySQL:

```bash
docker compose down -v
```

## Desarrollo local (sin Docker)

### Backend

```bash
cd backend
python -m venv .venv
# Linux / Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt

# Apunta a un MySQL local o usa SQLite:
export DATABASE_URL="sqlite:///./dev.db"
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

> Antes del primer push a GitHub, ejecuta `npm install` localmente para que se
> genere `package-lock.json` (lo necesita el pipeline de CI con `npm ci`).

## Pruebas

### Backend (pytest)

```bash
cd backend
pip install -r requirements.txt
pytest
```

### Frontend (Vitest + Testing Library)

```bash
cd frontend
npm test -- --run
```

## CI / CD

GitHub Actions ejecuta automáticamente en cada push o pull request a `main` /
`develop`:

1. `npm ci` — instala dependencias.
2. `npm run lint` — ESLint.
3. `npm test -- --run` — Vitest.
4. `npm run build` — build de producción.

Ver [`.github/workflows/frontend-ci.yml`](.github/workflows/frontend-ci.yml).

## Estructura del repositorio

```
.
├── backend/                # API FastAPI
│   ├── app/
│   │   ├── models/         # ORM
│   │   ├── schemas/        # Pydantic
│   │   ├── routers/        # endpoints REST
│   │   ├── crud/           # operaciones de BD
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # SPA React
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── tests/
│   ├── package.json
│   └── Dockerfile
│
├── docs/                   # documentación ágil
│   ├── historias-usuario.md
│   ├── definicion-terminado.md
│   └── kaizen.md
│
├── .github/workflows/
│   └── frontend-ci.yml
│
├── docker-compose.yml
├── PROPUESTA.md            # documento principal del taller
└── README.md
```

## Endpoints principales de la API

Prefijo: `/api/v1`

| Recurso | Endpoints |
|---|---|
| Animales | `GET /animales`, `GET /animales/{id}`, `POST /animales`, `PUT /animales/{id}`, `DELETE /animales/{id}` |
| Noticias | `GET /noticias`, `GET /noticias/{id}`, `POST /noticias`, `PUT /noticias/{id}`, `DELETE /noticias/{id}` |
| Eventos | `GET /eventos`, `GET /eventos/{id}`, `POST /eventos`, `PUT /eventos/{id}`, `DELETE /eventos/{id}` |
| Registros | `GET /registros`, `GET /registros/{id}`, `POST /registros`, `DELETE /registros/{id}` |

Documentación interactiva completa: http://localhost:8000/docs (Swagger UI
generado automáticamente por FastAPI).
