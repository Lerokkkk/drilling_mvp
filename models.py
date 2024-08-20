from typing import List, Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, DateTime, Float, ForeignKeyConstraint, \
    Identity, Index, Integer, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()


class MainMachine(Base):
    __tablename__ = 'main_machine'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='main_machine_pkey'),
    )

    id = Column(BigInteger, primary_key=True)
    machine_name = Column(String, nullable=False)
    startup_status = Column(Boolean, nullable=False)
    status = Column(Boolean, nullable=False)
    hot_reload = Column(String, nullable=False)
    check_time = Column(Integer, nullable=False)
    input_command = Column(String, nullable=False)
    write_way = Column(String)
    start_time = Column(TIMESTAMP, timezone=True)
    loadfile_path = Column(String)
    ready_ip = Column(ARRAY(String()))

    main_megacompila: Mapped[List['MainMegacompila']] = relationship('MainMegacompila', uselist=True,
                                                                     back_populates='machine')
    main_name_machine: Mapped[List['MainNameMachine']] = relationship('MainNameMachine', uselist=True,
                                                                      back_populates='machine')


class MainName(Base):
    __tablename__ = 'main_name'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='main_name_pkey'),
        UniqueConstraint('name', name='main_name_name_key'),
        Index('main_name_name_bedab4d2_like', 'name')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9_223_372_036_854_775_807, cycle=False, cache=1))
    name = mapped_column(String, nullable=False)

    main_megacompila: Mapped[List['MainMegacompila']] = relationship('MainMegacompila', uselist=True,
                                                                     back_populates='name')
    main_name_machine: Mapped[List['MainNameMachine']] = relationship('MainNameMachine', uselist=True,
                                                                      back_populates='name')


class MainMegacompila(Base):
    __tablename__ = 'main_megacompila'
    __table_args__ = (
        ForeignKeyConstraint(['machine_id'], ['main_machine.id'], deferrable=True, initially='DEFERRED',
                             name='main_megacompila_machine_id_524bb3ac_fk_main_machine_id'),
        ForeignKeyConstraint(['name_id'], ['main_name.id'], deferrable=True, initially='DEFERRED',
                             name='main_megacompila_name_id_f370b09a_fk_main_name_id'),
        PrimaryKeyConstraint('id', name='main_megacompila_pkey'),
        Index('main_megaco_name_id_a46229_idx', 'name_id', 'machine_id', 'get_time'),
        Index('main_megacompila_machine_id_524bb3ac', 'machine_id'),
        Index('main_megacompila_name_id_f370b09a', 'name_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    get_time = mapped_column(DateTime(True), nullable=False)
    analog = mapped_column(Boolean, nullable=False)
    unit = mapped_column(String, nullable=False)
    name_id = mapped_column(BigInteger, nullable=False)
    machine_id = mapped_column(BigInteger, nullable=False)
    value = mapped_column(Float)

    machine: Mapped['MainMachine'] = relationship('MainMachine', back_populates='main_megacompila')
    name: Mapped['MainName'] = relationship('MainName', back_populates='main_megacompila')


class MainNameMachine(Base):
    __tablename__ = 'main_name_machine'
    __table_args__ = (
        ForeignKeyConstraint(['machine_id'], ['main_machine.id'], deferrable=True, initially='DEFERRED',
                             name='main_name_machine_machine_id_7a01ebcb_fk_main_machine_id'),
        ForeignKeyConstraint(['name_id'], ['main_name.id'], deferrable=True, initially='DEFERRED',
                             name='main_name_machine_name_id_52a22dd8_fk_main_name_id'),
        PrimaryKeyConstraint('id', name='main_name_machine_pkey'),
        UniqueConstraint('name_id', 'machine_id', name='main_name_machine_name_id_machine_id_e8ce6328_uniq'),
        Index('main_name_machine_machine_id_7a01ebcb', 'machine_id'),
        Index('main_name_machine_name_id_52a22dd8', 'name_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name_id = mapped_column(BigInteger, nullable=False)
    machine_id = mapped_column(BigInteger, nullable=False)

    machine: Mapped['MainMachine'] = relationship('MainMachine', back_populates='main_name_machine')
    name: Mapped['MainName'] = relationship('MainName', back_populates='main_name_machine')
