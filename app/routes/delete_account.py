from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse

from app.config.api_router import api_router

from libs.manager import Manager, get_mt5_manager


@api_router.post("/api/delete_account/{user_id}")
async def delete_account(
    user_id: int,
    manager: Manager = Depends(get_mt5_manager),
):
    try:

        user_deleted = manager.client.UserDelete(user_id)

        if not user_deleted:
            raise HTTPException(status_code=400, detail="Failed to delete user account")

        return JSONResponse(
            content={"success": True, "message": f"User {user_id} deleted"},
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500,
        )
