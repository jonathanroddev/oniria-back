from typing import List, Optional
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    DateTime,
    func,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4

from oniria.infrastructure.db import Base


class ResourceDB(Base):
    __tablename__ = "resources"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions: Mapped[List["PermissionDB"]] = relationship(
        "PermissionDB", back_populates="resource_rel"
    )


class OperationDB(Base):
    __tablename__ = "operations"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions: Mapped[List["PermissionDB"]] = relationship(
        "PermissionDB", back_populates="operation_rel"
    )


class UserStatusDB(Base):
    __tablename__ = "user_status"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    users: Mapped[Optional[List["UserDB"]]] = relationship(
        "UserDB", back_populates="user_status_rel"
    )


class PlanDB(Base):
    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions_plans: Mapped[List["PermissionPlanDB"]] = relationship(
        "PermissionPlanDB", back_populates="plan_rel"
    )
    permissions: Mapped[List["PermissionDB"]] = relationship(
        "PermissionDB",
        secondary="permissions_plans",
        back_populates="plans",
        viewonly=True,
    )
    users: Mapped[Optional[List["UserDB"]]] = relationship(
        "UserDB", back_populates="plan_rel"
    )


class PermissionDB(Base):
    __tablename__ = "permissions"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    resource: Mapped[str] = mapped_column(
        String(50), ForeignKey("resources.name"), nullable=False
    )
    operation: Mapped[str] = mapped_column(
        String(50), ForeignKey("operations.name"), nullable=False
    )

    __table_args__ = (UniqueConstraint("resource", "operation"),)

    resource_rel: Mapped["ResourceDB"] = relationship(
        "ResourceDB", back_populates="permissions"
    )
    operation_rel: Mapped["OperationDB"] = relationship(
        "OperationDB", back_populates="permissions"
    )
    permissions_plans: Mapped[List["PermissionPlanDB"]] = relationship(
        "PermissionPlanDB", back_populates="permission"
    )
    plans: Mapped[List["PlanDB"]] = relationship(
        "PlanDB",
        secondary="permissions_plans",
        back_populates="permissions",
        viewonly=True,
    )


class PermissionPlanDB(Base):
    __tablename__ = "permissions_plans"

    permission_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissions.uuid"), primary_key=True
    )
    plan: Mapped[str] = mapped_column(
        String(50), ForeignKey("plans.name"), primary_key=True
    )

    permission: Mapped["PermissionDB"] = relationship(
        "PermissionDB", back_populates="permissions_plans"
    )
    plan_rel: Mapped["PlanDB"] = relationship(
        "PlanDB", back_populates="permissions_plans"
    )


class UserDB(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    external_uuid: Mapped[str] = mapped_column(String(50), nullable=False)
    dreamer_tag: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    user_status: Mapped[str] = mapped_column(
        String(50), ForeignKey("user_status.name"), nullable=False
    )
    plan: Mapped[str] = mapped_column(
        String(50), ForeignKey("plans.name"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=None
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user_status_rel: Mapped["UserStatusDB"] = relationship(
        "UserStatusDB", back_populates="users"
    )
    plan_rel: Mapped["PlanDB"] = relationship("PlanDB", back_populates="users")
    characters_sheets: Mapped[List["CharacterSheetDB"]] = relationship(
        "CharacterSheetDB", back_populates="user"
    )
    masters_workshops: Mapped[List["MasterWorkshopDB"]] = relationship(
        "MasterWorkshopDB", back_populates="user"
    )


class GameSessionDB(Base):
    __tablename__ = "games_sessions"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    owner: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=True)
    max_players: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=None
    )
    character_sheets: Mapped[Optional[List["CharacterSheetDB"]]] = relationship(
        "CharacterSheetDB", back_populates="game_session"
    )
    master_workshop: Mapped["MasterWorkshopDB"] = relationship(
        "MasterWorkshopDB", back_populates="game_session"
    )


class CharacterSheetDB(Base):
    __tablename__ = "characters_sheets"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    game_session_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("games_sessions.uuid"), nullable=True
    )

    user: Mapped["UserDB"] = relationship("UserDB", back_populates="characters_sheets")
    game_session: Mapped[Optional["GameSessionDB"]] = relationship(
        "GameSessionDB", back_populates="character_sheets"
    )


class MasterWorkshopDB(Base):
    __tablename__ = "masters_workshops"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=None
    )
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    game_session_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("games_sessions.uuid"),
        nullable=False,
        unique=True,
    )

    user: Mapped["UserDB"] = relationship("UserDB", back_populates="masters_workshops")
    game_session: Mapped["GameSessionDB"] = relationship(
        "GameSessionDB", back_populates="master_workshop"
    )


class TranslationDB(Base):
    __tablename__ = "translations"

    element_key: Mapped[str] = mapped_column(String(100), primary_key=True)
    property: Mapped[str] = mapped_column(String(50), primary_key=True)
    lang: Mapped[str] = mapped_column(String(5), primary_key=True)  # ISO 639-1
    display_text: Mapped[str] = mapped_column(Text, nullable=False)
