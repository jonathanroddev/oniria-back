from typing import List

from oniria.interfaces import (
    ExperienceDTO,
    ImprovementDTO,
    RenownDTO,
)
from oniria.infrastructure.db import (
    ExperienceDB,
    ImprovementDB,
    RenownDB,
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
