from fastapi.security import HTTPBearer
from fastapi import Depends
from sqlalchemy.orm import Session

from oniria.application import UserService
from oniria.domain import User, ForbiddenException
from oniria.infrastructure.db import get_session
from oniria.infrastructure.firebase.firebase_service import get_current_external_user

security = HTTPBearer(auto_error=False)


def get_current_user(
    user_data_external=Depends(get_current_external_user),
    db_session: Session = Depends(get_session),
) -> User:
    return UserService.get_user_by_external_uuid(user_data_external["uid"], db_session)


def check_permissions(user: User, resource: str, operation: str) -> None:
    authorized: bool = False
    for permission in user.plan.permissions:
        if (
            permission.resource.name == resource
            and permission.operation.name == operation
        ):
            authorized = True
            break
    if not authorized:
        raise ForbiddenException(
            "You do not have permission to perform this operation."
        )
