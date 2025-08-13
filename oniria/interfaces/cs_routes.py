from fastapi import APIRouter, Depends

from oniria.application.cs_sevices import BootstrapService
from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
from sqlalchemy.orm import Session
from oniria.interfaces import (
    BootstrapDTO,
)

from oniria.infrastructure.db import get_session


router = APIRouter()
router.prefix = "/v1"


@router.get(
    "/character-sheets/bootstrap", response_model=BootstrapDTO, tags=["initial load"]
)
def get_bootstrap_data(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> BootstrapDTO:
    check_permissions(user, "characters_sheets", "read")
    return BootstrapService.get_bootstrap_data(db_session)
