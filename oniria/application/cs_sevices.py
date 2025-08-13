from typing import List, Sequence, Optional

from sqlalchemy.orm import Session

from oniria.application.cs_mappers import (
    ExperienceMapper,
    RenownMapper,
)
from oniria.domain import NotFoundException
from oniria.interfaces import (
    ExperienceDTO,
    RenownDTO,
    BootstrapDTO,
)
from oniria.application import ExperienceMapper, RenownMapper
from oniria.infrastructure.db.cs_repositories import (
    ExperienceRepository,
    RenownRepository,
)
from oniria.infrastructure.db.cs_sql_models import (
    ExperienceDB,
    RenownDB,
)


class BootstrapService:
    @staticmethod
    def get_bootstrap_data(db_session: Session) -> BootstrapDTO:
        renown_entity: Sequence[RenownDB] = RenownRepository.get_all_renowns(db_session)
        experiences_entities: Sequence[ExperienceDB] = (
            ExperienceRepository.get_all_experiences(db_session)
        )
        return BootstrapDTO(
            renown=[
                RenownMapper.from_entity_to_dto(renown) for renown in renown_entity
            ],
            experiences=[
                ExperienceMapper.from_entity_to_dto(experience)
                for experience in experiences_entities
            ],
        )
