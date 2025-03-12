import dotenv

dotenv.load_dotenv()

from fastapi import FastAPI

from app.middlewares.api import ApiMiddleware
from app.routes import (
    delete_account,
    disable_account,
    reset_account_positions,
    close_account_positions,
    close_account_positions_by_symbol,
    get_user_by_id,
    home,
    create_mt5_account,
    reset_to_initial_balance,
    get_open_account_positions,
    get_trade_accounts_in_group,
)


def include_middlewares(app: FastAPI):
    app.add_middleware(ApiMiddleware)


def include_routers(app: FastAPI):
    app.include_router(home.api_router)
    app.include_router(delete_account.api_router)
    app.include_router(disable_account.api_router)
    app.include_router(reset_to_initial_balance.api_router)
    app.include_router(reset_account_positions.api_router)
    app.include_router(close_account_positions.api_router)
    app.include_router(close_account_positions_by_symbol.api_router)
    app.include_router(get_user_by_id.api_router)
    app.include_router(create_mt5_account.api_router)
    app.include_router(get_open_account_positions.api_router)
    app.include_router(get_trade_accounts_in_group.api_router)


def start_application():
    app = FastAPI()
    include_middlewares(app)
    include_routers(app)
    return app


app = start_application()
