from oniria.auth.domain import PlanDomain
from oniria.auth.interfaces import PlanDTO
from oniria.auth.infrastructure.db import Plan


class PlanMapper:
    @staticmethod
    def to_domain_from_entity(plan: Plan) -> PlanDomain:
        return PlanDomain(
            name=plan.name,
        )

    @staticmethod
    def to_dto_from_domain(domain: PlanDomain) -> PlanDTO:
        return PlanDTO(
            name=domain.name,
        )
