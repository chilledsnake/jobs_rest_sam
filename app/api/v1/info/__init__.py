from fastapi import APIRouter

from app.api.v1.info.endpoints import router as info_router

# Create a router with a prefix and tag
router = APIRouter(prefix="/info")

router.include_router(info_router)
