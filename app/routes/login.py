from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.templating import Jinja2Templates

from app.db import SessionLocal
from sqlalchemy import select
from app.models.user import User
from app.models.sessions import Sessions

from fastapi.responses import RedirectResponse

from app.dependencies import get_current_user

from app.services.hash_verify import compare_passwords

import secrets

from datetime import datetime, timedelta



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@router.get("/login")
def login_page(request: Request, redirect_uri : str = None, user : User=Depends(get_current_user)):
    if user:
        return RedirectResponse(f"/authorize?redirect_uri={redirect_uri}")

    return templates.TemplateResponse(request, "login.html", {"redirect_uri": redirect_uri})

# Request  = read what browser sent
# Response = tell browser what to store

@router.post("/login")
def login(response : Response, username : str = Form(), password : str = Form(), redirect_uri: str = Form(None)):
    with SessionLocal() as session:

        right_user = session.scalar(select(User).where(User.username == username))

        if right_user:
            compare = compare_passwords(right_user.password_hash, password)

            if compare != True:
                return "Wrong password. Try again."
            else:
                print("Successfull login!")
                session_id = secrets.token_urlsafe(32)

                # setting it to browser
                response.set_cookie(
                    key="session_id",
                    value=session_id,
                    httponly=True,
                    secure=True,
                    samesite="lax"
                )

                # setting session_id to db.
                session_table = Sessions(
                    user_id = right_user.id,
                    session_id = session_id,
                    expires_at = datetime.utcnow() + timedelta(days=7)
                )
                session.add(session_table)
                session.commit()
                session.refresh(session_table)

                return {"redirect": f"/authorize?redirect_uri={redirect_uri}"}


        else:
            return "Username not found. Try again."
    



