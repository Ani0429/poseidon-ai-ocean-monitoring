from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    role: str  # admin | scientist | public

class UserLogin(BaseModel):
    email: str
    password: str
