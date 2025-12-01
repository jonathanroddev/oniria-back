import uuid

import bcrypt
from random import Random
from typing import List, Sequence, Optional

from sqlalchemy.orm import Session

from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions

from oniria.application.mappers import (
    GameSessionMapper,
    MasterWorkshopMapper,
    CharacterSheetMapper,
)
from oniria.interfaces import (
    SignUp,
    GameSessionDTO,
    GameSessionRequest,
    MasterWorkshopRequest,
    CharacterSheetDTO,
    CharacterSheetRequest,
    CharacterSheetUpdatePropertiesRequest,
)
from oniria.application import PlanMapper, UserMapper
from oniria.infrastructure.db.repositories import (
    PlanRepository,
    UserRepository,
    UserStatusRepository,
    GameSessionRepository,
    MasterWorkshopRepository,
    CharacterSheetRepository,
)
from oniria.infrastructure.db.sql_models import (
    PlanDB,
    UserDB,
    GameSessionDB,
    MasterWorkshopDB,
    CharacterSheetDB,
)
from oniria.domain import (
    User,
    NotFoundException,
    ConflictException,
    Plan,
    GameSession,
    UnauthorizedException,
    ForbiddenException,
    MasterWorkshop,
    CharacterSheet,
)


class PlanService:
    @staticmethod
    def get_all_plans(db_session: Session) -> List[Plan]:
        plans_entities: Sequence[PlanDB] = PlanRepository.get_all_plans(db_session)
        if plans_entities:
            return [PlanMapper.to_domain_from_entity(plan) for plan in plans_entities]
        raise NotFoundException("No plans found")


class UserService:
    @staticmethod
    def sign_up(sign_up: SignUp, db_session: Session) -> User:
        try:
            user_record = firebase_auth.create_user(
                email=sign_up.email, password=sign_up.password
            )
        except firebase_exceptions.FirebaseError as e:
            raise ConflictException("Error creating user in external service") from e
        external_uuid = user_record.uid
        existing = UserRepository.get_user_by_external_uuid(db_session, external_uuid)
        if existing:
            raise ConflictException("User already exists with this external UUID")
        # TODO: dreamer_tag should be unique, consider adding a check by creating an endpoint to check if the tag exists
        new_user = UserDB(
            uuid=uuid.uuid4(),
            external_uuid=external_uuid,
            dreamer_tag=f"{str(sign_up.email).split('@')[0]}#{Random().randint(0, 9999)}",
            user_status=UserStatusRepository.get_user_status_by_name(
                db_session, "active"
            ).name,
            plan=PlanRepository.get_plan_by_name(db_session, "free").name,
        )
        UserRepository.create_user(db_session, new_user)
        return UserMapper.to_domain_from_entity(new_user)

    @staticmethod
    def get_user_by_external_uuid(external_uuid: str, db_session: Session) -> User:
        user_entity = UserRepository.get_user_by_external_uuid(
            db_session, external_uuid
        )
        if not user_entity:
            raise NotFoundException(
                f"No user found with external UUID: {external_uuid}"
            )
        return UserMapper.to_domain_from_entity(user_entity)


class GameSessionService:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def create_game_session(
        user: User,
        db_session: Session,
        master_workshop_uuid: str,
        game_session_request: GameSessionRequest,
    ) -> GameSession:
        master_workshop_db: Sequence[MasterWorkshopDB] = (
            MasterWorkshopRepository.get_master_workshop_by_uuid_and_owner(
                db_session, master_workshop_uuid, user.uuid
            )
        )
        if not master_workshop_db:
            raise NotFoundException(
                f"No master workshop found with UUID: {master_workshop_uuid} or user {user.uuid} is not the owner"
            )
        if not game_session_request.max_players or game_session_request.max_players < 1:
            game_session_request.max_players = 6
        game_session_db: GameSessionDB = GameSessionDB(
            uuid=uuid.uuid4(),
            name=game_session_request.name,
            password=(
                GameSessionService.hash_password(game_session_request.password)
                if game_session_request.password
                else None
            ),  # If not provided, it will be considered as public
            max_players=game_session_request.max_players,
            master_workshop_uuid=uuid.UUID(master_workshop_uuid),
        )
        game_session_recorded: GameSessionDB = (
            GameSessionRepository.create_game_session(db_session, game_session_db)
        )
        return GameSessionMapper.to_domain_from_entity(game_session_recorded)

    @staticmethod
    def get_game_sessions_by_master_workshop(
        user: User, db_session: Session, master_workshop_uuid: str
    ) -> List[GameSession]:
        master_workshop_db: Sequence[MasterWorkshopDB] = (
            MasterWorkshopRepository.get_master_workshop_by_uuid_and_owner(
                db_session, master_workshop_uuid, user.uuid
            )
        )
        if not master_workshop_db:
            raise NotFoundException(
                f"No master workshop found with UUID: {master_workshop_uuid} or user {user.uuid} is not the owner"
            )
        game_sessions_entities: Sequence[GameSessionDB] = (
            GameSessionRepository.get_game_sessions_by_master_workhop(
                db_session, master_workshop_uuid
            )
        )
        if game_sessions_entities:
            return [
                GameSessionMapper.to_domain_from_entity(game_session)
                for game_session in game_sessions_entities
            ]
        raise NotFoundException("No game sessions found")

    @staticmethod
    def get_game_session_by_uuid(
        db_session: Session, game_session_uuid: str, user: User
    ) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_uuid(
                db_session, game_session_uuid
            )
        )
        if not game_session_entity:
            raise NotFoundException(
                f"No game session found with UUID: {game_session_uuid}"
            )
        if str(game_session_entity.owner) not in str(user.uuid):
            raise ForbiddenException(
                f"User {user.uuid} is not the owner of this game session"
            )
        return GameSessionMapper.to_domain_from_entity(game_session_entity)

    @staticmethod
    def get_game_session_by_name(db_session: Session, name: str) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_name(db_session, name)
        )
        if not game_session_entity:
            raise NotFoundException(f"No game session found with name: {name}")
        return GameSessionMapper.to_domain_from_entity(game_session_entity)

    @staticmethod
    def get_public_games_sessions(db_session: Session) -> List[GameSession]:
        public_game_sessions: Sequence[GameSessionDB] = (
            GameSessionRepository.get_public_games_sessions(db_session)
        )
        if public_game_sessions:
            return [
                GameSessionMapper.to_domain_from_entity(session)
                for session in public_game_sessions
            ]
        raise NotFoundException("No public game sessions found")

    @staticmethod
    def get_private_game_session(
        db_session: Session, game_session_request: GameSessionRequest
    ) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_name(
                db_session, game_session_request.name
            )
        )
        if not game_session_entity:
            raise NotFoundException(
                f"No private game session found with name: {game_session_request.name}"
            )
        if not GameSessionService.verify_password(
            game_session_request.password, game_session_entity.password
        ):
            # TODO: Consider limiting the number of attempts to avoid brute force attacks
            raise ForbiddenException("Invalid password for this game session")
        return GameSessionMapper.to_domain_from_entity(game_session_entity)


class MasterWorkshopService:
    @staticmethod
    def create_master_workshop(
        user: User,
        db_session: Session,
        master_workshop_request: MasterWorkshopRequest,
    ) -> MasterWorkshop:
        master_workshop_db = MasterWorkshopDB(
            uuid=uuid.uuid4(),
            owner=user.uuid,
        )
        master_workshop_recorded = MasterWorkshopRepository.create_master_workshop(
            db_session, master_workshop_db
        )
        return MasterWorkshopMapper.to_domain_from_entity(master_workshop_recorded)


class CharacterSheetService:
    @staticmethod
    def create_character_sheet(
        user: User,
        db_session: Session,
        character_sheet_request: CharacterSheetRequest,
    ) -> CharacterSheet:
        game_session: GameSession = GameSessionService.get_game_session_by_name(
            db_session, character_sheet_request.game_session.name
        )
        # TODO: Consider limiting the number of attempts to avoid brute force attacks
        if game_session.password and (
            not character_sheet_request.game_session.password
            or not GameSessionService.verify_password(
                character_sheet_request.game_session.password, game_session.password
            )
        ):
            raise UnauthorizedException(
                "Password is required for this game session or it is invalid"
            )
        character_sheet_exists = CharacterSheetRepository.get_character_sheet_by_user_uuid_and_game_session_uuid(
            db_session, user.uuid, game_session.uuid
        )
        if character_sheet_exists:
            raise ConflictException(
                "Character sheet already exists for this user in this game session"
            )
        characters_sheets_on_this_game_session = (
            CharacterSheetRepository.get_characters_sheets_by_game_session_uuid(
                db_session, game_session.uuid
            )
        )
        if len(characters_sheets_on_this_game_session) >= game_session.max_players:
            raise ConflictException(
                "Maximum number of players reached for this game session"
            )
        character_sheet_db = CharacterSheetDB(
            uuid=uuid.uuid4(),
            user_uuid=user.uuid,
            game_session_uuid=game_session.uuid,
            properties=character_sheet_request.properties,
        )
        character_sheet_recorded = CharacterSheetRepository.create_character_sheet(
            db_session, character_sheet_db
        )
        return CharacterSheetMapper.to_domain_from_entity(character_sheet_recorded)

    @staticmethod
    def update_character_sheet_properties(
        user: User,
        db_session: Session,
        character_sheet_uuid: str,
        character_sheet_request: CharacterSheetUpdatePropertiesRequest,
    ) -> CharacterSheet:
        character_sheet_db: CharacterSheetDB = (
            CharacterSheetRepository.get_character_sheet_by_uuid(
                db_session, character_sheet_uuid
            )
        )
        if not character_sheet_db:
            raise NotFoundException("Character sheet not found")
        game_session: GameSessionDB = GameSessionRepository.get_game_session_by_uuid(
            db_session, str(character_sheet_db.game_session.uuid)
        )
        if (str(user.uuid) not in str(character_sheet_db.user_uuid)) and (
            str(user.uuid) not in str(game_session.owner)
        ):
            raise ForbiddenException(
                "User is not allowed to modify this character sheet"
            )
        character_sheet_db.properties = character_sheet_request.properties
        CharacterSheetRepository.update_properties(
            db_session, character_sheet_db.uuid, character_sheet_request.properties
        )
        return CharacterSheetMapper.to_domain_from_entity(character_sheet_db)

    @staticmethod
    def get_characters_sheets_by_master_workshop_and_game_session(
        db_session: Session,
        master_workshop_uuid: str,
        game_session_uuid: str,
        user: User,
    ) -> List[CharacterSheet]:
        master_workshop: MasterWorkshopDB = (
            MasterWorkshopRepository.get_master_workshop_by_uuid_and_owner(
                db_session, master_workshop_uuid, user.uuid
            )
        )
        if not master_workshop:
            raise NotFoundException(
                f"No master workshop found with UUID: {master_workshop_uuid} or user {user.uuid} is not the owner"
            )
        game_session: GameSession = GameSessionService.get_game_session_by_uuid(
            db_session,
            game_session_uuid,
            user,
        )
        if not game_session:
            raise NotFoundException(
                f"No game session found with UUID: {game_session_uuid} or user {user.uuid} is not the owner"
            )
        character_sheets_entities: Sequence[CharacterSheetDB] = (
            CharacterSheetRepository.get_characters_sheets_by_game_session_uuid(
                db_session, game_session.uuid
            )
        )
        if character_sheets_entities:
            return [
                CharacterSheetMapper.to_domain_from_entity(sheet)
                for sheet in character_sheets_entities
            ]
        raise NotFoundException("No character sheets found for this game session")
