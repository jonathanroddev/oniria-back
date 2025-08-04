import uuid
from random import Random
from typing import List, Sequence, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions
from oniria.auth.interfaces import SignUp, PlanDTO, UserDTO
from oniria.auth.application import PlanMapper, UserMapper
from oniria.auth.infrastructure.db.repositories import (
    PlanRepository,
    UserRepository,
    UserStatusRepository,
)
from oniria.auth.infrastructure.db.sql_models import Plan, User


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


class UserService:
    @staticmethod
    def sign_up(sign_up: SignUp, db_session: Session) -> UserDTO:
        try:
            user_record = firebase_auth.create_user(
                email=sign_up.email, password=sign_up.password
            )
        except firebase_exceptions.FirebaseError as e:
            # TODO: Handle this raise in a common error handler
            raise HTTPException(status_code=409, detail=str(e))
        external_uuid = user_record.uid
        existing = UserRepository.get_user_by_external_uuid(db_session, external_uuid)
        if existing:
            # TODO: Handle user already exists case and send 409 response
            pass
        # TODO: dreamer_tag should be unique, consider adding a check by creating an endpoint to check if the tag exists
        new_user = User(
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
    def get_user_by_external_uuid(external_uuid: str, db_session: Session) -> UserDTO:
        user_entity = UserRepository.get_user_by_external_uuid(
            db_session, external_uuid
        )
        if not user_entity:
            # TODO: Handle this raise in a common error handler
            raise HTTPException(status_code=204, detail="User not found")
        return UserMapper.to_dto_from_entity(user_entity)

    @staticmethod
    def get_self_user(
        user_data: firebase_auth.UserRecord, db_session: Session
    ) -> Optional[UserDTO]:
        return UserService.get_user_by_external_uuid(user_data["uid"], db_session)
