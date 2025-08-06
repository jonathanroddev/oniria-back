from oniria.domain import (
    Plan,
    User,
    UserStatus,
    Avatar,
    Oneironaut,
    Inventory,
    CharacterSheet,
    GameSession,
    MasterWorkshop,
)
from oniria.interfaces import (
    PlanDTO,
    UserStatusDTO,
    AvatarDTO,
    GameSessionDTO,
    OneironautDTO,
    InventoryDTO,
    CharacterSheetDTO,
    MasterWorkshopDTO,
    UserDTO,
)
from oniria.infrastructure.db import (
    PlanDB,
    UserStatusDB,
    UserDB,
    AvatarDB,
    GameSessionDB,
    OneironautDB,
    InventoryDB,
    CharacterSheetDB,
    MasterWorkshopDB,
)


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


class AvatarMapper:
    @staticmethod
    def to_dto_from_entity(avatar: AvatarDB) -> AvatarDTO:
        return AvatarDTO(
            uuid=str(avatar.uuid),
        )

    @staticmethod
    def to_domain_from_entity(avatar: AvatarDB) -> Avatar:
        return Avatar(
            uuid=str(avatar.uuid),
        )

    @staticmethod
    def to_dto_from_domain(domain: Avatar) -> AvatarDTO:
        return AvatarDTO(
            uuid=domain.uuid,
        )


class OneironautMapper:
    @staticmethod
    def to_dto_from_entity(oneironaut: OneironautDB) -> OneironautDTO:
        return OneironautDTO(
            uuid=str(oneironaut.uuid),
        )

    @staticmethod
    def to_domain_from_entity(oneironaut: OneironautDB) -> Oneironaut:
        return Oneironaut(
            uuid=str(oneironaut.uuid),
        )

    @staticmethod
    def to_dto_from_domain(domain: Oneironaut) -> OneironautDTO:
        return OneironautDTO(
            uuid=domain.uuid,
        )


class InventoryMapper:
    @staticmethod
    def to_dto_from_entity(inventory: InventoryDB) -> InventoryDTO:
        return InventoryDTO(
            uuid=str(inventory.uuid),
        )

    @staticmethod
    def to_domain_from_entity(inventory: InventoryDB) -> Inventory:
        return Inventory(
            uuid=str(inventory.uuid),
        )

    @staticmethod
    def to_dto_from_domain(domain: Inventory) -> InventoryDTO:
        return InventoryDTO(
            uuid=domain.uuid,
        )


class GameSessionMapper:
    @staticmethod
    def to_dto_from_entity(game_session: GameSessionDB) -> GameSessionDTO:
        return GameSessionDTO(
            uuid=str(game_session.uuid),
            name=game_session.name,
            owner=str(game_session.owner),
            max_players=game_session.max_players,
        )

    @staticmethod
    def to_domain_from_entity(game_session: GameSessionDB) -> GameSession:
        return GameSession(
            uuid=str(game_session.uuid),
            name=game_session.name,
            password=game_session.password,
            owner=str(game_session.owner),
            max_players=game_session.max_players,
        )

    @staticmethod
    def to_dto_from_domain(game_session: GameSession) -> GameSessionDTO:
        return GameSessionDTO(
            uuid=game_session.uuid,
            name=game_session.name,
            owner=game_session.owner,
            max_players=game_session.max_players,
        )

    @staticmethod
    def to_entity_from_dto(game_session_dto: GameSessionDTO) -> GameSessionDB:
        return GameSessionDB(
            name=game_session_dto.name,
            password=game_session_dto.password,
            owner=game_session_dto.owner,
            max_players=game_session_dto.max_players,
        )


class CharacterSheetMapper:
    @staticmethod
    def to_dto_from_entity(character_sheet: CharacterSheetDB) -> CharacterSheetDTO:
        return CharacterSheetDTO(
            uuid=str(character_sheet.uuid),
            user_uuid=str(character_sheet.user_uuid),
            avatar=AvatarMapper.to_dto_from_entity(character_sheet.avatar),
            oneironaut=OneironautMapper.to_dto_from_entity(character_sheet.oneironaut),
            inventory=InventoryMapper.to_dto_from_entity(character_sheet.inventory),
            game_session=GameSessionMapper.to_dto_from_entity(
                character_sheet.game_session
            ),
        )

    @staticmethod
    def to_domain_from_entity(character_sheet: CharacterSheetDB) -> CharacterSheet:
        return CharacterSheet(
            uuid=str(character_sheet.uuid),
            user_uuid=str(character_sheet.user_uuid),
            avatar=AvatarMapper.to_domain_from_entity(character_sheet.avatar),
            oneironaut=OneironautMapper.to_domain_from_entity(
                character_sheet.oneironaut
            ),
            inventory=InventoryMapper.to_domain_from_entity(character_sheet.inventory),
            game_session=GameSessionMapper.to_domain_from_entity(
                character_sheet.game_session
            ),
        )

    @staticmethod
    def to_dto_from_domain(domain: CharacterSheet) -> CharacterSheetDTO:
        return CharacterSheetDTO(
            uuid=domain.uuid,
            user_uuid=domain.user_uuid,
            avatar=AvatarMapper.to_dto_from_domain(domain.avatar),
            oneironaut=OneironautMapper.to_dto_from_domain(domain.oneironaut),
            inventory=InventoryMapper.to_dto_from_domain(domain.inventory),
            game_session=GameSessionMapper.to_dto_from_domain(domain.game_session),
        )


class MasterWorkshopMapper:
    @staticmethod
    def to_dto_from_entity(master_workshop: MasterWorkshopDB) -> MasterWorkshopDTO:
        return MasterWorkshopDTO(
            uuid=str(master_workshop.uuid),
            user_uuid=str(master_workshop.user_uuid),
            game_session=GameSessionMapper.to_dto_from_entity(
                master_workshop.game_session
            ),
        )

    @staticmethod
    def to_domain_from_entity(master_workshop: MasterWorkshopDB) -> MasterWorkshop:
        return MasterWorkshop(
            uuid=str(master_workshop.uuid),
            user_uuid=str(master_workshop.user_uuid),
            game_session=GameSessionMapper.to_domain_from_entity(
                master_workshop.game_session
            ),
        )

    @staticmethod
    def to_dto_from_domain(domain: MasterWorkshop) -> MasterWorkshopDTO:
        return MasterWorkshopDTO(
            uuid=domain.uuid,
            user_uuid=domain.user_uuid,
            game_session=GameSessionMapper.to_dto_from_domain(domain.game_session),
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
