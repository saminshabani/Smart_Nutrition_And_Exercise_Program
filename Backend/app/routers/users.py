# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
#
# from app.database import get_db
# from app.models import User, Profile
# from app.schemas.schema import UserResponse, ProfileUpdate, ProfileResponse
# from app.core.security import get_current_user
#
# router = APIRouter(prefix="/users", tags=["users"])
#
#
# @router.get("/me", response_model=UserResponse)
# async def get_me(current_user: User = Depends(get_current_user)):
#     """Get current authenticated user information"""
#     return current_user
#
#
# @router.get("/me/profile", response_model=ProfileResponse)
# async def get_profile(
#         current_user: User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db)
# ):
#     """Get current user's profile"""
#     result = await db.execute(
#         select(Profile).where(Profile.user_id == current_user.id)
#     )
#     profile = result.scalar_one_or_none()
#
#     if not profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Profile not found"
#         )
#
#     return profile
#
#
# @router.patch("/me/profile", response_model=ProfileResponse)
# async def update_profile(
#         body: ProfileUpdate,
#         current_user: User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db)
# ):
#     """Update current user's profile"""
#     result = await db.execute(
#         select(Profile).where(Profile.user_id == current_user.id)
#     )
#     profile = result.scalar_one_or_none()
#
#     if not profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Profile not found"
#         )
#
#     update_data = body.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(profile, field, value)
#
#     await db.commit()
#     await db.refresh(profile)
#
#     return profile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserOut, UserUpdate
from app.core.deps import get_current_user
from pydantic import BaseModel, EmailStr
from app.core.security import hash_password
router = APIRouter(prefix="/users", tags=["users"])


def require_role(*roles: UserRole):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return checker


class AdminCreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def admin_create_user(
    data: AdminCreateUser,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.admin)),
):
    # چک تکراری
    result = await db.execute(
        select(User).where((User.username == data.username) | (User.email == data.email))
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserOut)
async def update_me(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.username:
        current_user.username = data.username
    if data.email:
        current_user.email = data.email
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.admin)),
):
    result = await db.execute(select(User))
    return result.scalars().all()
