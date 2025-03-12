import MT5Manager
from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from app.schemas.login_request import LoginRequest
from libs.manager import Manager, get_mt5_manager

manager = Manager()


@api_router.post("/api/disable_account")
async def disable_account(
    request: LoginRequest, manager: Manager = Depends(get_mt5_manager)
):
    try:

        user_obj = manager.client.UserGet(request.login)

        if not isinstance(user_obj, MT5Manager.MTUser):
            raise HTTPException(status_code=404, detail="User not found")

        user_obj.Rights |= MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
        user_obj.Color = 255
        manager.client.UserUpdate(user_obj)

        return JSONResponse(
            content={"success": True, "message": f"User {request.login} disabled"},
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500,
        )
