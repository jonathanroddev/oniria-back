from oniria.auth.domain import Plan
from oniria.auth.interfaces import PlanDTO, UserStatusDTO, UserDTO
from oniria.auth.infrastructure.db import PlanDB, UserStatusDB, UserDB


class PlanMapper:
    @staticmethod
    def to_domain_from_entity(plan: PlanDB) -> Plan:
        return Plan(
            name=plan.name,
        )

    @staticmethod
    def to_dto_from_domain(domain: Plan) -> PlanDTO:
        return PlanDTO(
            name=domain.name,
        )


class UserStatusMapper:
    @staticmethod
    def to_dto_from_entity(user_status: UserStatusDB) -> UserStatusDTO:
        return UserStatusDTO(
            name=user_status.name,
        )


class UserMapper:
    @staticmethod
    def to_dto_from_entity(user: UserDB) -> UserDTO:
        return UserDTO(
            uuid=str(user.uuid),
            external_uuid=user.external_uuid,
            dreamer_tag=user.dreamer_tag,
            user_status=UserStatusMapper.to_dto_from_entity(user.user_status_rel),
            plan=PlanMapper.to_dto_from_domain(
                PlanMapper.to_domain_from_entity(user.plan_rel)
            ),
        )
