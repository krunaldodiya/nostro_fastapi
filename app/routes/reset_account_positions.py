import time
import MT5Manager

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.routes.dealer_sink import DealerSink
from app.schemas.login_request import LoginRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/reset_account_positions")
async def reset_account_positions(
    request: LoginRequest, manager: Manager = Depends(get_mt5_manager)
):
    try:

        user_obj: MT5Manager.MTUser = manager.client.UserGet(request.login)
        user_account: MT5Manager.MTAccount = manager.client.UserAccountGet(
            request.login
        )

        if not user_obj or not user_account:
            raise HTTPException(status_code=404, detail="User account not found")

        try:
            initial_balance = float(user_obj.Company)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid initial balance")

        positions = manager.client.PositionGet(request.login)

        sink = DealerSink()

        for position in positions:
            order = MT5Manager.MTRequest(manager.client)
            order.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_FIRST
            order.TypeFill = MT5Manager.MTOrder.EnOrderFilling.ORDER_FILL_FIRST
            order.Login = position.Login
            order.Symbol = position.Symbol
            order.Position = position.Position
            order.Volume = position.Volume

            if position.Action == 0:
                order.Type = MT5Manager.MTOrder.EnOrderType.OP_SELL
            elif position.Action == 1:
                order.Type = MT5Manager.MTOrder.EnOrderType.OP_BUY
            else:
                continue

            response = manager.client.DealerSend(order, sink)
            if not response:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to close position {position.Position}",
                )

        time.sleep(1)
        order = MT5Manager.MTRequest(manager.client)
        order.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_BALANCE
        order.Type = MT5Manager.MTOrder.EnOrderType.OP_SELL_STOP
        order.Login = request.login
        order.PriceOrder = initial_balance - user_account.Equity
        response = manager.client.DealerSend(order, sink)

        if not response:
            raise HTTPException(status_code=400, detail="Failed to reset balance")

        return JSONResponse(
            content={
                "success": True,
                "message": f"User {request.login} positions reset successfully",
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, status_code=500
        )
