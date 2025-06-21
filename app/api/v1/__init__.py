from fastapi import APIRouter

from app.api.v1.info import router as info_router
from app.api.v1.jobs import router as jobs_router

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(jobs_router)
router.include_router(info_router)
