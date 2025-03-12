import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.reset_password_request import ResetPasswordRequest
from libs.manager import Manager, get_mt5_manager
from libs.manager_helper import ManagerHelper


@api_router.post("/api/passwords/reset", response_model=None)
async def reset_password(
    request: ResetPasswordRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        temp_main_password = ManagerHelper.generate_temp_password(15)

        main_password_changed = manager.client.UserPasswordChange(
            MT5Manager.MTUser.EnUsersPasswords.USER_PASS_MAIN,
            request.login,
            temp_main_password,
        )

        if not main_password_changed:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        temp_investor_password = ManagerHelper.generate_temp_password(15)

        investor_password_changed = manager.client.UserPasswordChange(
            MT5Manager.MTUser.EnUsersPasswords.USER_PASS_MAIN,
            request.login,
            temp_investor_password,
        )

        if not investor_password_changed:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "main_password": temp_main_password,
                    "investor_password": temp_investor_password,
                },
            },
            status_code=http_status.HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
