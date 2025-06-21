from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
async def get_info():
    return """
    Github repository: https://github.com/chilledsnake/jobs_rest_sam,
    Author: Cezary Wróblewski
    Email: cwroblewski@o2.pl
    """
