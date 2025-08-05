from typing import Optional, List
from pydantic import BaseModel, constr, EmailStr


class SignUp(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8, max_length=100)


class PlanDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=4, max_length=50)


class UserStatusDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=4, max_length=50)


class GameSessionDTO(BaseModel):
    uuid: str
    owner: str
    name: constr(strip_whitespace=True, min_length=5, max_length=50)
    password: Optional[constr(strip_whitespace=True, min_length=8, max_length=100)] = (
        None
    )


class AvatarDTO(BaseModel):
    uuid: str


class OneironautDTO(BaseModel):
    uuid: str


class InventoryDTO(BaseModel):
    uuid: str


class CharacterSheetDTO(BaseModel):
    uuid: str
    user_uuid: str
    avatar: AvatarDTO
    oneironaut: OneironautDTO
    inventory: InventoryDTO
    game_session: GameSessionDTO


class MasterWorkshopDTO(BaseModel):
    uuid: str
    user_uuid: str
    game_session: GameSessionDTO


class UserDTO(BaseModel):
    uuid: str
    external_uuid: str
    dreamer_tag: constr(strip_whitespace=True, min_length=1, max_length=50)
    user_status: UserStatusDTO
    plan: PlanDTO
    character_sheets: List[CharacterSheetDTO] = []
    masters_workshops: List[MasterWorkshopDTO] = []
