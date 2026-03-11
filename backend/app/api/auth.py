from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from passlib.context import CryptContext
from jose import jwt
import os

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "user": db_user}

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "user": user}
