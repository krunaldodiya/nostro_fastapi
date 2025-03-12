import MT5Manager
from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.dealer_sink import DealerSink
from app.schemas.login_balance_request import LoginBalanceRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/reset_to_initial_balance")
async def reset_to_initial_balance(
    request: LoginBalanceRequest, manager: Manager = Depends(get_mt5_manager)
):
    try:

        user_account: MT5Manager.MTAccount = manager.client.UserAccountGet(
            request.login
        )
        if not user_account:
            raise HTTPException(status_code=404, detail="User account not found")

        mt_request = MT5Manager.MTRequest(manager.client)
        mt_request.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_BALANCE
        mt_request.Type = MT5Manager.MTOrder.EnOrderType.OP_SELL_STOP
        mt_request.Login = request.login
        mt_request.PriceOrder = request.initial_balance - user_account.Equity

        sink = DealerSink()
        response = manager.client.DealerSend(mt_request, sink)

        if not response:
            raise HTTPException(status_code=400, detail="Failed to reset balance")

        return JSONResponse(
            content={
                "success": True,
                "message": f"User {request.login} balance reset to {request.initial_balance}",
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500,
        )
