from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserLogin, UserOut
from app.database import get_db
from app.utils import hash_password, verify_password
from app.auth import create_access_token, verify_token

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Received data: {user}")
    existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_user:
        print("User already exists")
        raise HTTPException(status_code=400, detail="Пользователь с таким номером уже существует")
    hashed_password = hash_password(user.password)
    print(f"Hashed password: {hashed_password}")
    db_user = User(name=user.name, phone_number=user.phone_number, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Неверные учетные данные")
    access_token = create_access_token(data={"sub": db_user.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    db_user = db.query(User).filter(User.phone_number == token["sub"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user
