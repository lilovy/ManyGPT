from fastapi import FastAPI, APIRouter, Request, Response
import uvicorn

from src.API.routes.web import (
    user as web_user,
    auth as web_auth,
    user_models as web_user_models,
    project as web_project,
    conversation as web_convo,
)
from src.API.routes.telegram import (
    user as telegram_user,
    auth as telegram_auth,
    user_models as telegram_user_models,
    project as telegram_project,
    conversation as telegram_convo,
    admin as telegram_admin,
)
from src.API.routes.core import (
    core,
)
from config import access, BASE_API_PATH
from src.API.middleware import middleware


app = FastAPI()
app.middleware("http")(middleware.auth_middleware)


web_router = APIRouter(prefix=f"{BASE_API_PATH}/web")

web_router.include_router(web_user.router)
web_router.include_router(web_auth.router)
web_router.include_router(web_user_models.router)
web_router.include_router(web_project.router)
web_router.include_router(web_convo.router)


telegram_router = APIRouter(prefix=f"{BASE_API_PATH}/telegram")

telegram_router.include_router(telegram_user.router)
telegram_router.include_router(telegram_auth.router)
telegram_router.include_router(telegram_user_models.router)
telegram_router.include_router(telegram_project.router)
telegram_router.include_router(telegram_convo.router)
telegram_router.include_router(telegram_admin.router)


core_router = APIRouter(prefix=f"{BASE_API_PATH}")

core_router.include_router(core.router)


app.include_router(web_router)
app.include_router(telegram_router)
app.include_router(core_router)


# if __name__ == "__main__":
#     uvicorn.run(f"{__name__}:app", reload=True)