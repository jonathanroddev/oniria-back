from typing import List, Sequence, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

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
