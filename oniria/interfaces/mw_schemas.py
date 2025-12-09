from typing import Optional, List, Dict
from pydantic import BaseModel, constr


class MWCommonDTO(BaseModel):
    dice: str
    roll: int
    display_key: str


class MWCommonWithKeyDTO(MWCommonDTO):
    key: constr(max_length=50)


class ObjectiveDTO(MWCommonWithKeyDTO):
    pass


class ObjectiveByTypeDTO(BaseModel):
    motive: List[ObjectiveDTO]
    action: List[ObjectiveDTO]
    target: List[ObjectiveDTO]
    need: List[ObjectiveDTO]
    status: List[ObjectiveDTO]


class CommissionDTO(MWCommonWithKeyDTO):
    pass


class CommissionByTypeDTO(BaseModel):
    patron: List[CommissionDTO]
    condition: List[CommissionDTO]


class FactionDTO(MWCommonDTO):
    key: str
    ideology: str
    display_ideology: str
    resource: str
    display_resource: str
    limit: str
    display_limit: str


class NPCTraitDTO(MWCommonWithKeyDTO):
    pass


class NPCTraitByTypeDTO(BaseModel):
    appearance: List[NPCTraitDTO]
    skin: List[NPCTraitDTO]
    facial: List[NPCTraitDTO]
    hair: List[NPCTraitDTO]
    attire: List[NPCTraitDTO]
    voice: List[NPCTraitDTO]
    attitude: List[NPCTraitDTO]
    defect: List[NPCTraitDTO]


class NPCNameDTO(BaseModel):
    name: str
    surname: str
    dice: str
    roll: int


class ScenarioDTO(MWCommonWithKeyDTO):
    display_possible_threats: Optional[str] = None
    display_hazards: Optional[str] = None


class ScenarioByTypeDTO(BaseModel):
    location: List[ScenarioDTO]
    concept: List[ScenarioDTO]


class DungeonAspectDTO(MWCommonWithKeyDTO):
    pass


class DungeonAspectByTypeDTO(BaseModel):
    ascendancy: List[DungeonAspectDTO]
    usage: List[DungeonAspectDTO]
    content: List[DungeonAspectDTO]
    threat: List[DungeonAspectDTO]
    value: List[DungeonAspectDTO]
    context: List[DungeonAspectDTO]


class ConflictEntityDTO(MWCommonWithKeyDTO):
    pass


class ConflictEntityByTypeDTO(BaseModel):
    entity1: List[ConflictEntityDTO]
    entity2: List[ConflictEntityDTO]


class RandomEventDTO(MWCommonWithKeyDTO):
    pass


class ToneModifierDTO(MWCommonWithKeyDTO):
    pass


class ToneModifierByTypeDTO(BaseModel):
    fear: List[ToneModifierDTO]
    hope: List[ToneModifierDTO]


class RewardDTO(MWCommonWithKeyDTO):
    pass


class RewardByTypeDTO(BaseModel):
    object_type: List[RewardDTO]
    origin: List[RewardDTO]
    creation: List[RewardDTO]
    effect: List[RewardDTO]
    side_effect: List[RewardDTO]


class EnemySubtypeDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str


class EnemyDTO(BaseModel):
    key: constr(max_length=50)
    display_key: str
    subtypes: List[EnemySubtypeDTO]
    threshold_min: Optional[int]
    threshold_max: Optional[int]
    danger_min: Optional[int]
    danger_max: Optional[int]
    endurance_min: Optional[int]
    endurance_max: Optional[int]
    stamina_min: Optional[int]
    stamina_max: Optional[int]
    weakness_min: Optional[int]
    weakness_max: Optional[int]
    strength_min: Optional[int]
    strength_max: Optional[int]
    special_min: Optional[int]
    special_max: Optional[int]


class MWBootstrapDTO(BaseModel):
    objectives: ObjectiveByTypeDTO
    commissions: CommissionByTypeDTO
    factions: List[FactionDTO]
    npc_traits: NPCTraitByTypeDTO
    npc_names: List[NPCNameDTO]
    scenarios: ScenarioByTypeDTO
    dungeon_aspects: DungeonAspectByTypeDTO
    conflict_entities: ConflictEntityByTypeDTO
    random_events: List[RandomEventDTO]
    tone_modifiers: ToneModifierByTypeDTO
    rewards: RewardByTypeDTO
    enemies: List[EnemyDTO]
