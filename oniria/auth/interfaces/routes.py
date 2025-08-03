from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from oniria.auth import SignUp, PlanDTO, PlanService, UserService, UserDTO
from oniria.db import get_session, engine, Base


router = APIRouter()
router.prefix = "/v1"


@router.post("/signup", response_model=UserDTO, tags=["auth"])
def signup(sign_up: SignUp, db: Session = Depends(get_session)):
    return UserService.sign_up(sign_up, db)


@router.get("/public/plans", response_model=List[PlanDTO], tags=["public"])
def get_plans(db_session: Session = Depends(get_session)):
    return PlanService.get_all_plans(db_session)
