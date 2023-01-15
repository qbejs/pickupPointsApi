import json
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, JSON
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
Base: DeclarativeMeta = declarative_base()
encoder = json.JSONEncoder()
decoder = json.JSONDecoder()


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model"""

    roles = Column(JSON, nullable=True, default=encoder.encode(["ROLE_USER"]))

    def get_roles(self) -> list:
        return decoder.decode(self.roles)

    def set_role(self, role: str) -> list:
        roles = self.get_roles()
        roles.append(role)
        self.roles = encoder.encode(roles)
        return roles

    def remove_role(self, role: str) -> list:
        roles = self.get_roles()
        roles.remove(role)
        self.roles = encoder.encode(roles)
        return roles

    def has_role(self, role: str) -> bool:
        roles = self.get_roles()
        if role not in roles:
            return False
        return True

    def get_info(self) -> dict:
        return {
            "id": self.id,
            "username": self.email,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_superuser": self.is_superuser,
            "roles": self.get_roles(),
        }


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
