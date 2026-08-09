import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.config import settings
from app.database import Base

async def create_admin():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.email == "admin@example.com"))
        if result.scalar_one_or_none():
            print("Admin already exists!")
            return

        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.admin,
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        print("Admin created successfully!")

if __name__ == "__main__":
    asyncio.run(create_admin())
