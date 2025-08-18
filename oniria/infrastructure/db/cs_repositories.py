from typing import List, Sequence, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db.cs_sql_models import (
    RenownDB,
    ExperienceDB,
    ImprovementDB,
    PhilosophyDB,
    TemperamentDB,
    DreamPhaseDB,
    WeaknessDB,
    SomnaAffinityDB,
)


class RenownRepository:
    @staticmethod
    def get_all_renowns(db_session: Session) -> Sequence[RenownDB]:
        stmt = select(RenownDB)
        result = db_session.execute(
            stmt.order_by(RenownDB.level).options(joinedload(RenownDB.improvements))
        )
        return result.unique().scalars().all()


class ExperienceRepository:
    @staticmethod
    def get_all_experiences(db_session: Session) -> Sequence[ExperienceDB]:
        stmt = select(ExperienceDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class PhilosophyRepository:
    @staticmethod
    def get_all_philosophies(db_session: Session) -> Sequence[PhilosophyDB]:
        stmt = select(PhilosophyDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class TemperamentRepository:
    @staticmethod
    def get_all_temperaments(db_session: Session) -> Sequence[TemperamentDB]:
        stmt = select(TemperamentDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class DreamPhaseRepository:
    @staticmethod
    def get_all_dream_phases(db_session: Session) -> Sequence[DreamPhaseDB]:
        stmt = select(DreamPhaseDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class WeaknessRepository:
    @staticmethod
    def get_all_weaknesses(db_session: Session) -> Sequence[WeaknessDB]:
        stmt = select(WeaknessDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class SomnaAffinityRepository:
    @staticmethod
    def get_all_somna_affinities(db_session: Session) -> Sequence[SomnaAffinityDB]:
        stmt = select(SomnaAffinityDB)
        result = db_session.execute(stmt)
        return result.scalars().all()
