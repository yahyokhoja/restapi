from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserOut, UserUpdate
from app.database import get_db
from app.utils import hash_password, verify_password
from app.auth import create_access_token, verify_token

router = APIRouter(prefix="/user", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    db_user = User(
        name=user.name,
        phone_number=user.phone_number,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),  # использование формы с полями username и password
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.phone_number == form_data.username).first()  # используем phone_number как username
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Неверные учетные данные")
    
    access_token = create_access_token(data={"sub": db_user.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_me(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_data = verify_token(token)
    user = db.query(User).filter(User.phone_number == user_data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.put("/me", response_model=UserOut)
def update_me(
    update: UserUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_data = verify_token(token)
    user = db.query(User).filter(User.phone_number == user_data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if update.name:
        user.name = update.name
    if update.password:
        user.password_hash = hash_password(update.password)
    db.commit()
    db.refresh(user)
    return user
