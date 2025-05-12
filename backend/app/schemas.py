from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str = None

class UserInDB(UserBase):
    id: int
    password_hash: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str
