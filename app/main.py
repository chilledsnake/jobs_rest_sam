from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.api import router as api_router
from app.config import env_vars

root_path = f"/{env_vars.APP_ENV}" if env_vars.APP_ENV != "local" else ""

app = FastAPI(
    title="jobs-rest-api.ownspace.cloud API",
    description="""jobs-rest-api.ownspace.cloud API\n
    to get **github repository**, call **Get Info** endpoint,\n
    I hope You like it! 🚀
    """,
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

handler = Mangum(app)
