from typing import List, Sequence
from sqlalchemy.orm import Session

from oniria.auth.interfaces import PlanDTO
from oniria.auth.application import PlanMapper
from oniria.auth.infrastructure.db.repositories import PlanRepository
from oniria.auth.infrastructure.db.sql_models import Plan


class PlanService:
    @staticmethod
    def get_all_plans(db_session: Session) -> List[PlanDTO]:
        plans_entities: Sequence[Plan] = PlanRepository.get_all_plans(db_session)
        if plans_entities:
            return [
                PlanMapper.to_dto_from_domain(PlanMapper.to_domain_from_entity(plan))
                for plan in plans_entities
            ]
        # TODO: Handle empty list case to send 204 response
        return []
