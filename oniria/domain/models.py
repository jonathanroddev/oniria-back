from dataclasses import dataclass
from typing import List


@dataclass
class Plan:
    name: str


@dataclass
class GameSession:
    uuid: str
    owner: str
    name: str
    password: str


@dataclass
class UserStatus:
    name: str


@dataclass
class Avatar:
    uuid: str


@dataclass
class Oneironaut:
    uuid: str


@dataclass
class Inventory:
    uuid: str


@dataclass
class CharacterSheet:
    uuid: str
    user_uuid: str
    avatar: Avatar
    oneironaut: Oneironaut
    inventory: Inventory
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
