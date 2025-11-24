from typing import Optional, List, Dict
from pydantic import BaseModel, constr, EmailStr


class SignUp(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8, max_length=100)


class ResourceDTO(BaseModel):
    name: str


class OperationDTO(BaseModel):
    name: str


class PermissionDTO(BaseModel):
    resource: ResourceDTO
    operation: OperationDTO


class PlanDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=4, max_length=50)
    permissions: List[PermissionDTO] = []


class UserStatusDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=4, max_length=50)


class GameSessionDTO(BaseModel):
    uuid: str
    name: str
    max_players: int
    master_workshop_uuid: str


class GameSessionRequest(BaseModel):
    name: constr(strip_whitespace=True, min_length=5, max_length=50)
    password: Optional[constr(strip_whitespace=True, min_length=8, max_length=100)] = (
        None
    )
    max_players: Optional[int] = 6


class CharacterSheetDTO(BaseModel):
    uuid: str
    user_uuid: str
    game_session: GameSessionDTO
    properties: Optional[Dict] = None


class CharacterSheetRequest(BaseModel):
    game_session: GameSessionRequest
    properties: Optional[Dict] = None


class CharacterSheetUpdatePropertiesRequest(BaseModel):
    properties: Dict


class MasterWorkshopDTO(BaseModel):
    uuid: str
    owner: str
    game_sessions: List[GameSessionDTO]


class MasterWorkshopRequest(BaseModel):
    pass


class UserDTO(BaseModel):
    uuid: str
    external_uuid: str
    dreamer_tag: constr(strip_whitespace=True, min_length=1, max_length=50)
    user_status: UserStatusDTO
    plan: PlanDTO
    character_sheets: List[CharacterSheetDTO] = []
    masters_workshops: List[MasterWorkshopDTO] = []
