import MT5Manager

from fastapi import status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import Manager

manager = Manager()


@api_router.get("/api/users/{user_id}", response_model=None)
async def test(user_id: int):
    try:
        manager.connect()

        user = manager.client.UserGet(user_id)

        if not isinstance(user, MT5Manager.MTUser):
            return JSONResponse(
                content={"success": False, "error": "User not found"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )

        return JSONResponse(
            content={
                "success": True,
                "user": {"login": user.Login, "group": user.Group},
            },
            status_code=http_status.HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        manager.disconnect()
