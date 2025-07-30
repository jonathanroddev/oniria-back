from typing import List
from uuid import uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria import Base


class Biography(Base):
    __tablename__ = "biographies"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet", back_populates="biography"
    )


class HeroicPath(Base):
    __tablename__ = "heroic_paths"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet", back_populates="heroic_path"
    )


class Inventory(Base):
    __tablename__ = "inventories"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet", back_populates="inventory"
    )


class CharacterSheet(Base):
    __tablename__ = "characters_sheets"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    biography_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("biographies.uuid"), nullable=False
    )
    heroic_path_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("heroic_paths.uuid"), nullable=False
    )
    inventory_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("inventories.uuid"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="character_sheet")
    biography: Mapped["Biography"] = relationship(
        "Biography", back_populates="character_sheet"
    )
    heroic_path: Mapped["HeroicPath"] = relationship(
        "HeroicPath", back_populates="character_sheet"
    )
    inventory: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="character_sheet"
    )
    character_renown_history: Mapped[List["CharactersRenownHistory"]] = relationship(
        "CharactersRenownHistory", back_populates="character"
    )


class Renown(Base):
    __tablename__ = "renown"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    experience: Mapped["Experience"] = relationship(
        "Experience", back_populates="renown"
    )
    improvement: Mapped["Improvement"] = relationship(
        "Improvement", back_populates="renown"
    )


class CharacterRenown(Base):
    __tablename__ = "characters_renown"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), nullable=False
    )
    renown_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.name"), nullable=False
    )
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False)

    character_renown_history: Mapped[List["CharactersRenownHistory"]] = relationship(
        "CharactersRenownHistory", back_populates="character_renown"
    )


class CharactersRenownHistory(Base):
    __tablename__ = "characters_renown_history"

    character_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), primary_key=True
    )
    character_renown_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), primary_key=True
    )

    character: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet",
        back_populates="character_renown_history",
        foreign_keys=[character_uuid],
    )
    character_renown: Mapped["CharacterRenown"] = relationship(
        "CharacterRenown",
        back_populates="character_renown_history",
        foreign_keys=[character_renown_uuid],
    )


class Experience(Base):
    __tablename__ = "experiences"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    desc: Mapped[str] = mapped_column(String(100))
    renown_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.name"), nullable=False
    )
    renown: Mapped[List["Renown"]] = relationship("Renown", back_populates="experience")


class Improvement(Base):
    __tablename__ = "improvements"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    desc: Mapped[str] = mapped_column(String(100))
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    renown_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.name"), nullable=False
    )
    renown: Mapped[List["Renown"]] = relationship(
        "Renown", back_populates="improvement"
    )


class ExperienceAcquired(Base):
    __tablename__ = "experiences_acquired"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    experience_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("experiences.uuid"), nullable=False
    )
    character_renown_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)


class ImprovementAcquired(Base):
    __tablename__ = "improvements_acquired"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    improvement_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("improvements.uuid"), nullable=False
    )
    character_renown_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
