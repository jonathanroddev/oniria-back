from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria.db import Base


class AvatarDB(Base):
    __tablename__ = "avatars"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheetDB"] = relationship(
        "CharacterSheetDB", back_populates="avatar"
    )


class OneironautDB(Base):
    __tablename__ = "oneironauts"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheetDB"] = relationship(
        "CharacterSheetDB", back_populates="oneironaut"
    )


class InventoryDB(Base):
    __tablename__ = "inventories"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    character_sheet: Mapped["CharacterSheetDB"] = relationship(
        "CharacterSheetDB", back_populates="inventory"
    )


class CharacterSheetDB(Base):
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

    user: Mapped["User"] = relationship("UserDB", back_populates="characters_sheets")
    avatar: Mapped["AvatarDB"] = relationship(
        "AvatarDB", back_populates="character_sheet"
    )
    oneironaut: Mapped["OneironautDB"] = relationship(
        "OneironautDB", back_populates="character_sheet"
    )
    inventory: Mapped["InventoryDB"] = relationship(
        "InventoryDB", back_populates="character_sheet"
    )
    game_session: Mapped[Optional["GameSession"]] = relationship(
        "GameSessionDB", back_populates="character_sheets"
    )
    character_renown_history: Mapped[List["CharactersRenownHistoryDB"]] = relationship(
        "CharactersRenownHistoryDB", back_populates="character"
    )


class MasterWorkshopDB(Base):
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

    user: Mapped["User"] = relationship("UserDB", back_populates="masters_workshops")
    game_session: Mapped["GameSession"] = relationship(
        "GameSessionDB", back_populates="master_workshop"
    )


class RenownDB(Base):
    __tablename__ = "renown"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    experience: Mapped["ExperienceDB"] = relationship(
        "ExperienceDB", back_populates="renown"
    )
    improvement: Mapped["ImprovementDB"] = relationship(
        "ImprovementDB", back_populates="renown"
    )


class CharacterRenownDB(Base):
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

    character_renown_history: Mapped[List["CharactersRenownHistoryDB"]] = relationship(
        "CharactersRenownHistoryDB", back_populates="character_renown"
    )


class CharactersRenownHistoryDB(Base):
    __tablename__ = "characters_renown_history"

    character_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), primary_key=True
    )
    character_renown_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), primary_key=True
    )

    character: Mapped["CharacterSheetDB"] = relationship(
        "CharacterSheetDB",
        back_populates="character_renown_history",
        foreign_keys=[character_uuid],
    )
    character_renown: Mapped["CharacterRenownDB"] = relationship(
        "CharacterRenownDB",
        back_populates="character_renown_history",
        foreign_keys=[character_renown_uuid],
    )


class ExperienceDB(Base):
    __tablename__ = "experiences"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    desc: Mapped[str] = mapped_column(String(100))
    renown_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.name"), nullable=False
    )
    renown: Mapped[List["RenownDB"]] = relationship(
        "RenownDB", back_populates="experience"
    )


class ImprovementDB(Base):
    __tablename__ = "improvements"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    desc: Mapped[str] = mapped_column(String(100))
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    renown_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.name"), nullable=False
    )
    renown: Mapped[List["RenownDB"]] = relationship(
        "RenownDB", back_populates="improvement"
    )


class ExperienceAcquiredDB(Base):
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


class ImprovementAcquiredDB(Base):
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
