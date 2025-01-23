from collections.abc import Callable, AsyncGenerator
from contextlib import asynccontextmanager, AbstractContextManager
from typing import Any

import fastapi
from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from sqlmodel import SQLModel, create_engine

from src.app.core.config import DatabaseSettings, AppSettings, EnvironmentSettings, EnvironmentOption
from src.app.core.db.database import engine


# --------------------------- database ---------------------------
def create_tables() -> None:
    with engine.begin() as conn:
        SQLModel.metadata.create_all(bind=conn.engine)

# --------------------------- application ---------------------------
def lifespan_factory(
        settings: (
            AppSettings
            | DatabaseSettings
            | EnvironmentSettings
        ),
        create_tables_on_start: bool = True,
) -> Callable[[FastAPI], AbstractContextManager[Any]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

        if isinstance(settings, DatabaseSettings) and create_tables_on_start:
            create_tables()

        yield

    return lifespan

def create_application(
        router: APIRouter,
        settings: (
            AppSettings
            | DatabaseSettings
            | EnvironmentSettings
        ),
        create_tables_on_start: bool = True,
        **kwargs: Any,
) -> FastAPI:

    if isinstance(settings, AppSettings):
        to_update = {
            "title": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION
        }
        kwargs.update(to_update)

    if isinstance(settings, EnvironmentSettings):
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    lifespan = lifespan_factory(settings, create_tables_on_start = create_tables_on_start)

    application = FastAPI(lifespan = lifespan, **kwargs)
    application.include_router(router)

    if isinstance(settings, EnvironmentSettings):
        if settings.ENVIRONMENT != EnvironmentOption.PRODUCTION:
            docs_router = APIRouter()

            @docs_router.get("/docs", include_in_schema=False)
            def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
                return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/redoc", include_in_schema=False)
            def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
                return get_redoc_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/openapi.json", include_in_schema=False)
            def openapi() -> dict[str, Any]:
                out: dict = get_openapi(title=application.title, version=application.version, routes=application.routes)
                return out

            application.include_router(docs_router)

        return application