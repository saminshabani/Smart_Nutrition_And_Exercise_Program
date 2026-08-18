# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.database import get_db
# from app.schemas.schema import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
# from app.services.auth_services import AuthService
#
# router = APIRouter(prefix="/auth", tags=["auth"])
#
#
# @router.post("/register", response_model=TokenResponse, status_code=201)
# async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
#     access, refresh = await AuthService.register(body, db)
#     return TokenResponse(access_token=access, refresh_token=refresh)
#
#
# @router.post("/login", response_model=TokenResponse)
# async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
#     access, refresh = await AuthService.login(body, db)
#     return TokenResponse(access_token=access, refresh_token=refresh)
#
#
# @router.post("/refresh", response_model=TokenResponse)
# async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
#     access, refresh = await AuthService.refresh_tokens(body.refresh_token, db)
#     return TokenResponse(access_token=access, refresh_token=refresh)
#
#
# @router.post("/logout")
# async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
#     await AuthService.logout(body.refresh_token, db)
#     return {"message": "Logged out"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut
from app.core.security import hash_password, create_access_token, verify_password
from app.core.deps import get_current_user
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # چک کنیم username یا email تکراری نباشه
    result = await db.execute(
        select(User).where((User.username == data.username) | (User.email == data.email))
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # کاربر جدید همیشه با role=user ساخته میشه
    new_user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.user,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    token = create_access_token(user_id=user.id)
    return {"access_token": token}

class LogoutRequest(BaseModel):
    refresh_token: str


@router.post("/logout")
async def logout(
    body: LogoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # در صورت وجود AuthService برای ابطال توکن:
    # await AuthService.logout(body.refresh_token, db)
    return {"message": "Successfully logged out"}