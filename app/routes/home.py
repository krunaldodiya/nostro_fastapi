from fastapi import status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router


@api_router.get("/", response_model=None)
async def index():
    return JSONResponse(
        content={"status": "Hello"},
        status_code=http_status.HTTP_200_OK,
    )
