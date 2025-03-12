from fastapi import Depends, status as http_status
from fastapi.responses import JSONResponse
from app.config.api_router import api_router
from app.schemas.request_by_login import BaseRequest
from libs.manager import Manager, get_mt5_manager

@api_router.post("/api/delete_pending_orders", response_model=None)
async def delete_pending_orders(
    request: BaseRequest,
    manager: Manager = Depends(get_mt5_manager),
):
    try:
        open_orders = manager.client.OrderGetOpen(request.login)

        if not isinstance(open_orders, list):
            return JSONResponse(
                content={"success": False, "error": "Unable to fetch orders"},
                status_code=http_status.HTTP_404_NOT_FOUND,
            )

        for order in open_orders:
            manager.client.OrderDelete(order.Order)

        return JSONResponse(
            content={
                "success": True
            },
            status_code=http_status.HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )