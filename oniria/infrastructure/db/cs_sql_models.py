import enum
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oniria.infrastructure.db import Base


class RenownDB(Base):
    __tablename__ = "renown"

    key: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    lucidity_points: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_level: Mapped[int] = mapped_column(Integer, nullable=False)
    karma_points: Mapped[int] = mapped_column(Integer, nullable=False)
    totems_base: Mapped[int] = mapped_column(Integer, nullable=False)
    mantras_base: Mapped[int] = mapped_column(Integer, nullable=False)
    recipes_base: Mapped[int] = mapped_column(Integer, nullable=False)
    books_base: Mapped[int] = mapped_column(Integer, nullable=False)
    max_improvements: Mapped[int] = mapped_column(Integer, nullable=False)
    max_experiences: Mapped[int] = mapped_column(Integer, nullable=False)

    improvements: Mapped[List["ImprovementDB"]] = relationship(
        "ImprovementDB", back_populates="renown"
    )


class ExperienceDB(Base):
    __tablename__ = "experiences"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)


class ImprovementDB(Base):
    __tablename__ = "improvements"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    renown_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("renown.key"), nullable=False, primary_key=True
    )
    renown: Mapped["RenownDB"] = relationship("RenownDB", back_populates="improvements")


class PhilosophyDB(Base):
    __tablename__ = "philosophies"
    key: Mapped[str] = mapped_column(String(100), primary_key=True)


class TemperamentDB(Base):
    __tablename__ = "temperaments"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class DreamPhaseDB(Base):
    __tablename__ = "dream_phases"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class WeaknessDB(Base):
    __tablename__ = "weaknesses"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class SomnaAffinityDB(Base):
    __tablename__ = "somna_affinities"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)


class SkillDB(Base):
    __tablename__ = "skills"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class MartialDB(Base):
    __tablename__ = "martials"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)


class ManeuverTypeDB(enum.Enum):
    common = "common"
    advanced = "advanced"


class ManeuverDB(Base):
    __tablename__ = "maneuvers"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ManeuverTypeDB] = mapped_column(Enum(ManeuverTypeDB), nullable=False)
    requires_magic: Mapped[bool] = mapped_column(Boolean, default=False)


class EssenceDB(Base):
    __tablename__ = "essences"

    key: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)

    spells: Mapped[list["SpellDB"]] = relationship(back_populates="essence")


class SpellDB(Base):
    __tablename__ = "spells"

    key: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False)
    essence_key: Mapped[str] = mapped_column(ForeignKey("essences.key"), nullable=False)
    tier: Mapped[int] = mapped_column(Integer, nullable=False)

    essence: Mapped["EssenceDB"] = relationship(back_populates="spells")


class RecipeTypeDB(enum.Enum):
    brew = "brew"
    poison = "poison"


class RecipeDB(Base):
    __tablename__ = "recipes"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[RecipeTypeDB] = mapped_column(Enum(RecipeTypeDB), nullable=False)


class ArmorTypeDB(enum.Enum):
    light = "light"
    medium = "medium"
    heavy = "heavy"


class ArmorPropertyDB(Base):
    __tablename__ = "armors_properties"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    armors_properties_links: Mapped[List["ArmorPropertyLinkDB"]] = relationship(
        "ArmorPropertyLinkDB", back_populates="property"
    )
    armors: Mapped[List["ArmorDB"]] = relationship(
        "ArmorDB",
        secondary="armors_properties_links",
        back_populates="properties",
        viewonly=True,
    )


class ArmorPropertyLinkDB(Base):
    __tablename__ = "armors_properties_links"

    armor_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("armors.key"), primary_key=True
    )
    property_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("armors_properties.key"), primary_key=True
    )

    armor: Mapped["ArmorDB"] = relationship(
        "ArmorDB", back_populates="armors_properties_links"
    )
    property: Mapped["ArmorPropertyDB"] = relationship(
        "ArmorPropertyDB", back_populates="armors_properties_links"
    )


class ArmorDB(Base):
    __tablename__ = "armors"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[ArmorTypeDB] = mapped_column(Enum(ArmorTypeDB), nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    defense: Mapped[int] = mapped_column(Integer, nullable=False)

    armors_properties_links: Mapped[List["ArmorPropertyLinkDB"]] = relationship(
        "ArmorPropertyLinkDB", back_populates="armor"
    )
    properties: Mapped[List["ArmorPropertyDB"]] = relationship(
        "ArmorPropertyDB",
        secondary="armors_properties_links",
        back_populates="armors",
        viewonly=True,
    )


class WeaponCriticalLinkDB(Base):
    __tablename__ = "weapons_criticals_links"

    weapon_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("weapons.key"), primary_key=True
    )
    critical_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("weapons_criticals.key"), primary_key=True
    )

    weapon: Mapped["WeaponDB"] = relationship(
        "WeaponDB", back_populates="weapons_criticals_links"
    )
    critical: Mapped["WeaponCriticalDB"] = relationship(
        "WeaponCriticalDB", back_populates="weapons_criticals_links"
    )


class WeaponTypeDB(enum.Enum):
    melee_1_hand = "melee_1_hand"
    melee_2_hands = "melee_2_hands"
    ranged = "ranged"
    arcane = "arcane"


class WeaponDB(Base):
    __tablename__ = "weapons"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[WeaponTypeDB] = mapped_column(Enum(WeaponTypeDB), nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    range: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    attack: Mapped[int] = mapped_column(Integer, nullable=False)
    defense: Mapped[int] = mapped_column(Integer, nullable=False)

    weapons_criticals_links: Mapped[List[WeaponCriticalLinkDB]] = relationship(
        "WeaponCriticalLinkDB", back_populates="weapon"
    )
    criticals: Mapped[List["WeaponCriticalDB"]] = relationship(
        "WeaponCriticalDB",
        secondary="weapons_criticals_links",
        back_populates="weapons",
        viewonly=True,
    )

    weapons_properties_links: Mapped[List["WeaponPropertyLinkDB"]] = relationship(
        "WeaponPropertyLinkDB", back_populates="weapon"
    )
    properties: Mapped[List["WeaponPropertyDB"]] = relationship(
        "WeaponPropertyDB",
        secondary="weapons_properties_links",
        back_populates="weapons",
        viewonly=True,
    )


class WeaponCriticalDB(Base):
    __tablename__ = "weapons_criticals"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)

    weapons_criticals_links: Mapped[List[WeaponCriticalLinkDB]] = relationship(
        "WeaponCriticalLinkDB", back_populates="critical"
    )
    weapons: Mapped[List[WeaponDB]] = relationship(
        "WeaponDB",
        secondary="weapons_criticals_links",
        back_populates="criticals",
        viewonly=True,
    )


class WeaponPropertyDB(Base):
    __tablename__ = "weapons_properties"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)

    has_modifier: Mapped[bool] = mapped_column(Boolean, default=False)

    weapons_properties_links: Mapped[List["WeaponPropertyLinkDB"]] = relationship(
        "WeaponPropertyLinkDB", back_populates="property"
    )
    weapons: Mapped[List[WeaponDB]] = relationship(
        "WeaponDB",
        secondary="weapons_properties_links",
        back_populates="properties",
        viewonly=True,
    )


class WeaponPropertyLinkDB(Base):
    __tablename__ = "weapons_properties_links"

    weapon_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("weapons.key"), primary_key=True
    )
    property_key: Mapped[str] = mapped_column(
        String(50), ForeignKey("weapons_properties.key"), primary_key=True
    )

    modifier: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    weapon: Mapped["WeaponDB"] = relationship(
        "WeaponDB", back_populates="weapons_properties_links"
    )
    property: Mapped["WeaponPropertyDB"] = relationship(
        "WeaponPropertyDB", back_populates="weapons_properties_links"
    )


class ItemDB(Base):
    __tablename__ = "items"

    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    range: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    property_key: Mapped[str] = mapped_column(String(50))
