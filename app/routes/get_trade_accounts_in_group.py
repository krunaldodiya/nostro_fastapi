from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.trade_account_group_request import TradeAccountGroupRequest
from libs.manager import Manager, get_mt5_manager


@api_router.get("/api/trade/accounts/group", response_model=None)
async def get_trade_accounts_in_group(
    request: TradeAccountGroupRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    users = manager.client.UserGetByGroup(request.group)

    accounts = [user.Login for user in users]

    return JSONResponse(
        content={"status": "okay", "accounts": accounts},
        status_code=http_status.HTTP_200_OK,
    )
