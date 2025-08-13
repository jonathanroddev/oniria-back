from typing import Optional, List, Dict
from pydantic import BaseModel, constr, EmailStr


class ExperienceDTO(BaseModel):
    key: constr(max_length=100)


class ImprovementDTO(BaseModel):
    key: constr(max_length=100)
    max: int
    renown_key: constr(max_length=50)


class RenownDTO(BaseModel):
    key: constr(max_length=50)
    lucidity_points: Dict
    max_magic_level: int
    karma_points: Dict
    totems: Dict
    mantras: Dict
    recipes: Dict
    books: Dict
    max_improvements: int
    max_experiences: int
    improvements: List[ImprovementDTO] = []


class BootstrapDTO(BaseModel):
    renown: RenownDTO
    experiences: List[ExperienceDTO]
