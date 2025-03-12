from typing import List
import MT5Manager
from fastapi import Depends, HTTPException, status as http_status

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config.api_router import api_router

from app.schemas.login_request import LoginRequest
from libs.manager import Manager, get_mt5_manager


class OpenDealData(BaseModel):
    TradeAccount: int
    DealSymbol: str
    DealVolume: float
    Profit: float
    DealType: str
    PositionID: int


@api_router.post("/api/get_open_account_positions", response_model=List[OpenDealData])
async def get_open_account_positions(
    request: LoginRequest, manager: Manager = Depends(get_mt5_manager)
):
    try:
        activity_trades: List[OpenDealData] = []
        positions = manager.client.PositionGet(request.login)

        if not positions:
            return []

        for position in positions:
            trade = OpenDealData(
                TradeAccount=position.Login,
                DealSymbol=position.Symbol,
                DealVolume=position.Volume,
                Profit=position.Profit,
                DealType="SELL" if position.Action == 0 else "BUY",
                PositionID=position.Position,
            )
            activity_trades.append(trade)

        return activity_trades

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in get_open_account_positions: {str(e)}"
        )
