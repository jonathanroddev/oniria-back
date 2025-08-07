from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions

from oniria.domain import UnauthorizedException, User

security = HTTPBearer(auto_error=False)


def get_current_external_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not credentials:
        raise UnauthorizedException("Authorization header missing")
    token = credentials.credentials
    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded
    except firebase_exceptions.FirebaseError:
        raise UnauthorizedException("Invalid Firebase token")
