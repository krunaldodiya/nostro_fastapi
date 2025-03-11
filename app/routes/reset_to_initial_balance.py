import MT5Manager
from fastapi import HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import DealerSink, Manager

manager = Manager()


@api_router.post("/api/reset_to_initial_balance/{login}/{initial_balance}")
async def reset_to_initial_balance(login: int, initial_balance: float):
    try:

        manager.connect()

        user_account: MT5Manager.MTAccount = manager.client.UserAccountGet(login)
        if not user_account:
            raise HTTPException(status_code=404, detail="User account not found")

        request = MT5Manager.MTRequest(manager.client)
        request.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_BALANCE
        request.Type = MT5Manager.MTOrder.EnOrderType.OP_SELL_STOP
        request.Login = login
        request.PriceOrder = initial_balance - user_account.Equity

        sink = DealerSink()
        response = manager.client.DealerSend(request, sink)

        if not response:
            raise HTTPException(status_code=400, detail="Failed to reset balance")

        return JSONResponse(
            content={
                "success": True,
                "message": f"User {login} balance reset to {initial_balance}",
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500,
        )

    finally:
        manager.disconnect()
