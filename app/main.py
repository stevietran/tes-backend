import time

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

root_router = APIRouter()

app = FastAPI(
    title="TES BACKEND API",
    description="Backend service for TES applications",
    version=settings.API_V1_STR,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Vu Tran",
        "email": "levu.tran@ntu.edu.sg",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@root_router.get("/", status_code=200)
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

origins = [
    "http://tes-frontend",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR) ## <----- API versioning
app.include_router(root_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
