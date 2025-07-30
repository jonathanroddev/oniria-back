from typing import List, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from oniria.auth.infrastructure.db import Plan
from oniria.auth.infrastructure.db.sql_models import Plan


class PlanRepository:
    @staticmethod
    def get_all_plans(db_session: Session) -> Sequence[Plan]:
        stmt = select(Plan)
        result = db_session.execute(stmt)
        return result.scalars().all()
