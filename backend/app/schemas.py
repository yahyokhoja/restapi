from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone_number: str
    password: str

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    phone_number: str
    password: str

    model_config = {
        "from_attributes": True
    }

class UserOut(BaseModel):
    id: int
    name: str
    phone_number: str

    model_config = {
        "from_attributes": True
    }
