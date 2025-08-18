from typing import Optional, List, Dict
from pydantic import BaseModel, constr


class ExperienceDTO(BaseModel):
    key: constr(max_length=100)
    display_key: str


class ImprovementDTO(BaseModel):
    key: constr(max_length=100)
    display_key: str
    display_description: str
    max: int
    renown_key: constr(max_length=50)


class RenownDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    level: int
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


class PhilosophyDTO(BaseModel):
    key: constr(max_length=100)
    display_key: str


class TemperamentDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str


class DreamPhaseDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    display_description: str


class WeaknessDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str


class SomnaAffinityDTO(BaseModel):
    key: constr(max_length=100)
    display_key: str


class BootstrapDTO(BaseModel):
    renown: List[RenownDTO]
    experiences: List[ExperienceDTO]
    philosophies: List[PhilosophyDTO]
    temperaments: List[TemperamentDTO]
    dream_phases: List[DreamPhaseDTO]
    weaknesses: List[WeaknessDTO]
    somna_affinities: List[SomnaAffinityDTO]
