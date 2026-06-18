from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    routes_auth,
    routes_drone_types,
    routes_drones,
    routes_export,
    routes_flights,
    routes_reports,
    routes_users,
)
from app.core.config import get_settings
from app.core.version import APP_VERSION
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=APP_VERSION,
    description="API für das OpenUASLog Flugbuch.",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    routes_auth.router,
    routes_users.router,
    routes_drone_types.router,
    routes_drones.router,
    routes_flights.router,
    routes_reports.router,
    routes_export.router,
):
    app.include_router(router, prefix=settings.api_prefix)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": APP_VERSION}
