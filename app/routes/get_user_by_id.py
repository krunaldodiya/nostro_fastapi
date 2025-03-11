import MT5Manager

from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from libs.manager import Manager, get_mt5_manager


@api_router.get("/api/users/{user_id}", response_model=None)
async def get_user_by_id(
    user_id: int,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        user = manager.client.UserGet(user_id)

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
