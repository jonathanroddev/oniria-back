from pydantic import BaseModel, constr, EmailStr


class SignUp(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8, max_length=100)


class PlanDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=50)


class UserStatusDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=50)


class UserDTO(BaseModel):
    uuid: str
    external_uuid: str
    dreamer_tag: constr(strip_whitespace=True, min_length=1, max_length=50)
    user_status: UserStatusDTO
    plan: PlanDTO
