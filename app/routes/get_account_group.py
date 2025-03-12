from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.request_by_login import BaseRequest
from libs.manager import Manager, get_mt5_manager
import MT5Manager

@api_router.post("/api/get_account_group", response_model=None)
async def get_account_group(
    request: BaseRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user = MT5Manager.MTUser(manager.client)

        user: MT5Manager.MTUser = manager.client.UserGet(request.login)

        if user is False:
            return JSONResponse(
                content={"success": False, "error": "Unable to fetch user"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )
        else:
            return JSONResponse(
                content={
                    "success": True,
                    "account_group": user.Group
                },
                status_code=http_status.HTTP_200_OK,
            )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )