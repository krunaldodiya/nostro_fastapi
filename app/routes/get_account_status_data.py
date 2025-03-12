import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.request_by_login import BaseRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/get_account_status_data", response_model=None)
async def get_account_status_data(
    request: BaseRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user_obj = manager.client.UserGet(request.login)

        user_acc = manager.client.UserAccountGet(request.login)

        if not user_obj:
            return JSONResponse(
                content={"success": False, "error": "Unable to fetch user"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )

        activeAccount = not (
            (
                user_obj.Rights
                & MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
            )
            > 0
        )

        profit = user_acc.Profit
        balance = user_obj.Balance
        equity = user_acc.Equity
        group = user_obj.Group
        yesterdayEquity = user_obj.EquityPrevDay

        return JSONResponse(
            content={
                "success": True,
                "profit": profit,
                "balance": balance,
                "equity": equity,
                "group": group,
                "yesterdayEquity": yesterdayEquity,
                "activeAccount": activeAccount,
            },
            status_code=http_status.HTTP_200_OK,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
