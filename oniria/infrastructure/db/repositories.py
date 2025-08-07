from typing import List, Sequence, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db import MasterWorkshopDB
from oniria.infrastructure.db.sql_models import (
    PlanDB,
    UserDB,
    UserStatusDB,
    GameSessionDB,
    CharacterSheetDB,
    AvatarDB,
    OneironautDB,
    InventoryDB,
    PermissionPlanDB,
    PermissionDB,
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

    @staticmethod
    def get_game_session_by_uuid_and_owner(
        db_session: Session, uuid: str, owner_uuid: str
    ) -> Optional[GameSessionDB]:
        stmt = (
            select(GameSessionDB)
            .filter_by(uuid=uuid, owner=owner_uuid)
            .options(selectinload(GameSessionDB.master_workshop))
        )
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_public_games_sessions(db_session: Session) -> Sequence[GameSessionDB]:
        stmt = select(GameSessionDB).filter_by(password=None)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_game_session_by_name(
        db_session: Session, name: str
    ) -> Optional[GameSessionDB]:
        stmt = select(GameSessionDB).filter_by(name=name)
        result = db_session.execute(stmt)
        return result.scalars().first()


class MasterWorkshopRepository:
    @staticmethod
    def create_master_workshop(
        db_session: Session, master_workshop: MasterWorkshopDB
    ) -> MasterWorkshopDB:
        db_session.add(master_workshop)
        db_session.commit()
        db_session.refresh(master_workshop)
        return master_workshop

    @staticmethod
    def get_master_workshop_by_game_session_uuid(
        db_session: Session, game_session_uuid: str
    ) -> Optional[MasterWorkshopDB]:
        stmt = select(MasterWorkshopDB).filter_by(game_session_uuid=game_session_uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()


class CharacterSheetRepository:
    @staticmethod
    def create_character_sheet(
        db_session: Session, character_sheet: CharacterSheetDB
    ) -> CharacterSheetDB:
        db_session.add(character_sheet)
        db_session.commit()
        db_session.refresh(character_sheet)
        return character_sheet

    @staticmethod
    def get_character_sheet_by_user_uuid(
        db_session: Session, user_uuid: str
    ) -> Optional[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(user_uuid=user_uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_characters_sheets_by_game_session_uuid(
        db_session: Session, game_session_uuid: str
    ) -> Sequence[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(game_session_uuid=game_session_uuid)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_character_sheet_by_user_uuid_and_game_session_uuid(
        db_session: Session, user_uuid: str, game_session_uuid: str
    ) -> Optional[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(
            user_uuid=user_uuid, game_session_uuid=game_session_uuid
        )
        result = db_session.execute(stmt)
        return result.scalars().first()


class AvatarRepository:
    @staticmethod
    def get_avatar_by_uuid(db_session: Session, uuid: str) -> Optional[AvatarDB]:
        stmt = select(AvatarDB).filter_by(uuid=uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def create_avatar(db_session: Session, avatar: AvatarDB) -> AvatarDB:
        db_session.add(avatar)
        db_session.commit()
        db_session.refresh(avatar)
        return avatar


class OneironautRepository:
    @staticmethod
    def get_oneironaut_by_uuid(
        db_session: Session, uuid: str
    ) -> Optional[OneironautDB]:
        stmt = select(OneironautDB).filter_by(uuid=uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def create_oneironaut(
        db_session: Session, oneironaut: OneironautDB
    ) -> OneironautDB:
        db_session.add(oneironaut)
        db_session.commit()
        db_session.refresh(oneironaut)
        return oneironaut


class InventoryRepository:
    @staticmethod
    def get_inventory_by_uuid(db_session: Session, uuid: str) -> Optional[InventoryDB]:
        stmt = select(InventoryDB).filter_by(uuid=uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def create_inventory(db_session: Session, inventory: InventoryDB) -> InventoryDB:
        db_session.add(inventory)
        db_session.commit()
        db_session.refresh(inventory)
        return inventory
