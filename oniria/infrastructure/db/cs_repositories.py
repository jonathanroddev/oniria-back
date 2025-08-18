from typing import List, Sequence, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db.cs_sql_models import (
    RenownDB,
    ExperienceDB,
    ImprovementDB,
    PhilosophyDB,
    TemperamentDB,
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
