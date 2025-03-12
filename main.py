import dotenv

dotenv.load_dotenv()

from app.middlewares.api import ApiMiddleware
from app.routes import activate_account, delete_pending_orders
from app.routes import get_account_group, get_account_target, get_user_by_id, home
from app.routes import create_mt5_account, enable_account
from app.routes import get_account_status_data
from fastapi import FastAPI


def include_middlewares(app: FastAPI):
    app.add_middleware(ApiMiddleware)


def include_routers(app: FastAPI):
    app.include_router(home.api_router)
    app.include_router(get_user_by_id.api_router)
    app.include_router(create_mt5_account.api_router)
    app.include_router(delete_pending_orders.api_router)
    app.include_router(get_account_target.api_router)
    app.include_router(get_account_group.api_router)
    app.include_router(activate_account.api_router)
    app.include_router(enable_account.api_router)
    app.include_router(get_account_status_data.api_router)


def start_application():
    app = FastAPI()
    include_middlewares(app)
    include_routers(app)
    return app


app = start_application()
