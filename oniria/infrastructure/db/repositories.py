from typing import List, Sequence, Optional, Dict
from sqlalchemy import select, UUID, update
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db.sql_models import (
    PlanDB,
    UserDB,
    UserStatusDB,
    GameSessionDB,
    CharacterSheetDB,
    PermissionPlanDB,
    PermissionDB,
    MasterWorkshopDB,
    TranslationDB,
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
                joinedload(UserDB.plan_rel)
                .joinedload(PlanDB.permissions_plans)
                .joinedload(PermissionPlanDB.permission)
                .joinedload(PermissionDB.resource_rel),
                joinedload(UserDB.plan_rel)
                .joinedload(PlanDB.permissions_plans)
                .joinedload(PermissionPlanDB.permission)
                .joinedload(PermissionDB.operation_rel),
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


class TranslationRepository:
    @staticmethod
    def get_all_translations_by_language(
        db_session: Session, lang: str
    ) -> Sequence[TranslationDB]:
        stmt = (
            select(TranslationDB)
            .filter_by(lang=lang)
            .order_by(TranslationDB.table_name, TranslationDB.element_key)
        )
        result = db_session.execute(stmt)
        return result.scalars().all()
