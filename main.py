import dotenv

dotenv.load_dotenv()

from app.middlewares.api import ApiMiddleware
from app.routes import (
    delete_account,
    disable_account,
    reset_account_positions,
    reset_to_initial_balance,
)
from app.routes import (
    close_account_positions,
    close_account_positions_by_symbol,
    home,
    users,
)

from fastapi import FastAPI


def include_middlewares(app: FastAPI):
    app.add_middleware(ApiMiddleware)


def include_routers(app: FastAPI):
    app.include_router(home.api_router)
    app.include_router(users.api_router)
    app.include_router(delete_account.api_router)
    app.include_router(disable_account.api_router)
    app.include_router(reset_to_initial_balance.api_router)
    app.include_router(reset_account_positions.api_router)
    app.include_router(close_account_positions.api_router)
    app.include_router(close_account_positions_by_symbol.api_router)


def start_application():
    app = FastAPI()

    include_middlewares(app)
    include_routers(app)

    return app


app = start_application()
