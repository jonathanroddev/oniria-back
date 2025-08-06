import uuid
import bcrypt
from random import Random
from typing import List, Sequence, Optional

from sqlalchemy.orm import Session

from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions

from oniria.application.mappers import GameSessionMapper, MasterWorkshopMapper
from oniria.interfaces import (
    SignUp,
    GameSessionDTO,
    GameSessionRequest,
    MasterWorkshopRequest,
)
from oniria.application import PlanMapper, UserMapper
from oniria.infrastructure.db.repositories import (
    PlanRepository,
    UserRepository,
    UserStatusRepository,
    GameSessionRepository,
    MasterWorkshopRepository,
)
from oniria.infrastructure.db.sql_models import (
    PlanDB,
    UserDB,
    GameSessionDB,
    MasterWorkshopDB,
)
from oniria.domain import (
    User,
    NoContentException,
    ConflictException,
    Plan,
    GameSession,
    UnauthorizedException,
    ForbiddenException,
    MasterWorkshop,
)


class PlanService:
    @staticmethod
    def get_all_plans(db_session: Session) -> List[Plan]:
        plans_entities: Sequence[PlanDB] = PlanRepository.get_all_plans(db_session)
        if plans_entities:
            return [PlanMapper.to_domain_from_entity(plan) for plan in plans_entities]
        raise NoContentException("No plans found")


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
            raise NoContentException(
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
        game_session_request: GameSessionRequest,
    ) -> GameSession:
        game_session_db: GameSessionDB = GameSessionDB(
            uuid=uuid.uuid4(),  # Generate a new UUID for the game session
            owner=user.uuid,  # Set the owner to the current user's UUID
            name=game_session_request.name,
            password=(
                GameSessionService.hash_password(game_session_request.password)
                if game_session_request.password
                else None
            ),  # If not provided, it will be considered as public
            max_players=game_session_request.max_players or 6,
        )
        # TODO: Check public games sessions
        game_session_recorded: GameSessionDB = (
            GameSessionRepository.create_game_session(db_session, game_session_db)
        )
        return GameSessionMapper.to_domain_from_entity(game_session_recorded)

    @staticmethod
    def get_game_sessions_by_owner(
        user: User, db_session: Session
    ) -> List[GameSession]:
        game_sessions_entities: Sequence[GameSessionDB] = (
            GameSessionRepository.get_game_sessions_by_owner(db_session, user.uuid)
        )
        if game_sessions_entities:
            return [
                GameSessionMapper.to_domain_from_entity(game_session)
                for game_session in game_sessions_entities
            ]
        raise NoContentException("No game sessions found for this user")

    @staticmethod
    def get_game_session_by_uuid_and_owner(
        user: User, db_session: Session, uuid
    ) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_uuid_and_owner(
                db_session, uuid, user.uuid
            )
        )
        if not game_session_entity:
            raise NoContentException(f"No game session found with UUID: {uuid}")
        if game_session_entity.owner != user.uuid:
            raise ForbiddenException(
                f"User {user.uuid} is not the owner of this game session"
            )
        return GameSessionMapper.to_domain_from_entity(game_session_entity)


class MasterWorkshopService:
    @staticmethod
    def create_master_workshop(
        user: User,
        db_session: Session,
        master_workshop_request: MasterWorkshopRequest,
    ) -> MasterWorkshop:
        game_session: GameSession = (
            GameSessionService.get_game_session_by_uuid_and_owner(
                user, db_session, master_workshop_request.game_session_uuid
            )
        )
        master_workshop_exists = (
            MasterWorkshopRepository.get_master_workshop_by_game_session_uuid(
                db_session, master_workshop_request.game_session_uuid
            )
        )
        if master_workshop_exists:
            raise ConflictException(
                "Master workshop already exists for this game session"
            )
        master_workshop_db = MasterWorkshopDB(
            uuid=uuid.uuid4(),
            user_uuid=user.uuid,
            game_session=game_session.uuid,
        )
        master_workshop_recorded = MasterWorkshopRepository.create_master_workshop(
            db_session, master_workshop_db
        )
        return MasterWorkshopMapper.to_domain_from_entity(master_workshop_recorded)
