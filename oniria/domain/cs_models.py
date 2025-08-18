from dataclasses import dataclass
from typing import List


@dataclass
class Experience:
    key: str


@dataclass
class Improvement:
    key: str
    max: int
    renown_key: str


@dataclass
class Renown:
    key: str
    level: int
    lucidity_points: int
    max_magic_level: int
    karma_points: int
    totems_base: int
    mantras_base: int
    recipes_base: int
    books_base: int
    max_improvements: int
    max_experiences: int
    improvements: List[Improvement]


@dataclass
class Philosophy:
    key: str


@dataclass
class Temperament:
    key: str

@dataclass
class DreamPhase:
    key: str
