import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.create_account_response import CreateAccountResponse
from app.schemas.login_request import LoginRequest

from app.schemas.user_update_request import UserUpdateRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/user_update", response_model=CreateAccountResponse)
async def user_update(
    request: UserUpdateRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user_obj = manager.client.UserGet(request.login)

        if not isinstance(user_obj, MT5Manager.MTUser):
            return JSONResponse(
                content={"success": False, "error": "User account not found"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )
        user_obj.Comment = request.comment
        user_obj.Color = request.color
        user_right = user_obj.Rights
        user_right |= MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
        user_obj.Rights = user_right
        manager.client.UserUpdate(user_obj)
        return CreateAccountResponse(
            data={"user_rights": user_obj.Rights},
            success=True,
            message="User updated successfully",
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
