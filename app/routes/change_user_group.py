import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.change_group_request import ChangeGroupRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/users/change-group", response_model=None)
async def change_user_group(
    request: ChangeGroupRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        trade_user: MT5Manager.MTUser | None = manager.client.UserGet(request.login)

        if not trade_user:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        trade_user.Group = request.group

        group_changed = manager.client.UserUpdate(trade_user)

        if not group_changed:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return JSONResponse(
            content={"success": True, "message": "User group has been changed."},
            status_code=http_status.HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
