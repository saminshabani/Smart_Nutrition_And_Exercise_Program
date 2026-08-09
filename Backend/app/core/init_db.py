from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.config import settings


async def init_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.role == UserRole.admin)
        )

        admin_exists = result.scalars().first()

        if admin_exists is None:
            admin = User(
                username=settings.FIRST_ADMIN_USERNAME,
                email=settings.FIRST_ADMIN_EMAIL,
                hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
                role=UserRole.admin,
                is_active=True,
            )

            session.add(admin)
            await session.commit()

            print(f"[init_db] Admin '{settings.FIRST_ADMIN_USERNAME}' created.")
        else:
            print("[init_db] Admin already exists, skipping.")