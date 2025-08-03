from typing import List, Sequence, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from oniria.auth.infrastructure.db import Plan
from oniria.auth.infrastructure.db.sql_models import Plan, User, UserStatus


class PlanRepository:
    @staticmethod
    def get_all_plans(db_session: Session) -> Sequence[Plan]:
        stmt = select(Plan)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_plan_by_name(db_session: Session, name: str) -> Optional[Plan]:
        stmt = select(Plan).filter_by(name=name)
        result = db_session.execute(stmt)
        return result.scalars().first()


class UserRepository:
    @staticmethod
    def get_user_by_external_uuid(
        db_session: Session, external_uuid: str
    ) -> Optional[User]:
        stmt = select(User)
        result = db_session.execute(stmt.filter_by(external_uuid=external_uuid))
        return result.scalars().first()

    @staticmethod
    def create_user(db_session: Session, user: User) -> User:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user


class UserStatusRepository:
    @staticmethod
    def get_user_status_by_name(db_session: Session, name: str) -> Optional[UserStatus]:
        stmt = select(UserStatus).filter_by(name=name)
        result = db_session.execute(stmt)
        return result.scalars().first()
