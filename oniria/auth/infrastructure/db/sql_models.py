from typing import List, Optional

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4

from oniria.db import Base
from oniria.campaign.infrastructure.db import CharacterSheet


class Resource(Base):
    __tablename__ = "resources"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", back_populates="resource_rel"
    )


class Operation(Base):
    __tablename__ = "operations"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", back_populates="operation_rel"
    )


class Plan(Base):
    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions_plans_player_types: Mapped[List["PermissionPlanPlayerType"]] = (
        relationship("PermissionPlanPlayerType", back_populates="plan_rel")
    )
    users: Mapped[List["User"]] = relationship("User", backref="plan_rel")


class PlayerType(Base):
    __tablename__ = "players_types"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    permissions_plans_player_types: Mapped[List["PermissionPlanPlayerType"]] = (
        relationship("PermissionPlanPlayerType", back_populates="player_type_rel")
    )
    users: Mapped[List["User"]] = relationship("User", backref="player_type_rel")


class UserStatus(Base):
    __tablename__ = "user_status"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)

    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )

    users: Mapped[List["User"]] = relationship("User", backref="user_status_rel")


class Permission(Base):
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

    resource_rel: Mapped["Resource"] = relationship(
        "Resource", back_populates="permissions"
    )
    operation_rel: Mapped["Operation"] = relationship(
        "Operation", back_populates="permissions"
    )
    permissions_plans_player_types: Mapped[List["PermissionPlanPlayerType"]] = (
        relationship("PermissionPlanPlayerType", back_populates="permission")
    )


class PermissionPlanPlayerType(Base):
    __tablename__ = "permissions_plans_player_type"

    permission_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissions.uuid"), primary_key=True
    )
    plan: Mapped[str] = mapped_column(
        String(50), ForeignKey("plans.name"), primary_key=True
    )
    player_type: Mapped[str] = mapped_column(
        String(50), ForeignKey("players_types.name"), primary_key=True
    )

    permission: Mapped["Permission"] = relationship(
        "Permission", back_populates="permissions_plans_player_types"
    )
    plan_rel: Mapped["Plan"] = relationship(
        "Plan", back_populates="permissions_plans_player_types"
    )
    player_type_rel: Mapped["PlayerType"] = relationship(
        "PlayerType", back_populates="permissions_plans_player_types"
    )


class GameSession(Base):
    __tablename__ = "game_sessions"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    users: Mapped[List["User"]] = relationship("User", back_populates="game_sessions")


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    external_uuid: Mapped[str] = mapped_column(String(50), nullable=False)
    player_type: Mapped[str] = mapped_column(
        String(50), ForeignKey("players_types.name"), nullable=False
    )
    user_status: Mapped[str] = mapped_column(
        String(50), ForeignKey("user_status.name"), nullable=False
    )
    plan: Mapped[str] = mapped_column(
        String(50), ForeignKey("plans.name"), nullable=False
    )
    game_sessions_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game_sessions.uuid"), nullable=False
    )
    character_sheet_uuid: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), nullable=True
    )

    game_sessions: Mapped["GameSession"] = relationship(
        "GameSession", back_populates="users"
    )
    character_sheet: Mapped["CharacterSheet"] = relationship(
        "CharacterSheet", back_populates="user"
    )
