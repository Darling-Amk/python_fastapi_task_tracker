from abc import ABC, abstractmethod

from sqlalchemy import insert, select, delete

from app.db import async_session


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, abstract_id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self) -> list:
        """
        Метод работает с моделями и возвращает их read версию.

        Returns:
            read схему таблицы
        """
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def get_model_by_id(self, abstract_id: int):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == abstract_id)
            res = await session.execute(stmt)
            data = res.scalar_one_or_none()
            return data

    async def get_read_model_by_id(self, abstract_id: int):
        data = await self.get_model_by_id(abstract_id)
        if data is not None:
            return data.to_read_model()
        return None

    async def delete_one(self, abstract_id: int) -> None:
        async with async_session() as session:
            stmt = delete(self.model).where(self.model.id == abstract_id)
            res = await session.execute(stmt)
            await session.commit()  # Сохраняем изменения

    async def update_one(self, model):
        async with async_session() as session:
            session.add(model)
            await session.commit()  # Сохраняем изменения
            await session.refresh(model)  # Обновляем объект после сохранения
        return model.to_read_model()
