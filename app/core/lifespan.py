from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.db import engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Обработчик жизненного цикла приложения"""
    # Выполняется при старте приложения
    async with engine.begin() as conn:
        print("Initializing the database...")
        engine.sync_engine.echo = False
        await init_db()
        engine.sync_engine.echo = True
        await conn.run_sync(lambda x: print("Database initialized"))

    yield  # Здесь приложение запускается

    # Выполняется при завершении работы приложения
    print("Shutting down application...")
    await engine.dispose()