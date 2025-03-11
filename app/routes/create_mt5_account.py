import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.create_account_request import CreateAccountRequest
from app.schemas.create_account_response import CreateAccountResponse
from libs.manager import Manager, get_mt5_manager
from libs.manager_helper import ManagerHelper


@api_router.post("/api/accounts", response_model=CreateAccountResponse)
async def create_mt5_account(
    request: CreateAccountRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        temp_main_password = ManagerHelper.generate_temp_password(15)
        temp_investor_password = ManagerHelper.generate_temp_password(15)

        user = MT5Manager.MTUser(manager.client)

        user.Name = request.name
        user.EMail = request.email
        user.Color = 3329330
        user.Group = request.group
        user.Company = str(request.initial_balance)
        user.LeadCampaign = str(request.initial_target)
        user.Rights = (
            MT5Manager.MTUser.EnUsersRights.USER_RIGHT_DEFAULT
            | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
        )
        user.Leverage = request.leverage

        user_created: bool = manager.client.UserAdd(
            user, temp_main_password, temp_investor_password
        )

        if not user_created:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        balance_added = manager.client.DealerBalance(
            user.Login, request.initial_balance, 5, "Initial Balance"
        )

        if not balance_added:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user.Rights = (
            MT5Manager.MTUser.EnUsersRights.USER_RIGHT_EXPERT
            | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_ENABLED
        )

        user_updated = manager.client.UserUpdate(user)

        if not user_updated:
            return JSONResponse(
                content={"success": False, "error": MT5Manager.LastError()},
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return CreateAccountResponse(
            data={
                "login": user.Login,
                "main_password": temp_main_password,
                "investor_password": temp_investor_password,
            },
            success=True,
            message="User created successfully",
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
