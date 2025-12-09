from gettext import translation
from typing import List, Sequence, Optional

from sqlalchemy.orm import Session

from oniria.application.mw_mappers import (
    ObjectiveByTypeMapper,
    CommissionByTypeMapper,
    FactionMapper,
    NPCTraitByTypeMapper,
    NPCNameMapper,
    ScenarioByTypeMapper,
    DungeonAspectByTypeMapper,
    ConflictEntityByTypeMapper,
    RandomEventMapper,
    ToneModifierByTypeMapper,
    RewardByTypeMapper,
    EnemyMapper,
)
from oniria.interfaces import (
    ObjectiveDTO,
    ObjectiveByTypeDTO,
    CommissionDTO,
    CommissionByTypeDTO,
    FactionDTO,
    NPCTraitDTO,
    NPCTraitByTypeDTO,
    NPCNameDTO,
    ScenarioDTO,
    ScenarioByTypeDTO,
    DungeonAspectDTO,
    DungeonAspectByTypeDTO,
    ConflictEntityDTO,
    ConflictEntityByTypeDTO,
    RandomEventDTO,
    ToneModifierDTO,
    ToneModifierByTypeDTO,
    RewardDTO,
    RewardByTypeDTO,
    EnemySubtypeDTO,
    EnemyDTO,
    MWBootstrapDTO,
)
from oniria.infrastructure.db.mw_repositories import (
    ObjectiveRepository,
    CommissionRepository,
    FactionRepository,
    NPCTraitRepository,
    NPCNameRepository,
    ScenarioRepository,
    DungeonAspectRepository,
    ConflictEntityRepository,
    RandomEventRepository,
    ToneModifierRepository,
    RewardRepository,
    EnemyRepository,
)
from oniria.infrastructure.db.repositories import TranslationRepository
from oniria.infrastructure.db.mw_sql_models import (
    ObjectiveDB,
    CommissionDB,
    FactionDB,
    NPCTraitDB,
    NPCNameDB,
    ScenarioDB,
    DungeonAspectDB,
    ConflictEntityDB,
    RandomEventDB,
    ToneModifierDB,
    RewardDB,
    EnemyDB,
)
from oniria.infrastructure.db.sql_models import TranslationDB


class MWBootstrapService:
    @staticmethod
    def get_bootstrap_data(db_session: Session, lang: str = "es") -> MWBootstrapDTO:
        objectives_entities: Sequence[ObjectiveDB] = (
            ObjectiveRepository.get_all_objectives(db_session)
        )
        commissions_entities: Sequence[CommissionDB] = (
            CommissionRepository.get_all_commissions(db_session)
        )
        factions_entities: Sequence[FactionDB] = FactionRepository.get_all_factions(
            db_session
        )
        npc_traits_entities: Sequence[NPCTraitDB] = (
            NPCTraitRepository.get_all_npc_traits(db_session)
        )
        npc_names_entities: Sequence[NPCNameDB] = NPCNameRepository.get_all_npc_names(
            db_session
        )
        scenarios_entities: Sequence[ScenarioDB] = ScenarioRepository.get_all_scenarios(
            db_session
        )
        dungeon_aspects_entities: Sequence[DungeonAspectDB] = (
            DungeonAspectRepository.get_all_dungeon_aspects(db_session)
        )
        conflict_entities: Sequence[ConflictEntityDB] = (
            ConflictEntityRepository.get_all_conflict_entities(db_session)
        )
        random_events_entities: Sequence[RandomEventDB] = (
            RandomEventRepository.get_all_random_events(db_session)
        )
        tone_modifiers_entities: Sequence[ToneModifierDB] = (
            ToneModifierRepository.get_all_tone_modifiers(db_session)
        )
        rewards_entities: Sequence[RewardDB] = RewardRepository.get_all_rewards(
            db_session
        )
        enemies_entities: Sequence[EnemyDB] = EnemyRepository.get_all_enemies(
            db_session
        )
        # TODO: Isolate translations fetching to a separate service
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
        return MWBootstrapDTO(
            objectives=ObjectiveByTypeMapper.from_entities_to_dto(
                objectives_entities, translations_map["objectives"]
            ),
            commissions=CommissionByTypeMapper.from_entities_to_dto(
                commissions_entities, translations_map["commissions"]
            ),
            factions=[
                FactionMapper.from_entity_to_dto(faction, translations_map["factions"])
                for faction in factions_entities
            ],
            npc_traits=NPCTraitByTypeMapper.from_entities_to_dto(
                npc_traits_entities, translations_map["npc_traits"]
            ),
            npc_names=[
                NPCNameMapper.from_entity_to_dto(npc_name)
                for npc_name in npc_names_entities
            ],
            scenarios=ScenarioByTypeMapper.from_entities_to_dto(
                scenarios_entities, translations_map["scenarios"]
            ),
            dungeon_aspects=DungeonAspectByTypeMapper.from_entities_to_dto(
                dungeon_aspects_entities, translations_map["dungeon_aspects"]
            ),
            conflict_entities=ConflictEntityByTypeMapper.from_entities_to_dto(
                conflict_entities, translations_map["conflict_entities"]
            ),
            random_events=[
                RandomEventMapper.from_entity_to_dto(
                    random_event, translations_map["random_events"]
                )
                for random_event in random_events_entities
            ],
            tone_modifiers=ToneModifierByTypeMapper.from_entities_to_dto(
                tone_modifiers_entities, translations_map["tone_modifiers"]
            ),
            rewards=RewardByTypeMapper.from_entities_to_dto(
                rewards_entities, translations_map["rewards"]
            ),
            enemies=[
                EnemyMapper.from_entity_to_dto(
                    enemy,
                    [translations_map["enemies"], translations_map["enemies_subtypes"]],
                )
                for enemy in enemies_entities
            ],
        )
