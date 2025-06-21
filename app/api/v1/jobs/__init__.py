from fastapi import APIRouter

from app.api.v1.jobs.endpoints import (  # delete_job_router,  # Assuming you have a delete endpoint as well
    create_job_router,
    delete_job_router,
    get_job_router,
    list_jobs_router,
    update_job_router,
)

# Create a router with a prefix and tag
router = APIRouter(prefix="/jobs")

router.include_router(get_job_router)
router.include_router(list_jobs_router)
router.include_router(create_job_router)
router.include_router(update_job_router)
router.include_router(delete_job_router)
