from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions
from sqlalchemy.orm import Session

from oniria.application import UserService
from oniria.domain import UnauthorizedException, User
from oniria.infrastructure.db import get_session

security = HTTPBearer(auto_error=False)


def get_current_user(
    db_session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    if not credentials:
        raise UnauthorizedException("Authorization header missing")
    token = credentials.credentials
    try:
        decoded = firebase_auth.verify_id_token(token)
        return UserService.get_user_by_external_uuid(decoded["uid"], db_session)
    except firebase_exceptions.FirebaseError:
        raise UnauthorizedException("Invalid Firebase token")
