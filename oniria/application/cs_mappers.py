from typing import List, Dict

from sqlalchemy import Sequence

from oniria.interfaces import (
    ExperienceDTO,
    ImprovementDTO,
    RenownDTO,
    PhilosophyDTO,
    TemperamentDTO,
    DreamPhaseDTO,
    WeaknessDTO,
    SomnaAffinityDTO,
    SkillDTO,
    MartialDTO,
    ManeuverDTO,
    ManeuversByComplexityDTO,
    SpellDTO,
    EssenceDTO,
    MastersDTO,
    RecipeDTO,
    RecipeByTypeDTO,
    ArmorPropertyDTO,
    ArmorDTO,
    ArmorByTypeDTO,
)
from oniria.infrastructure.db import (
    ExperienceDB,
    ImprovementDB,
    RenownDB,
    PhilosophyDB,
    TemperamentDB,
    DreamPhaseDB,
    WeaknessDB,
    SomnaAffinityDB,
    SkillDB,
    MartialDB,
    ManeuverTypeDB,
    ManeuverDB,
    EssenceDB,
    SpellDB,
    RecipeTypeDB,
    RecipeDB,
    ArmorTypeDB,
    ArmorPropertyDB,
    ArmorDB,
)


class ExperienceMapper:
    @staticmethod
    def from_entity_to_dto(
        experience_db: ExperienceDB, translations: dict
    ) -> ExperienceDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == experience_db.key
        )
        return ExperienceDTO(key=experience_db.key, display_key=display_key)


class ImprovementMapper:
    @staticmethod
    def from_entity_to_dto(
        improvement_db: ImprovementDB, translations: dict
    ) -> ImprovementDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == improvement_db.key
        )
        display_description = next(
            key["translation"]
            for key in translations["description"]
            if key["original"] == improvement_db.key
        )
        return ImprovementDTO(
            key=improvement_db.key,
            display_key=display_key,
            display_description=display_description,
            max=improvement_db.max,
            renown_key=improvement_db.renown_key,
        )


class RenownMapper:
    @staticmethod
    def from_entity_to_dto(renown: RenownDB, translations: List[Dict]) -> RenownDTO:
        display_key = next(
            key["translation"]
            for key in translations[0]["key"]
            if key["original"] == renown.key
        )
        return RenownDTO(
            key=renown.key,
            display_key=display_key,
            level=renown.level,
            lucidity_points={"base": renown.lucidity_points},
            max_magic_level=renown.max_magic_level,
            karma_points={"base": renown.karma_points},
            totems={"base": renown.totems_base},
            mantras={"base": renown.mantras_base},
            recipes={"base": renown.recipes_base},
            books={"base": renown.books_base},
            max_improvements=renown.max_improvements,
            max_experiences=renown.max_experiences,
            improvements=[
                ImprovementMapper.from_entity_to_dto(improvement, translations[1])
                for improvement in renown.improvements
            ],
        )


class PhilosophyMapper:
    @staticmethod
    def from_entity_to_dto(
        philosophy: PhilosophyDB, translations: dict
    ) -> PhilosophyDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == philosophy.key
        )
        return PhilosophyDTO(key=philosophy.key, display_key=display_key)


class TemperamentMapper:
    @staticmethod
    def from_entity_to_dto(
        temperament: TemperamentDB, translations: dict
    ) -> TemperamentDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == temperament.key
        )
        return TemperamentDTO(key=temperament.key, display_key=display_key)


class DreamPhaseMapper:
    @staticmethod
    def from_entity_to_dto(
        dream_phase: DreamPhaseDB, translations: dict
    ) -> DreamPhaseDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == dream_phase.key
        )
        display_description = next(
            key["translation"]
            for key in translations["description"]
            if key["original"] == dream_phase.key
        )
        return DreamPhaseDTO(
            key=dream_phase.key,
            display_key=display_key,
            display_description=display_description,
        )


class WeaknessMapper:
    @staticmethod
    def from_entity_to_dto(weakness: WeaknessDB, translations: dict) -> WeaknessDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == weakness.key
        )
        return WeaknessDTO(key=weakness.key, display_key=display_key)


class SomnaAffinityMapper:
    @staticmethod
    def from_entity_to_dto(
        somna_affinity: SomnaAffinityDB, translations: dict
    ) -> SomnaAffinityDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == somna_affinity.key
        )
        return SomnaAffinityDTO(key=somna_affinity.key, display_key=display_key)


class SkillMapper:
    @staticmethod
    def from_entity_to_dto(skill: SkillDB, translations: dict) -> SkillDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == skill.key
        )
        return SkillDTO(key=skill.key, display_key=display_key)


class MartialMapper:
    @staticmethod
    def from_entity_to_dto(martial: MartialDB, translations: dict) -> MartialDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == martial.key
        )
        return MartialDTO(key=martial.key, display_key=display_key)


class ManeuverMapper:
    @staticmethod
    def from_entity_to_dto(maneuver: ManeuverDB, translations: dict) -> ManeuverDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == maneuver.key
        )
        return ManeuverDTO(
            key=maneuver.key,
            display_key=display_key,
            requires_magic=maneuver.requires_magic,
        )


class ManeuversByComplexityMapper:
    @staticmethod
    def from_entities_to_dto(
        maneuvers: Sequence[ManeuverDB], translations: dict
    ) -> ManeuversByComplexityDTO:
        commons = [
            ManeuverMapper.from_entity_to_dto(maneuver, translations)
            for maneuver in maneuvers
            if maneuver.type == ManeuverTypeDB.common
        ]
        advanced = [
            ManeuverMapper.from_entity_to_dto(maneuver, translations)
            for maneuver in maneuvers
            if maneuver.type == ManeuverTypeDB.advanced
        ]
        return ManeuversByComplexityDTO(commons=commons, advanced=advanced)


class SpellMapper:
    @staticmethod
    def from_entity_to_dto(spell: SpellDB, translations: dict) -> SpellDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == spell.key
        )
        display_description = next(
            key["translation"]
            for key in translations["description"]
            if key["original"] == spell.key
        )
        return SpellDTO(
            key=spell.key,
            tier=spell.tier,
            display_key=display_key,
            display_description=display_description,
        )


class EssenceMapper:
    @staticmethod
    def from_entity_to_dto(essence: EssenceDB, translations: List[Dict]) -> EssenceDTO:
        display_key = next(
            key["translation"]
            for key in translations[0]["key"]
            if key["original"] == essence.key
        )
        spells = [
            SpellMapper.from_entity_to_dto(spell, translations[1])
            for spell in essence.spells
        ]
        return EssenceDTO(key=essence.key, display_key=display_key, spells=spells)


class RecipeMapper:
    @staticmethod
    def from_entity_to_dto(recipe: RecipeDB, translations: Dict) -> RecipeDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == recipe.key
        )
        display_description = next(
            key["translation"]
            for key in translations["description"]
            if key["original"] == recipe.key
        )
        return RecipeDTO(
            key=recipe.key,
            display_key=display_key,
            display_description=display_description,
        )


class RecipeByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        recipes: Sequence[RecipeDB], translations: Dict
    ) -> RecipeByTypeDTO:
        brews = [
            RecipeMapper.from_entity_to_dto(recipe, translations)
            for recipe in recipes
            if recipe.type == RecipeTypeDB.brew
        ]
        poisons = [
            RecipeMapper.from_entity_to_dto(recipe, translations)
            for recipe in recipes
            if recipe.type == RecipeTypeDB.poison
        ]
        return RecipeByTypeDTO(brews=brews, poisons=poisons)


class ArmorPropertyMapper:
    @staticmethod
    def from_entity_to_dto(
        armor_property: ArmorPropertyDB, translations: dict
    ) -> ArmorPropertyDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == armor_property.key
        )
        display_description = next(
            key["translation"]
            for key in translations["description"]
            if key["original"] == armor_property.key
        )
        return ArmorPropertyDTO(
            key=armor_property.key,
            display_key=display_key,
            display_description=display_description,
        )


class ArmorMapper:
    @staticmethod
    def from_entity_to_dto(armor: ArmorDB, translations: List[Dict]) -> ArmorDTO:
        display_key = next(
            key["translation"]
            for key in translations[0]["key"]
            if key["original"] == armor.key
        )
        properties = [
            ArmorPropertyMapper.from_entity_to_dto(prop, translations[1])
            for prop in armor.properties
        ]
        return ArmorDTO(
            key=armor.key,
            display_key=display_key,
            rarity=armor.rarity,
            value=armor.value,
            defense=armor.defense,
            properties=properties,
        )


class ArmorByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        armors: Sequence[ArmorDB], translations: List[Dict]
    ) -> ArmorByTypeDTO:
        light = [
            ArmorMapper.from_entity_to_dto(armor, translations)
            for armor in armors
            if armor.type == ArmorTypeDB.light
        ]
        medium = [
            ArmorMapper.from_entity_to_dto(armor, translations)
            for armor in armors
            if armor.type == ArmorTypeDB.medium
        ]
        heavy = [
            ArmorMapper.from_entity_to_dto(armor, translations)
            for armor in armors
            if armor.type == ArmorTypeDB.heavy
        ]
        return ArmorByTypeDTO(light=light, medium=medium, heavy=heavy)
