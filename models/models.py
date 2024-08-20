import asyncio
import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, ARRAY, REAL

from sqlalchemy import Column, String, BigInteger, Boolean, Integer, ForeignKey, select, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column, selectinload

from config import *

engine = create_async_engine(
    f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:5432/{TEST_DB_NAME}",
    # f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}",
    echo=True, future=True)

Base = declarative_base()


class Machine(Base):
    __tablename__ = 'main_machine'

    id = Column(BigInteger, primary_key=True)
    machine_name: Mapped[str]
    startup_status: Mapped[bool]
    status: Mapped[bool]
    write_way: Mapped[str | None]
    start_time: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP(timezone=True))
    loadfile_path: Mapped[str | None]
    hot_reload: Mapped[str]
    ready_ip: Mapped[ARRAY] = mapped_column(ARRAY(String()), nullable=True)
    check_time: Mapped[int]
    input_command: Mapped[str]

    names: Mapped[list['Name']] = relationship(
        back_populates='machines',
        secondary='main_name_machine'
    )
    compiles: Mapped[list['MegaCompile']] = relationship(
        back_populates='machine'
    )


class Name(Base):
    __tablename__ = 'main_name'

    id = Column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    machines: Mapped[list['Machine']] = relationship(
        back_populates='names',
        secondary="main_name_machine"
    )
    compiles: Mapped[list["MegaCompile"]] = relationship(
        back_populates='name'
    )


class NameMachine(Base):
    __tablename__ = 'main_name_machine'
    __table_args__ = (
        UniqueConstraint('name_id', 'machine_id'),
    )

    id = mapped_column(BigInteger, primary_key=True)
    name_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('main_name.id', ondelete="CASCADE"))
    machine_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('main_machine.id', ondelete="CASCADE"))


class MegaCompile(Base):
    __tablename__ = 'main_megacompila'
    id = mapped_column(BigInteger, primary_key=True)
    value: Mapped[REAL | None] = mapped_column(REAL)
    get_time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True))
    analog: Mapped[bool]
    unit: Mapped[str]

    name_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('main_name.id'))
    machine_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('main_machine.id', ondelete="CASCADE"))

    name: Mapped["Name"] = relationship(
        back_populates='compiles'
    )

    machine: Mapped["Machine"] = relationship(
        back_populates='compiles'
    )


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_machine(machine_name: str = None):
    async with async_session() as ses:
        q = (
            select(Machine)
            .options(selectinload(Machine.names))
            .filter(Machine.machine_name == 'Bentec')
        )
        res = await ses.scalars(q)


async def load_all():
    async with async_session() as ses:
        res = await ses.execute(select(Name).filter())
        return res.scalars().all()


async def insert_machine():
    bentec = Machine(machine_name='Bentec', startup_status=False, status=1, write_way='none', start_time=datetime.now(),
                     hot_reload='none', ready_ip=['10.49.14.1', '10.49.16.1'], check_time=0, input_command='none')
    gaz = Machine(machine_name='gaz', startup_status=False, status=1, write_way='none', start_time=datetime.now(),
                  hot_reload='none', ready_ip=['10.49.14.1', '10.49.16.1'], check_time=0, input_command='none')
    async with async_session() as session:
        res = session.add_all([bentec, gaz])
        await session.commit()
        print(res)


if __name__ == "__main__":
    # asyncio.run(create_tables())
    asyncio.run(insert_machine())
    # asyncio.run(get_machine())
