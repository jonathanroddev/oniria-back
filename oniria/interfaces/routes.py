from typing import List, Generator
from fastapi import APIRouter, Depends

from oniria.domain import User
from oniria.infrastructure.firebase.firebase_service import get_current_user
from sqlalchemy.orm import Session
from oniria.interfaces import (
    SignUp,
    PlanDTO,
    UserDTO,
    GameSessionDTO,
    GameSessionRequest,
    MasterWorkshopRequest,
    MasterWorkshopDTO,
    CharacterSheetDTO,
    CharacterSheetRequest,
)
from oniria.application import (
    UserService,
    PlanService,
    PlanMapper,
    UserMapper,
    MasterWorkshopMapper,
    GameSessionMapper,
    GameSessionService,
    MasterWorkshopService,
    CharacterSheetMapper,
    CharacterSheetService,
)
from oniria.infrastructure.db import get_session


router = APIRouter()
router.prefix = "/v1"


@router.post("/signup", response_model=UserDTO, tags=["auth"])
def signup(sign_up: SignUp, db: Session = Depends(get_session)):
    return UserMapper.to_dto_from_domain(UserService.sign_up(sign_up, db))


@router.get("/public/plans", response_model=List[PlanDTO], tags=["public"])
def get_plans(db_session: Session = Depends(get_session)):
    return [
        PlanMapper.to_dto_from_domain(plan)
        for plan in PlanService.get_all_plans(db_session)
    ]


@router.get("/users/me", response_model=UserDTO, tags=["users"])
def get_self_user(
    db_session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    return UserMapper.to_dto_from_domain(user)


@router.post("/games-sessions", response_model=GameSessionDTO, tags=["campaigns"])
def create_game_session(
    game_session: GameSessionRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return GameSessionMapper.to_dto_from_domain(
        GameSessionService.create_game_session(user, db_session, game_session)
    )


@router.get("/games-sessions", response_model=List[GameSessionDTO], tags=["campaigns"])
def get_game_sessions_by_owner(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return [
        GameSessionMapper.to_dto_from_domain(game_session)
        for game_session in GameSessionService.get_game_sessions_by_owner(
            user, db_session
        )
    ]


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


@router.post("/characters-sheets", response_model=CharacterSheetDTO, tags=["campaigns"])
def create_character_sheet(
    character_sheet_request: CharacterSheetRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return CharacterSheetMapper.to_dto_from_domain(
        CharacterSheetService.create_character_sheet(
            user, db_session, character_sheet_request
        )
    )
