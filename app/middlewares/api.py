from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.environments import AUTH_TOKEN


class ApiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            try:
                token = request.headers.get("X-TOKEN", "")

                if not token or token != AUTH_TOKEN:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not Authorized",
                    )
            except HTTPException as e:
                return JSONResponse(
                    content={"errors": e.detail},
                    status_code=e.status_code,
                )

        response = await call_next(request)

        return response
