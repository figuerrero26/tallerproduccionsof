from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401 - registra los modelos en Base
from app.routers import news
from app.routers import registrations
from app.routers import animals, events


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Fundación Rescate Animal",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"
app.include_router(animals.router, prefix=API_PREFIX)
app.include_router(news.router, prefix=API_PREFIX)
app.include_router(events.router, prefix=API_PREFIX)
app.include_router(registrations.router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {"message": "API Fundación Rescate Animal", "docs": "/docs"}
