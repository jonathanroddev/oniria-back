from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from oniria import Base


class Resource(Base):
    __tablename__ = "resources"
    name = Column(String(50), primary_key=True)
    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )


class Operation(Base):
    __tablename__ = "operations"
    name = Column(String(50), primary_key=True)
    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )


class Plan(Base):
    __tablename__ = "plans"
    name = Column(String(50), primary_key=True)
    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )


class PlayerType(Base):
    __tablename__ = "players_types"
    name = Column(String(50), primary_key=True)
    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )


class UserStatus(Base):
    __tablename__ = "user_status"
    name = Column(String(50), primary_key=True)
    __table_args__ = (
        CheckConstraint("TRIM(BOTH FROM name) <> ''", name="check_empty_name"),
    )


class Permission(Base):
    __tablename__ = "permissions"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resource = Column(String(50), ForeignKey("resources.name"), nullable=False)
    operation = Column(String(50), ForeignKey("operations.name"), nullable=False)

    __table_args__ = (UniqueConstraint("resource", "operation"),)

    resource_rel = relationship("Resource", back_populates="permissions")
    operation_rel = relationship("Operation", back_populates="permissions")


class PermissionPlanPlayerType(Base):
    __tablename__ = "permissions_plans_player_type"
    permission_uuid = Column(
        UUID(as_uuid=True), ForeignKey("permissions.uuid"), primary_key=True
    )
    plan = Column(String(50), ForeignKey("plans.name"), primary_key=True)
    player_type = Column(String(50), ForeignKey("players_types.name"), primary_key=True)


class GameSession(Base):
    __tablename__ = "game_session"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class User(Base):
    __tablename__ = "users"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    external_uuid = Column(String(50), nullable=False)
    player_type = Column(String(50), ForeignKey("players_types.name"), nullable=False)
    user_status = Column(String(50), ForeignKey("user_status.name"), nullable=False)
    plan = Column(String(50), ForeignKey("plans.name"), nullable=False)
    game_session_uuid = Column(
        UUID(as_uuid=True), ForeignKey("game_session.uuid"), nullable=False
    )
    character_sheet_uuid = Column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), nullable=False
    )

    game_session = relationship("GameSession")
    character_sheet = relationship("CharacterSheet")
