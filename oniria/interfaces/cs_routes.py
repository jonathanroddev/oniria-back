from fastapi import APIRouter, Depends

from oniria.application.cs_sevices import CSBootstrapService
from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
from sqlalchemy.orm import Session
from oniria.interfaces import (
    CSBootstrapDTO,
)

from oniria.infrastructure.db import get_session


router = APIRouter()
router.prefix = "/v1"


@router.get(
    "/character-sheets/bootstrap", response_model=CSBootstrapDTO, tags=["initial load"]
)
def get_bootstrap_data(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> CSBootstrapDTO:
    check_permissions(user, "characters_sheets", "read")
    return CSBootstrapService.get_bootstrap_data(db_session)
