import time
import MT5Manager
from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from app.routes.dealer_sink import DealerSink
from app.schemas.login_symbol_request import LoginSymbolRequest
from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/close_account_positions_by_symbol")
async def close_account_positions_by_symbol(
    request: LoginSymbolRequest, manager: Manager = Depends(get_mt5_manager)
):

    try:
        manager.connect()
        positions: list[MT5Manager.MTPosition] = manager.client.PositionGet(
            request.login
        )
        if not positions:
            return JSONResponse(
                content={"success": True, "message": "No open positions"},
                status_code=200,
            )

        sink = DealerSink()
        position_closed = False

        for position in positions:
            if position.Symbol != request.symbol:
                continue

            order = MT5Manager.MTRequest(manager.client)
            order.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_FIRST
            order.TypeFill = MT5Manager.MTOrder.EnOrderFilling.ORDER_FILL_FIRST
            order.Login = request.login
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
                    status_code=500,
                    detail=f"Failed to close position {position.Position} for symbol {request.symbol}",
                )

            position_closed = True

        if not position_closed:
            raise HTTPException(
                status_code=404,
                detail=f"No matching positions found for symbol {request.symbol}",
            )

        return {"success": True}

    except AssertionError as ae:
        raise HTTPException(status_code=400, detail=str(ae))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error closing account positions: {str(e)}"
        )
    finally:
        manager.disconnect()
