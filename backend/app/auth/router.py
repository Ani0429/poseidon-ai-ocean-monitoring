from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register_user(data: RegisterRequest):
    return {
        "message": "User registered successfully",
        "email": data.email,
        "role": data.role
    }


@router.post("/login")
def login_user(data: LoginRequest):
    return {
        "access_token": "dummy-jwt-token",
        "token_type": "bearer",
        "email": data.email
    }
