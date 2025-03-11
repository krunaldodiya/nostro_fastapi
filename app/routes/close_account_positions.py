import time
import MT5Manager
from fastapi import HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import DealerSink, Manager

manager = Manager()


@api_router.post("/api/close_account_positions/{login}")
async def close_account_positions(login: int):
    try:
        manager.connect()

        positions = manager.client.PositionGet(login)
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
                print(
                    f"Couldn't close position due to invalid action type: {position.Action}"
                )
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
                "message": f"All positions for user {login} closed successfully",
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, status_code=500
        )

    finally:
        manager.disconnect()
