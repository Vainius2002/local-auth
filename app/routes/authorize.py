from fastapi import APIRouter, Request, Depends

from fastapi.responses import RedirectResponse

from app.dependencies import get_current_user

from app.models.authorized_codes import Authorized

import secrets

from datetime import datetime, timedelta
from app.db import SessionLocal
from sqlalchemy import select
from app.models.user import User
from app.models.sessions import Sessions

from app.config import ALLOWED_REDIRECT_URIS




router = APIRouter()


@router.get("/authorize")
def check_cookies(request: Request, redirect_uri: str, user: User = Depends(get_current_user)):

    if redirect_uri not in ALLOWED_REDIRECT_URIS:
        return RedirectResponse(f"/login?redirect_uri={redirect_uri}")
    
    if not user:
        return RedirectResponse(f"/login?redirect_uri={redirect_uri}")


    username = user.username
    code = secrets.token_urlsafe(32)



    with SessionLocal() as session:
        authorized_row = Authorized(
            user_id = user.id,
            code = code,
            expires_at = datetime.utcnow() + timedelta(minutes=3)
        )
        session.add(authorized_row)
        session.commit()
        session.refresh(authorized_row)


    return RedirectResponse(f"{redirect_uri}?code={code}")


