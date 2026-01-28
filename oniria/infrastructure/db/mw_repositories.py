from typing import List, Sequence, Optional, Dict
from sqlalchemy import select, update, UUID
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db import MasterWorkshopDB, GameSessionDB
from oniria.infrastructure.db.mw_sql_models import (
    ObjectiveType,
    ObjectiveDB,
    CommissionType,
    CommissionDB,
    FactionDB,
    NPCTraitType,
    NPCTraitDB,
    NPCNameDB,
    ScenarioType,
    ScenarioDB,
    DungeonAspectType,
    DungeonAspectDB,
    ConflictEntityType,
    ConflictEntityDB,
    RandomEventDB,
    ToneModifierType,
    ToneModifierDB,
    RewardType,
    RewardDB,
    EnemyDB,
    EnemySubTypeDB,
)


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
    def get_game_sessions_by_master_workshop(
        db_session: Session, master_workshop_uuid: str
    ) -> Sequence[GameSessionDB]:
        stmt = select(GameSessionDB).filter_by(
            master_workshop_uuid=master_workshop_uuid
        )
        result = db_session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_game_session_by_uuid(
        db_session: Session, uuid: str
    ) -> Optional[GameSessionDB]:
        stmt = (
            select(GameSessionDB)
            .filter_by(uuid=uuid)
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
    def get_master_workshop_by_uuid_and_owner(
        db_session: Session, master_workshop_uuid: str, owner: str
    ) -> Optional[MasterWorkshopDB]:
        stmt = select(MasterWorkshopDB).filter_by(
            uuid=master_workshop_uuid, owner=owner
        )
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def update_properties(db_session: Session, uuid: UUID, properties: Dict):
        stmt = (
            update(MasterWorkshopDB)
            .where(MasterWorkshopDB.uuid == uuid)
            .values(properties=properties)
            .execution_options(synchronize_session="fetch")
        )
        db_session.execute(stmt)
        db_session.commit()


class ObjectiveRepository:
    @staticmethod
    def get_all_objectives(db_session: Session) -> Sequence[ObjectiveDB]:
        stmt = select(ObjectiveDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class CommissionRepository:
    @staticmethod
    def get_all_commissions(db_session: Session) -> Sequence[CommissionDB]:
        stmt = select(CommissionDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class FactionRepository:
    @staticmethod
    def get_all_factions(db_session: Session) -> Sequence[FactionDB]:
        stmt = select(FactionDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class NPCTraitRepository:
    @staticmethod
    def get_all_npc_traits(db_session: Session) -> Sequence[NPCTraitDB]:
        stmt = select(NPCTraitDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class NPCNameRepository:
    @staticmethod
    def get_all_npc_names(db_session: Session) -> Sequence[NPCNameDB]:
        stmt = select(NPCNameDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class ScenarioRepository:
    @staticmethod
    def get_all_scenarios(db_session: Session) -> Sequence[ScenarioDB]:
        stmt = select(ScenarioDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class DungeonAspectRepository:
    @staticmethod
    def get_all_dungeon_aspects(db_session: Session) -> Sequence[DungeonAspectDB]:
        stmt = select(DungeonAspectDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class ConflictEntityRepository:
    @staticmethod
    def get_all_conflict_entities(db_session: Session) -> Sequence[ConflictEntityDB]:
        stmt = select(ConflictEntityDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class RandomEventRepository:
    @staticmethod
    def get_all_random_events(db_session: Session) -> Sequence[RandomEventDB]:
        stmt = select(RandomEventDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class ToneModifierRepository:
    @staticmethod
    def get_all_tone_modifiers(db_session: Session) -> Sequence[ToneModifierDB]:
        stmt = select(ToneModifierDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class RewardRepository:
    @staticmethod
    def get_all_rewards(db_session: Session) -> Sequence[RewardDB]:
        stmt = select(RewardDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class EnemyRepository:
    @staticmethod
    def get_all_enemies(db_session: Session) -> Sequence[EnemyDB]:
        stmt = select(EnemyDB).options(
            selectinload(EnemyDB.subtypes).joinedload(EnemySubTypeDB.enemy)
        )
        result = db_session.execute(stmt)
        return result.unique().scalars().all()
