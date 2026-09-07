from fastapi import APIRouter, Form
from app.db import SessionLocal
from sqlalchemy import select
from app.models.authorized_codes import Authorized

from datetime import datetime

from app.models.user import User



router = APIRouter()



@router.post("/token")
def get_valid(code: str = Form()):

    if not code:
        return None
    
    with SessionLocal() as session:
        check_existing = session.scalar(select(Authorized).where(Authorized.code == code))

        if not check_existing:
            return None
        
        if check_existing.expires_at < datetime.utcnow():
            session.delete(check_existing)
            session.commit()
            return None
        
        

        logged_user = session.scalar(select(User).where(User.id == check_existing.user_id))
        if not logged_user:
            return None
            


        session.delete(check_existing)
        session.commit()

        return {"user_id":logged_user.id, "username":logged_user.username}