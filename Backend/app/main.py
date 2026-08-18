from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.config import settings
from app.routers import auth
from app.core.init_db import init_db
from app.routers.users import router as users_router
from app.routers.food_import import router as foods_router
from app.routers.meal_plan import router as meal_plans_router
from app.routers.profile import router as profiles_router
from app.routers.workout_profile import router as workout_profile_router
from app.routers.workout import router as workout_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users_router)
app.include_router(foods_router)
app.include_router(meal_plans_router)
app.include_router(profiles_router)
app.include_router(workout_profile_router)
app.include_router(workout_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
