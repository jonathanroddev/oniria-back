from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria.db import Base


class Avatar(Base):
    __tablename__ = "avatars"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet", back_populates="avatar"
    )


class Oneironaut(Base):
    __tablename__ = "oneironauts"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet", back_populates="oneironaut"
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
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    avatar_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("avatars.uuid"), nullable=False
    )
    oneironaut_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("oneironauts.uuid"), nullable=False
    )
    inventory_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("inventories.uuid"), nullable=False
    )
    game_session_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game_sessions.uuid"), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="characters_sheets")
    avatar: Mapped["Avatar"] = relationship("Avatar", back_populates="character_sheet")
    oneironaut: Mapped["Oneironaut"] = relationship(
        "Oneironaut", back_populates="character_sheet"
    )
    inventory: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="character_sheet"
    )
    game_session: Mapped[Optional["GameSession"]] = relationship(
        "GameSession", back_populates="character_sheets"
    )
    character_renown_history: Mapped[List["CharactersRenownHistory"]] = relationship(
        "CharactersRenownHistory", back_populates="character"
    )


class MasterWorkshop(Base):
    __tablename__ = "masters_workshops"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    game_session_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game_sessions.uuid"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="masters_workshops")
    game_session: Mapped["GameSession"] = relationship(
        "GameSession", back_populates="master_workshop"
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
