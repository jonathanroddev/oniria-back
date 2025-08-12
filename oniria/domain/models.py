from dataclasses import dataclass
from typing import List


@dataclass
class Resource:
    name: str


@dataclass
class Operation:
    name: str


@dataclass
class Permission:
    resource: Resource
    operation: Operation


@dataclass
class Plan:
    name: str
    permissions: List[Permission]


@dataclass
class GameSession:
    uuid: str
    owner: str
    name: str
    password: str
    max_players: int


@dataclass
class UserStatus:
    name: str


@dataclass
class CharacterSheet:
    uuid: str
    user_uuid: str
    game_session: GameSession


@dataclass
class MasterWorkshop:
    uuid: str
    user_uuid: str
    game_session: GameSession


@dataclass
class User:
    uuid: str
    external_uuid: str
    dreamer_tag: str
    user_status: UserStatus
    plan: Plan
    character_sheets: List[CharacterSheet]
    masters_workshops: List[MasterWorkshop]
