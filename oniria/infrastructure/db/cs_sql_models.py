from typing import List

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria.infrastructure.db import Base


class RenownDB(Base):
    __tablename__ = "renown"

    key: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    lucidity_points: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_level: Mapped[int] = mapped_column(Integer, nullable=False)
    karma_points: Mapped[int] = mapped_column(Integer, nullable=False)
    totems_base: Mapped[int] = mapped_column(Integer, nullable=False)
    mantras_base: Mapped[int] = mapped_column(Integer, nullable=False)
    recipes_base: Mapped[int] = mapped_column(Integer, nullable=False)
    books_base: Mapped[int] = mapped_column(Integer, nullable=False)
    max_improvements: Mapped[int] = mapped_column(Integer, nullable=False)
    max_experiences: Mapped[int] = mapped_column(Integer, nullable=False)

    improvements: Mapped[List["ImprovementDB"]] = relationship(
        "ImprovementDB", back_populates="renown"
    )


class ExperienceDB(Base):
    __tablename__ = "experiences"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)


class ImprovementDB(Base):
    __tablename__ = "improvements"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    renown_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.key"), nullable=False
    )
    renown: Mapped[List["RenownDB"]] = relationship(
        "RenownDB", back_populates="improvements"
    )
