from oniria.domain import (
    Experience,
    Improvement,
    Renown,
)
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
    def from_main_to_dto(experience: Experience) -> ExperienceDTO:
        return ExperienceDTO(key=experience.key)


class ImprovementMapper:
    @staticmethod
    def from_main_to_dto(improvement: Improvement) -> ImprovementDTO:
        return ImprovementDTO(
            key=improvement.key, max=improvement.max, renown_key=improvement.renown_key
        )


class RenownMapper:
    @staticmethod
    def from_main_to_dto(renown: Renown) -> RenownDTO:
        return RenownDTO(
            key=renown.key,
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
                ImprovementMapper.from_main_to_dto(improvement)
                for improvement in renown.improvements
            ],
        )
