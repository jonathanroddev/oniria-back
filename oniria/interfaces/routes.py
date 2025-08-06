from typing import List, Generator
from fastapi import APIRouter, Depends

from oniria.application.mappers import GameSessionMapper
from oniria.application.sevices import GameSessionService
from oniria.domain import User
from oniria.infrastructure.firebase.firebase_service import get_current_user
from sqlalchemy.orm import Session
from oniria.interfaces import (
    SignUp,
    PlanDTO,
    UserDTO,
    GameSessionDTO,
    GameSessionRequest,
)
from oniria.application import UserService, PlanService, PlanMapper, UserMapper
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
