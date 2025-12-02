import enum
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria.infrastructure.db import Base


class ObjectiveType(enum.Enum):
    motive = "motive"
    action = "action"
    target = "target"
    need = "need"
    status = "status"


class ObjectiveDB(Base):
    __tablename__ = "objectives"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ObjectiveType] = mapped_column(Enum(ObjectiveType), nullable=False)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class CommissionType(enum.Enum):
    patron = "patron"
    condition = "condition"


class CommissionDB(Base):
    __tablename__ = "commissions"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[CommissionType] = mapped_column(Enum(CommissionType), nullable=False)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class FactionDB(Base):
    __tablename__ = "factions"

    roll: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    ideology: Mapped[str] = mapped_column(String(50), nullable=False)
    resource: Mapped[str] = mapped_column(String(50), nullable=False)
    limit: Mapped[str] = mapped_column(String(50), nullable=False)


class NPCTraitType(enum.Enum):
    appearance = "appearance"
    skin = "skin"
    facial = "facial"
    hair = "hair"
    attire = "attire"
    voice = "voice"
    attitude = "attitude"
    defect = "defect"
    profession = "profession"
    problem = "problem"


class NPCTraitDB(Base):
    __tablename__ = "npc_traits"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[NPCTraitType] = mapped_column(Enum(NPCTraitType), nullable=False)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class NPCNameDB(Base):
    __tablename__ = "npc_names"

    roll: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)


class ScenarioType(enum.Enum):
    location = "location"
    concept = "concept"


class ScenarioDB(Base):
    __tablename__ = "scenarios"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ScenarioType] = mapped_column(Enum(ScenarioType), nullable=False)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonAspectType(enum.Enum):
    ascendancy = "ascendancy"
    usage = "usage"
    content = "content"
    threat = "threat"
    value = "value"
    context = "context"


class DungeonAspectDB(Base):
    __tablename__ = "dungeon_aspects"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[DungeonAspectType] = mapped_column(
        Enum(DungeonAspectType), nullable=False
    )
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class ConflictEntityType(enum.Enum):
    entity1 = "entity1"
    entity2 = "entity2"


class ConflictEntityDB(Base):
    __tablename__ = "conflict_entities"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ConflictEntityType] = mapped_column(
        Enum(ConflictEntityType), nullable=False
    )
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class RandomEventDB(Base):
    __tablename__ = "random_events"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class ToneModifierType(enum.Enum):
    fear = "fear"
    hope = "hope"


class ToneModifierDB(Base):
    __tablename__ = "tone_modifiers"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ToneModifierType] = mapped_column(
        Enum(ToneModifierType), nullable=False
    )
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class RewardType(enum.Enum):
    object_type = "object_type"
    origin = "origin"
    creation = "creation"
    effect = "effect"
    side_effect = "side_effect"


class RewardDB(Base):
    __tablename__ = "rewards"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[RewardType] = mapped_column(Enum(RewardType), nullable=False)
    dice: Mapped[str] = mapped_column(String(10), nullable=False)
    roll: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyDB(Base):
    __tablename__ = "enemies"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    threshold_min: Mapped[int] = mapped_column(Integer, nullable=True)
    threshold_max: Mapped[int] = mapped_column(Integer, nullable=True)
    danger_min: Mapped[int] = mapped_column(Integer, nullable=True)
    danger_max: Mapped[int] = mapped_column(Integer, nullable=True)
    endurance_min: Mapped[int] = mapped_column(Integer, nullable=True)
    endurance_max: Mapped[int] = mapped_column(Integer, nullable=True)
    stamina_min: Mapped[int] = mapped_column(Integer, nullable=True)
    stamina_max: Mapped[int] = mapped_column(Integer, nullable=True)
    weakness_min: Mapped[int] = mapped_column(Integer, nullable=True)
    weakness_max: Mapped[int] = mapped_column(Integer, nullable=True)
    strength_min: Mapped[int] = mapped_column(Integer, nullable=True)
    strength_max: Mapped[int] = mapped_column(Integer, nullable=True)
    special_min: Mapped[int] = mapped_column(Integer, nullable=True)
    special_max: Mapped[int] = mapped_column(Integer, nullable=True)
    subtypes: Mapped[List["EnemySubTypeDB"]] = relationship(
        "EnemySubTypeDB", back_populates="enemy"
    )


class EnemySubTypeDB(Base):
    __tablename__ = "enemies_subtypes"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("enemies.key"), nullable=False
    )

    enemy: Mapped["EnemyDB"] = relationship("EnemyDB", back_populates="subtypes")
