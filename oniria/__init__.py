import os
from dotenv import load_dotenv, dotenv_values

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(os.path.abspath(dotenv_path))

from oniria.db import Base, engine, SessionLocal
from oniria.auth.infrastructure.db import (
    PermissionPlanPlayerType,
    PlayerType,
    Plan,
    UserStatus,
    GameSession,
    User,
    Permission,
    Resource,
    Operation,
)
from oniria.campaign.infrastructure.db import (
    Renown,
    CharacterRenown,
    CharactersRenownHistory,
    Experience,
    Improvement,
    ExperienceAcquired,
    ImprovementAcquired,
    CharacterSheet,
    Biography,
    HeroicPath,
    Inventory,
)

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "PermissionPlanPlayerType",
    "PlayerType",
    "Plan",
    "UserStatus",
    "GameSession",
    "User",
    "Permission",
    "Resource",
    "Operation",
    "Renown",
    "CharacterRenown",
    "CharactersRenownHistory",
    "Experience",
    "Improvement",
    "ExperienceAcquired",
    "ImprovementAcquired",
    "CharacterSheet",
    "Biography",
    "HeroicPath",
    "Inventory",
]
