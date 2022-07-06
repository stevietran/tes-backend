from fastapi import APIRouter

from app.api.api_v1.endpoints import case, auth, result, result_2


api_router = APIRouter()
api_router.include_router(result.router, prefix="/result", tags=["app1"])
api_router.include_router(case.router, prefix="/case", tags=["case"])
api_router.include_router(auth.router, prefix='/auth', tags=["auth"])
api_router.include_router(result_2.router, prefix='/result/app2', tags=["app2"])
