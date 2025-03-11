import dotenv

dotenv.load_dotenv()

from app.middlewares.api import ApiMiddleware
from app.routes import get_user_by_id, home, create_mt5_account
from fastapi import FastAPI


def include_middlewares(app: FastAPI):
    app.add_middleware(ApiMiddleware)


def include_routers(app: FastAPI):
    app.include_router(home.api_router)
    app.include_router(get_user_by_id.api_router)
    app.include_router(create_mt5_account.api_router)


def start_application():
    app = FastAPI()
    include_middlewares(app)
    include_routers(app)
    return app


app = start_application()
