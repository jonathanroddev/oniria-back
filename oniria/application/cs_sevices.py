from gettext import translation
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
from oniria.infrastructure.db.repositories import TranslationRepository
from oniria.infrastructure.db.cs_sql_models import (
    ExperienceDB,
    RenownDB,
)
from oniria.infrastructure.db.sql_models import TranslationDB


class BootstrapService:
    @staticmethod
    def get_bootstrap_data(db_session: Session, lang: str = "es") -> BootstrapDTO:
        renown_entities: Sequence[RenownDB] = RenownRepository.get_all_renowns(
            db_session
        )
        experiences_entities: Sequence[ExperienceDB] = (
            ExperienceRepository.get_all_experiences(db_session)
        )
        translations: Sequence[TranslationDB] = (
            TranslationRepository.get_all_translations_by_language(
                db_session, lang.lower()
            )
        )
        translations_map = {}
        for entity in translations:
            translations_map.setdefault(entity.table_name, {}).setdefault(
                entity.property, []
            ).append(
                {"original": entity.element_key, "translation": entity.display_text}
            )
        bootstrap: BootstrapDTO = BootstrapDTO(
            renown=[
                RenownMapper.from_entity_to_dto(
                    renown,
                    [translations_map["renown"], translations_map["improvements"]],
                )
                for renown in renown_entities
            ],
            experiences=[
                ExperienceMapper.from_entity_to_dto(
                    experience, translations_map["experiences"]
                )
                for experience in experiences_entities
            ],
        )
        return bootstrap
