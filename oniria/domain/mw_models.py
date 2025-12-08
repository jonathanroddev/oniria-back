from dataclasses import dataclass
from typing import List


@dataclass
class MWCommon:
    type: str
    dice: str
    roll: int


@dataclass
class MWCommonWithKey(MWCommon):
    key: str


@dataclass
class Objective(MWCommonWithKey):
    pass


@dataclass
class Commission(MWCommonWithKey):
    pass


@dataclass
class Faction(MWCommon):
    ideology: str
    resource: str
    limit: str


@dataclass
class NPCTrait(MWCommonWithKey):
    pass


@dataclass
class NPCName:
    name: str
    surname: str
    dice: str
    roll: int


@dataclass
class Scenario(MWCommonWithKey):
    pass


@dataclass
class DungeonAspect(MWCommonWithKey):
    pass


@dataclass
class ConflictEntity(MWCommonWithKey):
    pass


@dataclass
class RandomEvent:
    key: str
    dice: str
    roll: int


@dataclass
class ToneModifier(MWCommonWithKey):
    pass


@dataclass
class Reward(MWCommonWithKey):
    pass


@dataclass
class EnemySubtype:
    key: str


@dataclass
class Enemy:
    key: str
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
    subtypes: List[EnemySubtype]
