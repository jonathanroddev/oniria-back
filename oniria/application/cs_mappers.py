from typing import List

from oniria.interfaces import (
    ExperienceDTO,
    ImprovementDTO,
    RenownDTO,
    PhilosophyDTO,
    TemperamentDTO,
    DreamPhaseDTO,
    WeaknessDTO,
    SomnaAffinityDTO,
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
    def from_entity_to_dto(renown: RenownDB, translations: List[dict]) -> RenownDTO:
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
