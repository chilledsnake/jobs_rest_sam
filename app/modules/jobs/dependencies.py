from app.modules.jobs.repository import JobRepository


async def get_job_repository() -> JobRepository:
    return await JobRepository.create()
