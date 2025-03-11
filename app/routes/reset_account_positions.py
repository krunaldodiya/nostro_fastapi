import time
import MT5Manager
from fastapi import HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import DealerSink, Manager

manager = Manager()


@api_router.post("/api/reset_account/{login}")
async def reset_account_positions(login: int):
    try:
        manager.connect()

        user_obj: MT5Manager.MTUser = manager.client.UserGet(login)
        user_account: MT5Manager.MTAccount = manager.client.UserAccountGet(login)

        if not user_obj or not user_account:
            raise HTTPException(status_code=404, detail="User account not found")

        try:
            initial_balance = float(user_obj.Company)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid initial balance")

        # Get open positions
        positions = manager.client.PositionGet(login)
        if not positions:
            return JSONResponse(
                content={"success": True, "message": "No open positions to reset"},
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

        time.sleep(1)

        balance_order = MT5Manager.MTRequest(manager.client)
        balance_order.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_BALANCE
        balance_order.Type = MT5Manager.MTOrder.EnOrderType.OP_SELL_STOP
        balance_order.Login = login
        balance_order.PriceOrder = initial_balance - user_account.Equity

        response = manager.client.DealerSend(balance_order, sink)
        if not response:
            raise HTTPException(status_code=400, detail="Failed to reset balance")

        return JSONResponse(
            content={
                "success": True,
                "message": f"User {login} positions reset successfully",
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, status_code=500
        )

    finally:
        manager.disconnect()
