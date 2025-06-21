from fastapi import APIRouter

from app.api.v1 import router as api_v1_router

# Create a router with a prefix and tag
router = APIRouter()

# Include individual routers
router.include_router(api_v1_router)
