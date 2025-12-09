from typing import List, Dict

from sqlalchemy import Sequence

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
)
from oniria.infrastructure.db import (
    ObjectiveType,
    ObjectiveDB,
    CommissionType,
    CommissionDB,
    FactionDB,
    NPCTraitType,
    NPCTraitDB,
    NPCNameDB,
    ScenarioType,
    ScenarioDB,
    DungeonAspectType,
    DungeonAspectDB,
    ConflictEntityType,
    ConflictEntityDB,
    RandomEventDB,
    ToneModifierType,
    ToneModifierDB,
    RewardType,
    RewardDB,
    EnemyDB,
    EnemySubTypeDB,
)


class ObjectiveMapper:
    @staticmethod
    def from_entity_to_dto(obj: ObjectiveDB, translations: dict) -> ObjectiveDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == obj.key
        )
        return ObjectiveDTO(
            key=obj.key,
            dice=obj.dice,
            roll=obj.roll,
            display_key=display_key,
        )


class ObjectiveByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        objectives: Sequence[ObjectiveDB], translations: dict
    ) -> ObjectiveByTypeDTO:
        motive = [
            ObjectiveMapper.from_entity_to_dto(objective, translations)
            for objective in objectives
            if objective.type == ObjectiveType.motive
        ]
        action = [
            ObjectiveMapper.from_entity_to_dto(objective, translations)
            for objective in objectives
            if objective.type == ObjectiveType.action
        ]
        target = [
            ObjectiveMapper.from_entity_to_dto(objective, translations)
            for objective in objectives
            if objective.type == ObjectiveType.target
        ]
        need = [
            ObjectiveMapper.from_entity_to_dto(objective, translations)
            for objective in objectives
            if objective.type == ObjectiveType.need
        ]
        status = [
            ObjectiveMapper.from_entity_to_dto(objective, translations)
            for objective in objectives
            if objective.type == ObjectiveType.status
        ]
        return ObjectiveByTypeDTO(
            motive=motive,
            action=action,
            target=target,
            need=need,
            status=status,
        )


class CommissionMapper:
    @staticmethod
    def from_entity_to_dto(
        commission: CommissionDB, translations: dict
    ) -> CommissionDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == commission.key
        )
        return CommissionDTO(
            key=commission.key,
            dice=commission.dice,
            roll=commission.roll,
            display_key=display_key,
        )


class CommissionByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        commissions: Sequence[CommissionDB], translations: dict
    ) -> CommissionByTypeDTO:
        patron = [
            CommissionMapper.from_entity_to_dto(commission, translations)
            for commission in commissions
            if commission.type == CommissionType.patron
        ]
        condition = [
            CommissionMapper.from_entity_to_dto(commission, translations)
            for commission in commissions
            if commission.type == CommissionType.condition
        ]
        return CommissionByTypeDTO(
            patron=patron,
            condition=condition,
        )


class FactionMapper:
    @staticmethod
    def from_entity_to_dto(
        faction: Sequence[FactionDB], translations: dict
    ) -> FactionDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == faction.type
        )
        display_ideology = next(
            key["translation"]
            for key in translations["ideology"]
            if key["original"] == faction.ideology
        )
        display_resource = next(
            key["translation"]
            for key in translations["resource"]
            if key["original"] == faction.resource
        )
        display_limit = next(
            key["translation"]
            for key in translations["limit"]
            if key["original"] == faction.limit
        )
        return FactionDTO(
            key=faction.type,
            dice=faction.dice,
            roll=faction.roll,
            display_key=display_key,
            ideology=faction.ideology,
            display_ideology=display_ideology,
            resource=faction.resource,
            display_resource=display_resource,
            limit=faction.limit,
            display_limit=display_limit,
        )


class NPCTraitMapper:
    @staticmethod
    def from_entity_to_dto(npc_trait: NPCTraitDB, translations: dict) -> NPCTraitDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == npc_trait.key
        )
        return NPCTraitDTO(
            key=npc_trait.key,
            dice=npc_trait.dice,
            roll=npc_trait.roll,
            display_key=display_key,
        )


class NPCTraitByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        npc_traits: Sequence[NPCTraitDB], translations: dict
    ) -> NPCTraitByTypeDTO:
        appearance = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.appearance
        ]
        skin = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.skin
        ]
        facial = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.facial
        ]
        hair = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.hair
        ]
        attire = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.attire
        ]
        voice = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.voice
        ]
        attitude = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.attitude
        ]
        defect = [
            NPCTraitMapper.from_entity_to_dto(npc_trait, translations)
            for npc_trait in npc_traits
            if npc_trait.type == NPCTraitType.defect
        ]
        return NPCTraitByTypeDTO(
            appearance=appearance,
            skin=skin,
            facial=facial,
            hair=hair,
            attire=attire,
            voice=voice,
            attitude=attitude,
            defect=defect,
        )


class NPCNameMapper:
    @staticmethod
    def from_entity_to_dto(npc_name: NPCNameDB) -> NPCNameDTO:
        return NPCNameDTO(
            name=npc_name.name,
            surname=npc_name.surname,
            dice=npc_name.dice,
            roll=npc_name.roll,
        )


class ScenarioMapper:
    @staticmethod
    def from_entity_to_dto(scenario: ScenarioDB, translations: dict) -> ScenarioDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == scenario.key
        )
        display_possible_threats = next(
            (
                key["translation"]
                for key in translations.get("possible_threats", [])
                if key["original"] == scenario.key
            ),
            None,
        )
        display_hazards = next(
            (
                key["translation"]
                for key in translations.get("hazards", [])
                if key["original"] == scenario.key
            ),
            None,
        )
        return ScenarioDTO(
            key=scenario.key,
            dice=scenario.dice,
            roll=scenario.roll,
            display_key=display_key,
            display_possible_threats=display_possible_threats,
            display_hazards=display_hazards,
        )


class ScenarioByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        scenarios: Sequence[ScenarioDB], translations: dict
    ) -> ScenarioByTypeDTO:
        location = [
            ScenarioMapper.from_entity_to_dto(scenario, translations)
            for scenario in scenarios
            if scenario.type == ScenarioType.location
        ]
        concept = [
            ScenarioMapper.from_entity_to_dto(scenario, translations)
            for scenario in scenarios
            if scenario.type == ScenarioType.concept
        ]
        return ScenarioByTypeDTO(
            location=location,
            concept=concept,
        )


class DungeonAspectMapper:
    @staticmethod
    def from_entity_to_dto(
        dungeon_aspect: DungeonAspectDB, translations: dict
    ) -> DungeonAspectDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == dungeon_aspect.key
        )
        return DungeonAspectDTO(
            key=dungeon_aspect.key,
            dice=dungeon_aspect.dice,
            roll=dungeon_aspect.roll,
            display_key=display_key,
        )


class DungeonAspectByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        dungeon_aspects: Sequence[DungeonAspectDB], translations: dict
    ) -> DungeonAspectByTypeDTO:
        ascendancy = [
            DungeonAspectMapper.from_entity_to_dto(da, translations)
            for da in dungeon_aspects
            if da.type == DungeonAspectType.ascendancy
        ]
        usage = [
            DungeonAspectMapper.from_entity_to_dto(da, translations)
            for da in dungeon_aspects
            if da.type == DungeonAspectType.usage
        ]
        content = [
            DungeonAspectMapper.from_entity_to_dto(da, translations)
            for da in dungeon_aspects
            if da.type == DungeonAspectType.content
        ]
        threat = [
            DungeonAspectMapper.from_entity_to_dto(da, translations)
            for da in dungeon_aspects
            if da.type == DungeonAspectType.threat
        ]
        value = [
            DungeonAspectMapper.from_entity_to_dto(da, translations)
            for da in dungeon_aspects
            if da.type == DungeonAspectType.value
        ]
        context = [
            DungeonAspectMapper.from_entity_to_dto(da, translations)
            for da in dungeon_aspects
            if da.type == DungeonAspectType.context
        ]
        return DungeonAspectByTypeDTO(
            ascendancy=ascendancy,
            usage=usage,
            content=content,
            threat=threat,
            value=value,
            context=context,
        )


class ConflictEntityMapper:
    @staticmethod
    def from_entity_to_dto(
        conflict_entity: ConflictEntityDB, translations: dict
    ) -> ConflictEntityDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == conflict_entity.key
        )
        return ConflictEntityDTO(
            key=conflict_entity.key,
            dice=conflict_entity.dice,
            roll=conflict_entity.roll,
            display_key=display_key,
        )


class ConflictEntityByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        conflict_entities: Sequence[ConflictEntityDB], translations: dict
    ) -> ConflictEntityByTypeDTO:
        entity1 = [
            ConflictEntityMapper.from_entity_to_dto(ce, translations)
            for ce in conflict_entities
            if ce.type == ConflictEntityType.entity1
        ]
        entity2 = [
            ConflictEntityMapper.from_entity_to_dto(ce, translations)
            for ce in conflict_entities
            if ce.type == ConflictEntityType.entity2
        ]
        return ConflictEntityByTypeDTO(
            entity1=entity1,
            entity2=entity2,
        )


class RandomEventMapper:
    @staticmethod
    def from_entity_to_dto(
        random_event: RandomEventDB, translations: dict
    ) -> RandomEventDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == random_event.key
        )
        return RandomEventDTO(
            key=random_event.key,
            dice=random_event.dice,
            roll=random_event.roll,
            display_key=display_key,
        )


class ToneModifierMapper:
    @staticmethod
    def from_entity_to_dto(
        tone_modifier: ToneModifierDB, translations: dict
    ) -> ToneModifierDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == tone_modifier.key
        )
        return ToneModifierDTO(
            key=tone_modifier.key,
            dice=tone_modifier.dice,
            roll=tone_modifier.roll,
            display_key=display_key,
        )


class ToneModifierByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        tone_modifiers: Sequence[ToneModifierDB], translations: dict
    ) -> ToneModifierByTypeDTO:
        fear = [
            ToneModifierMapper.from_entity_to_dto(tm, translations)
            for tm in tone_modifiers
            if tm.type == ToneModifierType.fear
        ]
        hope = [
            ToneModifierMapper.from_entity_to_dto(tm, translations)
            for tm in tone_modifiers
            if tm.type == ToneModifierType.hope
        ]
        return ToneModifierByTypeDTO(
            fear=fear,
            hope=hope,
        )


class RewardMapper:
    @staticmethod
    def from_entity_to_dto(reward: RewardDB, translations: dict) -> RewardDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == reward.key
        )
        return RewardDTO(
            key=reward.key,
            dice=reward.dice,
            roll=reward.roll,
            display_key=display_key,
        )


class RewardByTypeMapper:
    @staticmethod
    def from_entities_to_dto(
        rewards: Sequence[RewardDB], translations: dict
    ) -> RewardByTypeDTO:
        object_type = [
            RewardMapper.from_entity_to_dto(reward, translations)
            for reward in rewards
            if reward.type == RewardType.object_type
        ]
        origin = [
            RewardMapper.from_entity_to_dto(reward, translations)
            for reward in rewards
            if reward.type == RewardType.origin
        ]
        creation = [
            RewardMapper.from_entity_to_dto(reward, translations)
            for reward in rewards
            if reward.type == RewardType.creation
        ]
        effect = [
            RewardMapper.from_entity_to_dto(reward, translations)
            for reward in rewards
            if reward.type == RewardType.effect
        ]
        side_effect = [
            RewardMapper.from_entity_to_dto(reward, translations)
            for reward in rewards
            if reward.type == RewardType.side_effect
        ]
        return RewardByTypeDTO(
            object_type=object_type,
            origin=origin,
            creation=creation,
            effect=effect,
            side_effect=side_effect,
        )


class EnemySubtypeMapper:
    @staticmethod
    def from_entity_to_dto(
        enemy_subtype: EnemySubTypeDB, translations: dict
    ) -> EnemySubtypeDTO:
        display_key = next(
            key["translation"]
            for key in translations["key"]
            if key["original"] == enemy_subtype.key
        )
        return EnemySubtypeDTO(
            key=enemy_subtype.key,
            display_key=display_key,
        )


class EnemyMapper:
    @staticmethod
    def from_entity_to_dto(enemy: EnemyDB, translations: List[dict]) -> EnemyDTO:
        display_key = next(
            key["translation"]
            for key in translations[0]["key"]
            if key["original"] == enemy.key
        )
        subtypes = [
            EnemySubtypeMapper.from_entity_to_dto(subtype, translations[1])
            for subtype in enemy.subtypes
        ]
        return EnemyDTO(
            key=enemy.key,
            display_key=display_key,
            subtypes=subtypes,
            threshold_min=enemy.threshold_min,
            threshold_max=enemy.threshold_max,
            danger_min=enemy.danger_min,
            danger_max=enemy.danger_max,
            endurance_min=enemy.endurance_min,
            endurance_max=enemy.endurance_max,
            stamina_min=enemy.stamina_min,
            stamina_max=enemy.stamina_max,
            weakness_min=enemy.weakness_min,
            weakness_max=enemy.weakness_max,
            strength_min=enemy.strength_min,
            strength_max=enemy.strength_max,
            special_min=enemy.special_min,
            special_max=enemy.special_max,
        )
