import uuid
from random import Random
from typing import List, Sequence, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions
from oniria.interfaces import SignUp, PlanDTO, UserDTO
from oniria.application import PlanMapper, UserMapper
from oniria.infrastructure.db.repositories import (
    PlanRepository,
    UserRepository,
    UserStatusRepository,
)
from oniria.infrastructure.db.sql_models import PlanDB, UserDB
from oniria.domain import User, NoContentException, ConflictException


class PlanService:
    @staticmethod
    def get_all_plans(db_session: Session) -> List[PlanDTO]:
        plans_entities: Sequence[PlanDB] = PlanRepository.get_all_plans(db_session)
        if plans_entities:
            return [
                PlanMapper.to_dto_from_domain(PlanMapper.to_domain_from_entity(plan))
                for plan in plans_entities
            ]
        raise NoContentException("No plans found")


class UserService:
    @staticmethod
    def sign_up(sign_up: SignUp, db_session: Session) -> UserDTO:
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
        return UserMapper.to_dto_from_entity(new_user)

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

    @staticmethod
    def get_self_user(
        user_data: firebase_auth.UserRecord, db_session: Session
    ) -> UserDTO:
        return UserMapper.to_dto_from_domain(
            UserService.get_user_by_external_uuid(user_data["uid"], db_session)
        )
