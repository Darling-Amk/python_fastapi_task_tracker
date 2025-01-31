from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from app.api.models import Base
from app.core import app_config

# Создаем асинхронный движок для работы с БД
engine = create_async_engine(
    url=app_config.pg.database_url,  # URL базы данных
    pool_size=app_config.pg.pool_size,  # Максимальное количество единовременных подключений
    max_overflow=0,  # Максимальное количество дополнительных подключений
    echo=True,  # Логирование SQL-запросов (можно отключить в продакшене)
    future=True,  # Использование новой API SQLAlchemy
)

# Создаем асинхронную фабрику сессий
async_session = async_sessionmaker(
    engine,  # Привязываем сессии к асинхронному движку
    expire_on_commit=False,  # Сессия не сбрасывает объекты при коммите
)


async def init_db():
    """
    Метод инициализации базы данных алхимией
    """
    async with engine.begin() as conn:
        # Создание всех таблиц
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
