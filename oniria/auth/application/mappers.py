from oniria.auth.domain import PlanDomain
from oniria.auth.interfaces import PlanDTO, UserStatusDTO, UserDTO
from oniria.auth.infrastructure.db import Plan, UserStatus, User


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


class UserStatusMapper:
    @staticmethod
    def to_dto_from_entity(user_status: UserStatus) -> UserStatusDTO:
        return UserStatusDTO(
            name=user_status.name,
        )


class UserMapper:
    @staticmethod
    def to_dto_from_entity(user: User) -> UserDTO:
        return UserDTO(
            uuid=str(user.uuid),
            external_uuid=user.external_uuid,
            dreamer_tag=user.dreamer_tag,
            user_status=UserStatusMapper.to_dto_from_entity(user.user_status_rel),
            plan=PlanMapper.to_dto_from_domain(
                PlanMapper.to_domain_from_entity(user.plan_rel)
            ),
        )
