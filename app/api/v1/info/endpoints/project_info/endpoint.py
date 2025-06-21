from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
async def get_info():
    return """
    Github repository: https://github.com/chilledsnake/common_pairs_sam_api,
    Author: Cezary Wróblewski
    Email: cwroblewski@o2.pl
    """
