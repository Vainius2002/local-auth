from fastapi import APIRouter, Depends, Response
from app.dependencies import get_current_user

from app.models.user import User

from fastapi.responses import RedirectResponse



router = APIRouter()


@router.get("/")
def hello(response: Response, user: User=Depends(get_current_user)):
    if not user:
        response.delete_cookie("session_id")

        return RedirectResponse("/login")
        
    return {"found_user": "yes"}
