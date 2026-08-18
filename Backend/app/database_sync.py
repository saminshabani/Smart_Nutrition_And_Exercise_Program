"""
app/database_sync.py

یک engine و SessionLocal کاملاً sync و مستقل، فقط برای ماژول ورزش (repository،
routerها، و seed_exercises.py). بقیه‌ی پروژه همچنان از app/database.py
(async) استفاده می‌کنه؛ این دو تا هیچ تداخلی با هم ندارن چون هردو فقط
دارن به یک دیتابیس Postgres یکسان وصل می‌شن، هرکدوم با درایور خودشون.

نیازمندی: pip install psycopg2-binary   (اگه از قبل نصب نیست)
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings;

#   postgresql+asyncpg://user:pass@host:5432/dbname

_raw_url = settings.DATABASE_URL
if not _raw_url:
    raise RuntimeError("DATABASE_URL پیدا نشد - مسیر خوندنش رو با config.py خودت هماهنگ کن.")

SYNC_DATABASE_URL = _raw_url.replace("postgresql+asyncpg://", "postgresql://")

sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


def get_db_sync():
    """Dependency برای FastAPI routerهای ماژول ورزش - مثل get_db ولی sync."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()