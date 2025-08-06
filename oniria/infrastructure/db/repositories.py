from typing import List, Sequence, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db.sql_models import (
    PlanDB,
    UserDB,
    UserStatusDB,
    GameSessionDB,
)


class PlanRepository:
    @staticmethod
    def get_all_plans(db_session: Session) -> Sequence[PlanDB]:
        stmt = select(PlanDB)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_plan_by_name(db_session: Session, name: str) -> Optional[PlanDB]:
        stmt = select(PlanDB).filter_by(name=name)
        result = db_session.execute(stmt)
        return result.scalars().first()


class UserRepository:
    @staticmethod
    def get_user_by_external_uuid(
        db_session: Session, external_uuid: str
    ) -> Optional[UserDB]:
        stmt = select(UserDB)
        result = db_session.execute(
            stmt.filter_by(external_uuid=external_uuid).options(
                joinedload(UserDB.plan_rel),
                joinedload(UserDB.user_status_rel),
                joinedload(UserDB.characters_sheets),
                joinedload(UserDB.masters_workshops),
            )
        )
        return result.scalars().first()

    @staticmethod
    def create_user(db_session: Session, user: UserDB) -> UserDB:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user


class UserStatusRepository:
    @staticmethod
    def get_user_status_by_name(
        db_session: Session, name: str
    ) -> Optional[UserStatusDB]:
        stmt = select(UserStatusDB).filter_by(name=name)
        result = db_session.execute(stmt)
        return result.scalars().first()


class GameSessionRepository:
    @staticmethod
    def get_game_session_by_uuid(
        db_session: Session, uuid: str
    ) -> Optional[GameSessionDB]:
        stmt = select(GameSessionDB).filter_by(uuid=uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def create_game_session(
        db_session: Session, game_session: GameSessionDB
    ) -> GameSessionDB:
        db_session.add(game_session)
        db_session.commit()
        db_session.refresh(game_session)
        return game_session

    @staticmethod
    def get_game_sessions_by_owner(
        db_session: Session, owner_uuid: str
    ) -> Sequence[GameSessionDB]:
        stmt = select(GameSessionDB).filter_by(owner=owner_uuid)
        result = db_session.execute(stmt)
        return result.scalars().all()
