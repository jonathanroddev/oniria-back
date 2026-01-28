from dataclasses import dataclass
from typing import List, Dict


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
    name: str
    password: str
    max_players: int
    master_workshop_uuid: str


@dataclass
class UserStatus:
    name: str


@dataclass
class CharacterSheet:
    uuid: str
    user_uuid: str
    game_session: GameSession
    properties: Dict


@dataclass
class MasterWorkshop:
    uuid: str
    owner: str
    game_sessions: List[GameSession]
    properties: Dict


@dataclass
class User:
    uuid: str
    external_uuid: str
    dreamer_tag: str
    user_status: UserStatus
    plan: Plan
    character_sheets: List[CharacterSheet]
    masters_workshops: List[MasterWorkshop]
