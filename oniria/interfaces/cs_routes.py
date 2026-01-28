from typing import List

from fastapi import APIRouter, Depends

from oniria.application import CharacterSheetMapper, CharacterSheetService
from oniria.application.cs_sevices import CSBootstrapService
from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
from sqlalchemy.orm import Session
from oniria.interfaces import (
    CSBootstrapDTO,
    CharacterSheetDTO,
    CharacterSheetRequest,
    UpdatePropertiesRequest,
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
    update_properties_request: UpdatePropertiesRequest,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    check_permissions(user, "characters_sheets", "write")
    return CharacterSheetMapper.to_dto_from_domain(
        CharacterSheetService.update_character_sheet_properties(
            user, db_session, character_sheet_uuid, update_properties_request
        )
    )


@router.get(
    "/characters-sheets", response_model=List[CharacterSheetDTO], tags=["campaigns"]
)
def get_character_sheet_by_user(
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[CharacterSheetDTO]:
    check_permissions(user, "characters_sheets", "read")
    character_sheets = CharacterSheetService.get_character_sheet_by_user(
        db_session, user
    )
    return [
        CharacterSheetMapper.to_dto_from_domain(sheet) for sheet in character_sheets
    ]


@router.get(
    "/masters-workshops/{master_workshop_uuid}/games-sessions/{game_session_uuid}/characters-sheets",
    response_model=List[CharacterSheetDTO],
    tags=["campaigns"],
)
def get_characters_sheets_by_master_workshop_and_game_session(
    master_workshop_uuid: str,
    game_session_uuid: str,
    db_session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[CharacterSheetDTO]:
    check_permissions(user, "characters_sheets", "read")
    character_sheets = (
        CharacterSheetService.get_characters_sheets_by_master_workshop_and_game_session(
            db_session, master_workshop_uuid, game_session_uuid, user
        )
    )
    return [
        CharacterSheetMapper.to_dto_from_domain(sheet) for sheet in character_sheets
    ]
