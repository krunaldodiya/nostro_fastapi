import time
import MT5Manager
from fastapi import HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import DealerSink, Manager

manager = Manager()


@api_router.post("/api/close_account_positions_by_symbol/{login}/{symbol}")
async def close_account_positions_by_symbol(login: int, symbol: str):

    try:
        manager.connect()
        positions: list[MT5Manager.MTPosition] = manager.client.PositionGet(login)
        if not positions:
            raise HTTPException(
                status_code=404,
                detail=f"No open positions found for login {login}",
            )

        sink = DealerSink()
        position_closed = False

        for position in positions:
            if position.Symbol != symbol:
                continue

            order = MT5Manager.MTRequest(manager.client)
            order.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_FIRST
            order.TypeFill = MT5Manager.MTOrder.EnOrderFilling.ORDER_FILL_FIRST
            order.Login = login
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
                    detail=f"Failed to close position {position.Position} for symbol {symbol}",
                )

            position_closed = True

        if not position_closed:
            raise HTTPException(
                status_code=404,
                detail=f"No matching positions found for symbol {symbol}",
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
