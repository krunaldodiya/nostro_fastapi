from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from app.schema.login_request import LoginRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/delete_account")
async def delete_account(
    request: LoginRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:

        user_deleted = manager.client.UserDelete(request.login)

        if not user_deleted:
            raise HTTPException(status_code=400, detail="Failed to delete user account")

        return JSONResponse(
            content={"success": True, "message": f"User {request.login} deleted"},
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500,
        )
