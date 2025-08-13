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
    def from_entity_to_dto(experience_db: ExperienceDB) -> ExperienceDTO:
        return ExperienceDTO(key=experience_db.key)


class ImprovementMapper:
    @staticmethod
    def from_entity_to_dto(improvement_db: ImprovementDB) -> ImprovementDTO:
        return ImprovementDTO(
            key=improvement_db.key,
            max=improvement_db.max,
            renown_key=improvement_db.renown_key,
        )


class RenownMapper:
    @staticmethod
    def from_entity_to_dto(renown: RenownDB) -> RenownDTO:
        return RenownDTO(
            key=renown.key,
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
                ImprovementMapper.from_entity_to_dto(improvement)
                for improvement in renown.improvements
            ],
        )
