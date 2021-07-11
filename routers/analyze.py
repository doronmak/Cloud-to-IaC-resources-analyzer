from analyzer_service import AnalyzeService
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.logger import logger


def create_analyze_router(analyze_service: AnalyzeService):
    analyze_router = APIRouter()

    @analyze_router.get('')
    def analyze(cloud_resource_id: str):
        try:
            response = analyze_service.analyze_resource(cloud_resource_id)
            return JSONResponse(content=response, status_code=200)
        except Exception as e:
            if e.__str__() == "cloud resource was not found":
                return JSONResponse(content=e.__str__(), status_code=404)
            else:
                error = f"Got Exception when trying get analyze of resource, EX: {e.__str__()}"
                logger.exception(error)
                return JSONResponse(content=error, status_code=500)

    return analyze_router
