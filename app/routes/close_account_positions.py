import time
import MT5Manager
from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from app.routes.dealer_sink import DealerSink
from app.schema.login_request import LoginRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/close_account_positions")
async def close_account_positions(
    request: LoginRequest, manager: Manager = Depends(get_mt5_manager)
):
    try:

        positions = manager.client.PositionGet(request.login)
        if not positions:
            return JSONResponse(
                content={"success": True, "message": "No open positions to close"},
                status_code=200,
            )

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

        return JSONResponse(
            content={
                "success": True,
                "message": f"All positions for user {request.login} closed successfully",
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, status_code=500
        )
