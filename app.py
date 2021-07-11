from fastapi import FastAPI
from settings import config, resources
from fastapi.responses import JSONResponse
from data_managers.file_loader import FileLoader
from routers import analyze
from analyzer_service import AnalyzeService


def init_routes(app: FastAPI, analyze_service):
    @app.get(config.BASE_URL)
    def index():
        data = "Api is on fire!"
        return JSONResponse(content=data, status_code=200)

    app.include_router(analyze.create_analyze_router(analyze_service), prefix=resources.ANALYZE)


def init_service():
    file_loader = FileLoader()
    return AnalyzeService(file_loader)


def create_app():
    analyze_service = init_service()
    app = FastAPI(title="Resource Analyzer API", openapi_url=config.OPEN_API_URL, docs_url=config.DOCS_URL,
                  redoc_url=config.REDOC_URL)
    init_routes(app, analyze_service)
    return app
