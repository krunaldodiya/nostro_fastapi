import MT5Manager
from fastapi import HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import Manager

manager = Manager()


@api_router.post("/api/disable_account/{login}")
async def disable_account(login: int):
    try:
        manager.connect()

        user_obj = manager.client.UserGet(login)

        if not isinstance(user_obj, MT5Manager.MTUser):
            raise HTTPException(status_code=404, detail="User not found")

        user_obj.Rights |= MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
        user_obj.Color = 255
        manager.client.UserUpdate(user_obj)

        return JSONResponse(
            content={"success": True, "message": f"User {login} disabled"},
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500,
        )

    finally:
        manager.disconnect()
