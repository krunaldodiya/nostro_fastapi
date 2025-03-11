import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.create_account_request import CreateAccountRequest
from app.schemas.create_account_response import CreateAccountResponse
from libs.manager import Manager, get_mt5_manager


@api_router.get("/api/accounts", response_model=CreateAccountResponse)
async def create_mt5_account(
    request: CreateAccountRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user = manager.client.UserGet(request.email)

        if not isinstance(user, MT5Manager.MTUser):
            return JSONResponse(
                content={"success": False, "error": "User not found"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )

        return JSONResponse(
            content={
                "success": True,
                "user": {
                    "Login": user.Login,
                    "Account": user.Account,
                    "Group": user.Group,
                    "Name": user.Name,
                    "Phone": user.Phone,
                    "Country": user.Country,
                    "City": user.City,
                    "Address": user.Address,
                },
            },
            status_code=http_status.HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
