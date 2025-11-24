from oniria.domain import (
    Resource,
    Operation,
    Permission,
    Plan,
    User,
    UserStatus,
    CharacterSheet,
    GameSession,
    MasterWorkshop,
)
from oniria.interfaces import (
    ResourceDTO,
    OperationDTO,
    PermissionDTO,
    PlanDTO,
    UserStatusDTO,
    GameSessionDTO,
    CharacterSheetDTO,
    MasterWorkshopDTO,
    UserDTO,
)
from oniria.infrastructure.db import (
    ResourceDB,
    OperationDB,
    PermissionDB,
    PlanDB,
    UserStatusDB,
    UserDB,
    GameSessionDB,
    CharacterSheetDB,
    MasterWorkshopDB,
)


class ResourceMapper:
    @staticmethod
    def to_domain_from_entity(resource: ResourceDB) -> Resource:
        return Resource(
            name=resource.name,
        )

    @staticmethod
    def to_dto_from_domain(domain: Resource) -> ResourceDTO:
        return ResourceDTO(
            name=domain.name,
        )


class OperationMapper:
    @staticmethod
    def to_domain_from_entity(operation: OperationDB) -> Operation:
        return Operation(
            name=operation.name,
        )

    @staticmethod
    def to_dto_from_domain(domain: Operation) -> OperationDTO:
        return OperationDTO(
            name=domain.name,
        )


class PermissionMapper:
    @staticmethod
    def to_domain_from_entity(permission: PermissionDB) -> Permission:
        return Permission(
            resource=ResourceMapper.to_domain_from_entity(permission.resource_rel),
            operation=OperationMapper.to_domain_from_entity(permission.operation_rel),
        )

    @staticmethod
    def to_dto_from_domain(domain: Permission) -> PermissionDTO:
        return PermissionDTO(
            resource=ResourceMapper.to_dto_from_domain(domain.resource),
            operation=OperationMapper.to_dto_from_domain(domain.operation),
        )


class PlanMapper:
    @staticmethod
    def to_domain_from_entity(plan: PlanDB) -> Plan:
        return Plan(
            name=plan.name,
            permissions=[
                PermissionMapper.to_domain_from_entity(permission)
                for permission in plan.permissions
            ],
        )

    @staticmethod
    def to_dto_from_domain(domain: Plan) -> PlanDTO:
        return PlanDTO(
            name=domain.name,
            permissions=[
                PermissionMapper.to_dto_from_domain(permission)
                for permission in domain.permissions
            ],
        )


class UserStatusMapper:
    @staticmethod
    def to_dto_from_entity(user_status: UserStatusDB) -> UserStatusDTO:
        return UserStatusDTO(
            name=user_status.name,
        )

    @staticmethod
    def to_domain_from_entity(user_status: UserStatusDB) -> UserStatus:
        return UserStatus(
            name=user_status.name,
        )

    @staticmethod
    def to_dto_from_domain(domain: UserStatus) -> UserStatusDTO:
        return UserStatusDTO(
            name=domain.name,
        )


class GameSessionMapper:
    @staticmethod
    def to_dto_from_entity(game_session: GameSessionDB) -> GameSessionDTO:
        return GameSessionDTO(
            uuid=str(game_session.uuid),
            name=game_session.name,
            max_players=game_session.max_players,
            master_workshop_uuid=str(game_session.master_workshop_uuid),
        )

    @staticmethod
    def to_domain_from_entity(game_session: GameSessionDB) -> GameSession:
        return GameSession(
            uuid=str(game_session.uuid),
            name=game_session.name,
            password=game_session.password,
            max_players=game_session.max_players,
            master_workshop_uuid=str(game_session.master_workshop_uuid),
        )

    @staticmethod
    def to_dto_from_domain(game_session: GameSession) -> GameSessionDTO:
        return GameSessionDTO(
            uuid=game_session.uuid,
            name=game_session.name,
            max_players=game_session.max_players,
            master_workshop_uuid=game_session.master_workshop_uuid,
        )

    @staticmethod
    def to_entity_from_dto(game_session_dto: GameSessionDTO) -> GameSessionDB:
        return GameSessionDB(
            name=game_session_dto.name,
            password=game_session_dto.password,
            max_players=game_session_dto.max_players,
        )


class CharacterSheetMapper:
    @staticmethod
    def to_dto_from_entity(character_sheet: CharacterSheetDB) -> CharacterSheetDTO:
        return CharacterSheetDTO(
            uuid=str(character_sheet.uuid),
            user_uuid=str(character_sheet.user_uuid),
            game_session=GameSessionMapper.to_dto_from_entity(
                character_sheet.game_session
            ),
            properties=character_sheet.properties,
        )

    @staticmethod
    def to_domain_from_entity(character_sheet: CharacterSheetDB) -> CharacterSheet:
        return CharacterSheet(
            uuid=str(character_sheet.uuid),
            user_uuid=str(character_sheet.user_uuid),
            game_session=GameSessionMapper.to_domain_from_entity(
                character_sheet.game_session
            ),
            properties=character_sheet.properties,
        )

    @staticmethod
    def to_dto_from_domain(character_sheet: CharacterSheet) -> CharacterSheetDTO:
        return CharacterSheetDTO(
            uuid=character_sheet.uuid,
            user_uuid=character_sheet.user_uuid,
            game_session=GameSessionMapper.to_dto_from_domain(
                character_sheet.game_session
            ),
            properties=character_sheet.properties or None,
        )


class MasterWorkshopMapper:
    @staticmethod
    def to_dto_from_entity(master_workshop: MasterWorkshopDB) -> MasterWorkshopDTO:
        return MasterWorkshopDTO(
            uuid=str(master_workshop.uuid),
            owner=str(master_workshop.user_uuid),
            game_sessions=[
                GameSessionMapper.to_dto_from_entity(game_session)
                for game_session in master_workshop.game_sessions
            ],
        )

    @staticmethod
    def to_domain_from_entity(master_workshop: MasterWorkshopDB) -> MasterWorkshop:
        return MasterWorkshop(
            uuid=str(master_workshop.uuid),
            owner=str(master_workshop.owner),
            game_sessions=[
                GameSessionMapper.to_domain_from_entity(game_session)
                for game_session in master_workshop.game_sessions
            ],
        )

    @staticmethod
    def to_dto_from_domain(domain: MasterWorkshop) -> MasterWorkshopDTO:
        return MasterWorkshopDTO(
            uuid=domain.uuid,
            owner=domain.owner,
            game_sessions=[
                GameSessionMapper.to_dto_from_domain(game_session)
                for game_session in domain.game_sessions
            ],
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
            character_sheets=[
                CharacterSheetMapper.to_dto_from_entity(sheet)
                for sheet in user.character_sheets
            ],
            masters_workshops=[
                MasterWorkshopMapper.to_dto_from_entity(workshop)
                for workshop in user.masters_workshops
            ],
        )

    @staticmethod
    def to_domain_from_entity(user: UserDB) -> User:
        return User(
            uuid=str(user.uuid),
            external_uuid=user.external_uuid,
            dreamer_tag=user.dreamer_tag,
            user_status=UserStatusMapper.to_domain_from_entity(user.user_status_rel),
            plan=PlanMapper.to_domain_from_entity(user.plan_rel),
            character_sheets=[
                CharacterSheetMapper.to_domain_from_entity(sheet)
                for sheet in user.characters_sheets
            ],
            masters_workshops=[
                MasterWorkshopMapper.to_domain_from_entity(workshop)
                for workshop in user.masters_workshops
            ],
        )

    @staticmethod
    def to_dto_from_domain(user: User) -> UserDTO:
        return UserDTO(
            uuid=user.uuid,
            external_uuid=user.external_uuid,
            dreamer_tag=user.dreamer_tag,
            user_status=UserStatusMapper.to_dto_from_domain(user.user_status),
            plan=PlanMapper.to_dto_from_domain(user.plan),
            character_sheets=[
                CharacterSheetMapper.to_dto_from_domain(sheet)
                for sheet in user.character_sheets
            ],
            masters_workshops=[
                MasterWorkshopMapper.to_dto_from_domain(workshop)
                for workshop in user.masters_workshops
            ],
        )
