from fastapi import APIRouter, Depends

from oniria.application.mw_sevices import MWBootstrapService
from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
from sqlalchemy.orm import Session
from oniria.interfaces import (
    MWBootstrapDTO,
)

from oniria.infrastructure.db import get_session


router = APIRouter()
router.prefix = "/v1"


@router.get(
    "/masters-workshops/bootstrap", response_model=MWBootstrapDTO, tags=["initial load"]
)
def get_master_workshop_bootstrap_data(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> MWBootstrapDTO:
    check_permissions(user, "masters_workshops", "read")
    return MWBootstrapService.get_bootstrap_data(db_session)
