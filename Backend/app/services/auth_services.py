from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models import User, Profile, RefreshToken
from app.schemas.schema import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.config import settings


class AuthService:
    @staticmethod
    async def register(data: RegisterRequest, db: AsyncSession) -> tuple[str, str]:
        result = await db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = User(
            email=data.email,
            password_hash=hash_password(data.password)
        )
        db.add(user)
        await db.flush()

        profile = Profile(user_id=user.id)
        db.add(profile)

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        rt = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(rt)
        await db.commit()

        return access_token, refresh_token

    @staticmethod
    async def login(data: LoginRequest, db: AsyncSession) -> tuple[str, str]:
        result = await db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account disabled"
            )

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        rt = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(rt)
        await db.commit()

        return access_token, refresh_token

    @staticmethod
    async def refresh_tokens(refresh_token: str, db: AsyncSession) -> tuple[str, str]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token == refresh_token)
        )
        rt = result.scalar_one_or_none()
        if not rt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found"
            )

        await db.delete(rt)

        user_id = int(payload["sub"])
        new_access = create_access_token(user_id)
        new_refresh = create_refresh_token(user_id)

        new_rt = RefreshToken(
            user_id=user_id,
            token=new_refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_rt)
        await db.commit()

        return new_access, new_refresh

    @staticmethod
    async def logout(refresh_token: str, db: AsyncSession) -> None:
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token == refresh_token)
        )
        rt = result.scalar_one_or_none()
        if rt:
            await db.delete(rt)
            await db.commit()
