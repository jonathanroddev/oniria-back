from fastapi import APIRouter

router = APIRouter()
router.prefix = "/v1/auth"


@router.get("/dummy")
def dummy():
    return {"messag": "Working on something big!"}
