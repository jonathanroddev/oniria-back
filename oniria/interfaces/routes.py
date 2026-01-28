from typing import List
from fastapi import APIRouter, Depends

from oniria.domain import User
from oniria.application.utils import get_current_user, check_permissions
from sqlalchemy.orm import Session
from oniria.interfaces import (
    SignUp,
    PlanDTO,
    UserDTO,
)
from oniria.application import (
    UserService,
    PlanService,
    PlanMapper,
    UserMapper,
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
