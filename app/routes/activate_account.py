from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.request_by_login import BaseRequest
from libs.manager import Manager, get_mt5_manager
import MT5Manager

@api_router.post("/api/activate_account", response_model=None)
async def activate_account(
    request: BaseRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user_obj = MT5Manager.MTUser(manager.client)
        user_obj: MT5Manager.MTUser = manager.client.UserGet(request.login)

        user_obj.Rights = (
            user_obj.Rights
            | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_ENABLED
            | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_EXPERT
        ) & (~MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED)

        user_obj.Color = 3329330

        response = manager.client.UserUpdate(user_obj)

        if response != True:
            return JSONResponse(
                content={"success": False, "error": "Unable to update user"},
                status_code=http_status.HTTP_404_NOT_FOUND)
        else:
            return JSONResponse(
                content={
                    "success": True
                },
                status_code=http_status.HTTP_200_OK,
            )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )