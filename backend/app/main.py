from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app import crud, models, schemas, security
from backend.app.database import SessionLocal, engine
from backend.app.security import verify_password, create_access_token
from datetime import timedelta

app = FastAPI()

# Создание базы данных
models.Base.metadata.create_all(bind=engine)

# OAuth2PasswordBearer сообщает FastAPI, что в запросах будет передаваться токен Bearer.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для получения текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.verify_token(token)
    user = crud.get_user_by_username(db=db, username=payload.get("sub"))
    if user is None:
        raise credentials_exception
    return user

@app.post("/users/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user

@app.post("/token")
def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Защищенные эндпоинты, доступные только с токеном
@app.get("/users/me", response_model=schemas.UserBase)
def read_users_me(current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user
