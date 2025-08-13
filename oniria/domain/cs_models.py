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
