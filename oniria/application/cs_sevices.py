from gettext import translation
from typing import List, Sequence, Optional

from sqlalchemy.orm import Session

from oniria.application.cs_mappers import (
    ExperienceMapper,
    RenownMapper,
    PhilosophyMapper,
    TemperamentMapper,
    DreamPhaseMapper,
    WeaknessMapper,
    SomnaAffinityMapper,
    SkillMapper,
    MartialMapper,
    ManeuversByComplexityMapper,
    EssenceMapper,
    RecipeByTypeMapper,
    ArmorByTypeMapper,
    WeaponByTypeMapper,
)
from oniria.domain import NotFoundException
from oniria.interfaces import (
    ExperienceDTO,
    RenownDTO,
    BootstrapDTO,
    PhilosophyDTO,
    TemperamentDTO,
    DreamPhaseDTO,
    WeaknessDTO,
    SomnaAffinityDTO,
    SkillDTO,
    MartialDTO,
    ManeuversByComplexityDTO,
    EssenceDTO,
    MastersDTO,
    RecipeByTypeDTO,
    ArmorDTO,
    ArmorByTypeDTO,
    WeaponByTypeDTO,
)
from oniria.application import ExperienceMapper, RenownMapper
from oniria.infrastructure.db.cs_repositories import (
    ExperienceRepository,
    RenownRepository,
    PhilosophyRepository,
    TemperamentRepository,
    DreamPhaseRepository,
    WeaknessRepository,
    SomnaAffinityRepository,
    SkillRepository,
    MartialRepository,
    ManeuverRepository,
    EssenceRepository,
    RecipeRepository,
    ArmorRepository,
    WeaponRepository,
)
from oniria.infrastructure.db.repositories import TranslationRepository
from oniria.infrastructure.db.cs_sql_models import (
    ExperienceDB,
    RenownDB,
    PhilosophyDB,
    TemperamentDB,
    DreamPhaseDB,
    WeaknessDB,
    SomnaAffinityDB,
    SkillDB,
    MartialDB,
    ManeuverDB,
    EssenceDB,
    RecipeDB,
    ArmorDB,
    WeaponDB,
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
        philosophies_entities: Sequence[PhilosophyDB] = (
            PhilosophyRepository.get_all_philosophies(db_session)
        )
        temperaments_entities: Sequence[TemperamentDB] = (
            TemperamentRepository.get_all_temperaments(db_session)
        )
        dream_phases_entities: Sequence[DreamPhaseDB] = (
            DreamPhaseRepository.get_all_dream_phases(db_session)
        )
        weaknesses_entities: Sequence[WeaknessDB] = (
            WeaknessRepository.get_all_weaknesses(db_session)
        )
        somna_affinities_entities: Sequence[SomnaAffinityDB] = (
            SomnaAffinityRepository.get_all_somna_affinities(db_session)
        )
        skill_entities: Sequence[SkillDB] = SkillRepository.get_all_skills(db_session)
        martial_entities: Sequence[MartialDB] = MartialRepository.get_all_martials(
            db_session
        )
        maneuvers_entities: Sequence[ManeuverDB] = ManeuverRepository.get_all_maneuvers(
            db_session
        )
        essence_entities: Sequence[EssenceDB] = EssenceRepository.get_all_essences(
            db_session
        )
        recipes: Sequence[RecipeDB] = RecipeRepository.get_all_recipes(db_session)
        armors: Sequence[ArmorDB] = ArmorRepository.get_all_armors(db_session)
        weapons: Sequence[WeaponDB] = WeaponRepository.get_all_weapons(db_session)
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
        masters: MastersDTO = MastersDTO(
            skills=[
                SkillMapper.from_entity_to_dto(skill, translations_map["skills"])
                for skill in skill_entities
            ],
            martial=[
                MartialMapper.from_entity_to_dto(martial, translations_map["martials"])
                for martial in martial_entities
            ],
            maneuvers=ManeuversByComplexityMapper.from_entities_to_dto(
                maneuvers_entities, translations_map["maneuvers"]
            ),
            magics=[
                EssenceMapper.from_entity_to_dto(
                    essence, [translations_map["essences"], translations_map["spells"]]
                )
                for essence in essence_entities
            ],
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
            philosophies=[
                PhilosophyMapper.from_entity_to_dto(
                    philosophy, translations_map["philosophies"]
                )
                for philosophy in philosophies_entities
            ],
            temperaments=[
                TemperamentMapper.from_entity_to_dto(
                    temperament, translations_map["temperaments"]
                )
                for temperament in temperaments_entities
            ],
            dream_phases=[
                DreamPhaseMapper.from_entity_to_dto(
                    dream_phase, translations_map["dream_phases"]
                )
                for dream_phase in dream_phases_entities
            ],
            weaknesses=[
                WeaknessMapper.from_entity_to_dto(
                    weakness, translations_map["weaknesses"]
                )
                for weakness in weaknesses_entities
            ],
            somna_affinities=[
                SomnaAffinityMapper.from_entity_to_dto(
                    somna_affinity, translations_map["somna_affinities"]
                )
                for somna_affinity in somna_affinities_entities
            ],
            masters=masters,
            recipes=RecipeByTypeMapper.from_entities_to_dto(
                recipes, translations_map["recipes"]
            ),
            armors=ArmorByTypeMapper.from_entities_to_dto(
                armors,
                [translations_map["armors"], translations_map["armors_properties"]],
            ),
            weapons=WeaponByTypeMapper.from_entities_to_dto(
                weapons,
                [
                    translations_map["weapons"],
                    translations_map["weapons_criticals"],
                    translations_map["weapons_properties"],
                ],
            ),
        )
        return bootstrap
