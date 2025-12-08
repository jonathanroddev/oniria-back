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
    ideology: str
    resource: str
    limit: str


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
    threshold_min: int
    threshold_max: int
    danger_min: int
    danger_max: int
    endurance_min: int
    endurance_max: int
    stamina_min: int
    stamina_max: int
    weakness_min: int
    weakness_max: int
    strength_min: int
    strength_max: int
    special_min: int
    special_max: int


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
