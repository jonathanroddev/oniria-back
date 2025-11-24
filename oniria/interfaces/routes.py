from typing import List
from fastapi import APIRouter, Depends

from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
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
    CharacterSheetUpdatePropertiesRequest,
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
    check_permissions(user, "characters_sheets", "write")
    return CharacterSheetMapper.to_dto_from_domain(
        CharacterSheetService.create_character_sheet(
            user, db_session, character_sheet_request
        )
    )


@router.put(
    "/characters-sheets/{character_sheet_uuid}/properties",
    response_model=CharacterSheetDTO,
    tags=["campaigns"],
)
def update_character_sheet_properties(
    character_sheet_uuid: str,
    character_sheet_request: CharacterSheetUpdatePropertiesRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    check_permissions(user, "characters_sheets", "write")
    return CharacterSheetMapper.to_dto_from_domain(
        CharacterSheetService.update_character_sheet_properties(
            user, db_session, character_sheet_uuid, character_sheet_request
        )
    )


@router.get(
    "/characters-sheets/games-sessions/{game_session_uuid}",
    response_model=List[CharacterSheetDTO],
    tags=["campaigns"],
)
def get_characters_sheets_by_game_session_uuid(
    game_session_uuid: str,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[CharacterSheetDTO]:
    check_permissions(user, "characters_sheets", "read")
    character_sheets = CharacterSheetService.get_characters_sheets_by_game_session_uuid(
        db_session, game_session_uuid, user
    )
    return [
        CharacterSheetMapper.to_dto_from_domain(sheet) for sheet in character_sheets
    ]
