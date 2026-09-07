from fastapi import APIRouter
from app.db import SessionLocal
from app.models.user import User
from sqlalchemy import select

from app.services.hash_verify import hash_passw

from app.config import USERNAME, PASSWORD


router = APIRouter()


@router.get("/login-creation")
def create_login():
    hashed_passw = hash_passw(PASSWORD)
    
    with SessionLocal() as session:

        user = User(
            username=USERNAME,
            password_hash=hashed_passw
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
