from app.models.sessions import Sessions
from app.models.user import User
from app.db import SessionLocal
from sqlalchemy import select

from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from datetime import datetime




def get_current_user(request : Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return None

    with SessionLocal() as session:
        session_exists = session.scalar(select(Sessions).where(Sessions.session_id == session_id))

        if not session_exists:
            return None

        if session_exists.expires_at < datetime.utcnow():
            session.delete(session_exists)
            session.commit()
            return None
            
        user = session.scalar(select(User).where(User.id == session_exists.user_id))
        if not user:
            return None


        return user


