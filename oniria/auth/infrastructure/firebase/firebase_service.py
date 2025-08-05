from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from firebase_admin import auth as firebase_auth, exceptions as firebase_exceptions

security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        # TODO: Handle this raise in a common error handler
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = credentials.credentials
    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded
    except firebase_exceptions.FirebaseError:
        # TODO: Handle this raise in a common error handler
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
