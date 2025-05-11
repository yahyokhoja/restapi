from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone_number: str
    password: str

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None

class UserOut(BaseModel):
    id: int
    name: str
    phone_number: str

    class Config:
        orm_mode = True
