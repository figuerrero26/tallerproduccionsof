"""Pruebas básicas del módulo de animales.

Usan SQLite en memoria para ser rápidas y no depender de MySQL.
Las pruebas de integración contra MySQL real se introducirán en el sprint 2
(ver docs/kaizen.md).
"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tallerproduccionsof.backend.app.main import app
from tallerproduccionsof.backend.app.database import Base, get_db


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root_responde_ok():
    r = client.get("/")
    assert r.status_code == 200


def test_crear_y_listar_animal():
    payload = {"nombre": "Luna", "especie": "perro", "edad": 3}
    r = client.post("/api/v1/animales", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["nombre"] == "Luna"
    assert data["estado"] == "disponible"

    r = client.get("/api/v1/animales")
    assert r.status_code == 200
    assert any(a["nombre"] == "Luna" for a in r.json())


def test_animal_inexistente_devuelve_404():
    r = client.get("/api/v1/animales/99999")
    assert r.status_code == 404
