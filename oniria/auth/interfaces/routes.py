from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from oniria.auth import PlanDTO, PlanService
from oniria.db import get_session, engine, Base

router = APIRouter()
router.prefix = "/v1"


@router.get("/public/plans", response_model=List[PlanDTO], tags=["public"])
def get_plans(db_session: Session = Depends(get_session)):
    return PlanService.get_all_plans(db_session)
