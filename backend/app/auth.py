from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .secret import SECRET_KEY, ALGORITHM  # Тут должны быть ваши ключи и алгоритм

# Для использования OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для создания токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для верификации токена
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Проверка, есть ли обязательное поле 'sub' (например, телефон пользователя)
        if "sub" not in payload:
            raise HTTPException(status_code=403, detail="Token does not contain subject ('sub')")
        
        return payload  # Возвращаем полезную нагрузку токена
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

