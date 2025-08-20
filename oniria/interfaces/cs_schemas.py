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


class SkillDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str


class MartialDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str


class ManeuverDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    requires_magic: bool


class ManeuversByComplexityDTO(BaseModel):
    commons: List[ManeuverDTO]
    advanced: List[ManeuverDTO]


class SpellDTO(BaseModel):
    key: constr(max_length=50)
    tier: int
    display_key: str
    display_description: str


class EssenceDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    spells: List[SpellDTO]


class MastersDTO(BaseModel):
    skills: List[SkillDTO]
    martial: List[MartialDTO]
    maneuvers: ManeuversByComplexityDTO
    magics: List[EssenceDTO]


class RecipeDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    display_description: str


class RecipeByTypeDTO(BaseModel):
    brews: List[RecipeDTO]
    poisons: List[RecipeDTO]


class ArmorPropertyDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    display_description: str


class ArmorDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    rarity: int
    value: int
    defense: int
    properties: List[ArmorPropertyDTO]


class ArmorByTypeDTO(BaseModel):
    light: List[ArmorDTO]
    medium: List[ArmorDTO]
    heavy: List[ArmorDTO]


class BootstrapDTO(BaseModel):
    renown: List[RenownDTO]
    experiences: List[ExperienceDTO]
    philosophies: List[PhilosophyDTO]
    temperaments: List[TemperamentDTO]
    dream_phases: List[DreamPhaseDTO]
    weaknesses: List[WeaknessDTO]
    somna_affinities: List[SomnaAffinityDTO]
    masters: MastersDTO
    recipes: RecipeByTypeDTO
    armors: ArmorByTypeDTO
