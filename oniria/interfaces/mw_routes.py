from typing import List
from fastapi import APIRouter, Depends

from oniria.application import (
    MasterWorkshopMapper,
    MasterWorkshopService,
    GameSessionMapper,
    GameSessionService,
)
from oniria.application.mw_sevices import MWBootstrapService
from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
from sqlalchemy.orm import Session
from oniria.interfaces import (
    MWBootstrapDTO,
    MasterWorkshopDTO,
    MasterWorkshopRequest,
    GameSessionDTO,
    GameSessionRequest,
    UpdatePropertiesRequest,
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


@router.post("/masters-workshops", response_model=MasterWorkshopDTO, tags=["campaigns"])
def create_master_workshop(
    master_workshop_request: MasterWorkshopRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return MasterWorkshopMapper.to_dto_from_domain(
        MasterWorkshopService.create_master_workshop(
            user, db_session, master_workshop_request
        )
    )


@router.put(
    "/masters-workshops/{master_workshop_uuid}/properties",
    response_model=MasterWorkshopDTO,
    tags=["campaigns"],
)
def update_master_workshop_properties(
    master_workshop_uuid: str,
    update_properties_request: UpdatePropertiesRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    check_permissions(user, "masters_workshops", "write")
    return MasterWorkshopMapper.to_dto_from_domain(
        MasterWorkshopService.update_master_workshop_properties(
            user, db_session, master_workshop_uuid, update_properties_request
        )
    )


@router.get(
    "/masters-workshops",
    response_model=List[MasterWorkshopDTO],
    tags=["campaigns"],
)
def get_masters_workshops_by_user(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[MasterWorkshopDTO]:
    check_permissions(user, "masters_workshops", "read")
    masters_workshops = MasterWorkshopService.get_masters_workshops_by_user(
        db_session, user
    )
    return [MasterWorkshopMapper.to_dto_from_domain(mw) for mw in masters_workshops]


@router.get(
    "/masters-workshops/{master_workshop_uuid}/games-sessions",
    response_model=List[GameSessionDTO],
    tags=["campaigns"],
)
def get_game_sessions_by_master_workshop(
    master_workshop_uuid: str,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return [
        GameSessionMapper.to_dto_from_domain(game_session)
        for game_session in GameSessionService.get_game_sessions_by_master_workshop(
            user, db_session, master_workshop_uuid
        )
    ]


@router.post(
    "/masters-workshops/{master_workshop_uuid}/games-sessions",
    response_model=GameSessionDTO,
    tags=["campaigns"],
)
def create_game_session(
    master_workshop_uuid: str,
    game_session: GameSessionRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return GameSessionMapper.to_dto_from_domain(
        GameSessionService.create_game_session(
            user, db_session, master_workshop_uuid, game_session
        )
    )


@router.put(
    "/masters-workshops/{master_workshop_uuid}/games-sessions/properties",
    response_model=List[GameSessionDTO],
    tags=["campaigns"],
)
def update_game_session_properties(
    master_workshop_uuid: str,
    update_properties_request: UpdatePropertiesRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    check_permissions(user, "masters_workshops", "write")
    return GameSessionMapper.to_dto_from_domain(
        GameSessionService.update_game_session_properties(
            user, db_session, master_workshop_uuid, update_properties_request
        )
    )


@router.get(
    "/games-sessions/public", response_model=List[GameSessionDTO], tags=["campaigns"]
)
def get_public_game_sessions(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[GameSessionDTO]:
    public_game_sessions = GameSessionService.get_public_games_sessions(db_session)
    return [
        GameSessionMapper.to_dto_from_domain(session)
        for session in public_game_sessions
    ]
