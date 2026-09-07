from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles

from app.routes.authorize import router as check_cookies
from app.routes.create_login import router as create_login
from app.routes.home import router as hello
from app.routes.login import router as login
from app.routes.token import router as get_valid




app = FastAPI()


app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(check_cookies)
app.include_router(create_login)
app.include_router(hello)
app.include_router(login)
app.include_router(get_valid)