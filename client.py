from fastapi import FastAPI, APIRouter, Request, Response
from src.API.routes.web import user, auth, user_models, project, conversation
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from config import access, BASE_API_PATH
from src.API.middleware import middleware


app = FastAPI()
app.middleware("http")(middleware.auth_middleware)

app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

templates = Jinja2Templates(directory="src/frontend/templates")


web_router = APIRouter(prefix=f"{BASE_API_PATH}/web")

web_router.include_router(user.router)
web_router.include_router(auth.router)
web_router.include_router(user_models.router)
web_router.include_router(project.router)
web_router.include_router(conversation.router)


telegram_router = APIRouter(prefix=f"{BASE_API_PATH}/telegram/{access}")



app.include_router(web_router)
app.include_router(telegram_router)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)