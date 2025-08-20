import enum
from typing import List

from sqlalchemy import ForeignKey, String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria.infrastructure.db import Base


class RenownDB(Base):
    __tablename__ = "renown"

    key: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
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
        String(50), ForeignKey("renown.key"), nullable=False, primary_key=True
    )
    renown: Mapped["RenownDB"] = relationship("RenownDB", back_populates="improvements")


class PhilosophyDB(Base):
    __tablename__ = "philosophies"
    key: Mapped[str] = mapped_column(String(100), primary_key=True)


class TemperamentDB(Base):
    __tablename__ = "temperaments"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class DreamPhaseDB(Base):
    __tablename__ = "dream_phases"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class WeaknessDB(Base):
    __tablename__ = "weaknesses"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class SomnaAffinityDB(Base):
    __tablename__ = "somna_affinities"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)


class SkillDB(Base):
    __tablename__ = "skills"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class MartialDB(Base):
    __tablename__ = "martials"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class ManeuverTypeDB(enum.Enum):
    common = "common"
    advanced = "advanced"


class ManeuverDB(Base):
    __tablename__ = "maneuvers"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ManeuverTypeDB] = mapped_column(Enum(ManeuverTypeDB), nullable=False)
    requires_magic: Mapped[bool] = mapped_column(Boolean, default=False)


class EssenceDB(Base):
    __tablename__ = "essences"

    key: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)

    spells: Mapped[list["SpellDB"]] = relationship(back_populates="essence")


class SpellDB(Base):
    __tablename__ = "spells"

    key: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False)
    essence_key: Mapped[str] = mapped_column(ForeignKey("essences.key"), nullable=False)
    tier: Mapped[int] = mapped_column(Integer, nullable=False)

    essence: Mapped["EssenceDB"] = relationship(back_populates="spells")


class RecipeTypeDB(enum.Enum):
    brew = "brew"
    poison = "poison"


class RecipeDB(Base):
    __tablename__ = "recipes"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[RecipeTypeDB] = mapped_column(Enum(RecipeTypeDB), nullable=False)
