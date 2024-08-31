from sqlalchemy.dialects.postgresql import TIMESTAMP, ARRAY, REAL
from sqlalchemy import Column, String, BigInteger, ForeignKey, UniqueConstraint
from src.db import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


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

    def __repr__(self):
        return f"{self.id}-{self.machine_name}"


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

    def __repr__(self):
        return f"{self.id}-{self.name}"


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
