import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.create_account_response import CreateAccountResponse
from app.schemas.login_request import LoginRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/get_user_account", response_model=CreateAccountResponse)
async def get_user_account(
    request: LoginRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user_account = manager.client.UserAccountGet(request.login)

        if not isinstance(user_account, MT5Manager.MTAccount):
            return JSONResponse(
                content={"success": False, "error": "User account not found"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )

        return CreateAccountResponse(
            data={
                "Login": user_account.Login,
                "Equity": user_account.Equity,
                "Balance": user_account.Balance,
                "Profit": user_account.Profit,
            },
            success=True,
            message="Get user account successfully",
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
