import uuid
from gettext import translation
from typing import List, Sequence, Optional

import bcrypt
from sqlalchemy.orm import Session

from oniria.application import MasterWorkshopMapper, GameSessionMapper
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
from oniria.domain import (
    MasterWorkshop,
    User,
    NotFoundException,
    ForbiddenException,
    GameSession,
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
    MasterWorkshopRequest,
    GameSessionRequest,
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
from oniria.infrastructure.db.repositories import (
    TranslationRepository,
    MasterWorkshopRepository,
    GameSessionRepository,
)
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
from oniria.infrastructure.db.sql_models import (
    TranslationDB,
    MasterWorkshopDB,
    GameSessionDB,
)


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


class GameSessionService:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def create_game_session(
        user: User,
        db_session: Session,
        master_workshop_uuid: str,
        game_session_request: GameSessionRequest,
    ) -> GameSession:
        master_workshop_db: Sequence[MasterWorkshopDB] = (
            MasterWorkshopRepository.get_master_workshop_by_uuid_and_owner(
                db_session, master_workshop_uuid, user.uuid
            )
        )
        if not master_workshop_db:
            raise NotFoundException(
                f"No master workshop found with UUID: {master_workshop_uuid} or user {user.uuid} is not the owner"
            )
        if not game_session_request.max_players or game_session_request.max_players < 1:
            game_session_request.max_players = 6
        game_session_db: GameSessionDB = GameSessionDB(
            uuid=uuid.uuid4(),
            name=game_session_request.name,
            password=(
                GameSessionService.hash_password(game_session_request.password)
                if game_session_request.password
                else None
            ),  # If not provided, it will be considered as public
            max_players=game_session_request.max_players,
            master_workshop_uuid=master_workshop_uuid,
        )
        game_session_recorded: GameSessionDB = (
            GameSessionRepository.create_game_session(db_session, game_session_db)
        )
        return GameSessionMapper.to_domain_from_entity(game_session_recorded)

    @staticmethod
    def get_game_sessions_by_master_workshop(
        user: User, db_session: Session, master_workshop_uuid: str
    ) -> List[GameSession]:
        master_workshop_db: Sequence[MasterWorkshopDB] = (
            MasterWorkshopRepository.get_master_workshop_by_uuid_and_owner(
                db_session, master_workshop_uuid, user.uuid
            )
        )
        if not master_workshop_db:
            raise NotFoundException(
                f"No master workshop found with UUID: {master_workshop_uuid} or user {user.uuid} is not the owner"
            )
        game_sessions_entities: Sequence[GameSessionDB] = (
            GameSessionRepository.get_game_sessions_by_master_workhop(
                db_session, master_workshop_uuid
            )
        )
        if game_sessions_entities:
            return [
                GameSessionMapper.to_domain_from_entity(game_session)
                for game_session in game_sessions_entities
            ]
        raise NotFoundException("No game sessions found")

    @staticmethod
    def get_game_session_by_uuid(
        db_session: Session, game_session_uuid: str, user: User
    ) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_uuid(
                db_session, game_session_uuid
            )
        )
        if not game_session_entity:
            raise NotFoundException(
                f"No game session found with UUID: {game_session_uuid}"
            )
        if str(game_session_entity.master_workshop.owner) not in str(user.uuid):
            raise ForbiddenException(
                f"User {user.uuid} is not the owner of this game session"
            )
        return GameSessionMapper.to_domain_from_entity(game_session_entity)

    @staticmethod
    def get_game_session_by_name(db_session: Session, name: str) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_name(db_session, name)
        )
        if not game_session_entity:
            raise NotFoundException(f"No game session found with name: {name}")
        return GameSessionMapper.to_domain_from_entity(game_session_entity)

    @staticmethod
    def get_public_games_sessions(db_session: Session) -> List[GameSession]:
        public_game_sessions: Sequence[GameSessionDB] = (
            GameSessionRepository.get_public_games_sessions(db_session)
        )
        if public_game_sessions:
            return [
                GameSessionMapper.to_domain_from_entity(session)
                for session in public_game_sessions
            ]
        raise NotFoundException("No public game sessions found")

    @staticmethod
    def get_private_game_session(
        db_session: Session, game_session_request: GameSessionRequest
    ) -> GameSession:
        game_session_entity: Optional[GameSessionDB] = (
            GameSessionRepository.get_game_session_by_name(
                db_session, game_session_request.name
            )
        )
        if not game_session_entity:
            raise NotFoundException(
                f"No private game session found with name: {game_session_request.name}"
            )
        if not GameSessionService.verify_password(
            game_session_request.password, game_session_entity.password
        ):
            # TODO: Consider limiting the number of attempts to avoid brute force attacks
            raise ForbiddenException("Invalid password for this game session")
        return GameSessionMapper.to_domain_from_entity(game_session_entity)


class MasterWorkshopService:
    @staticmethod
    def create_master_workshop(
        user: User,
        db_session: Session,
        master_workshop_request: MasterWorkshopRequest,
    ) -> MasterWorkshop:
        master_workshop_db = MasterWorkshopDB(
            uuid=uuid.uuid4(),
            owner=user.uuid,
            properties=master_workshop_request.properties,
        )
        master_workshop_recorded = MasterWorkshopRepository.create_master_workshop(
            db_session, master_workshop_db
        )
        return MasterWorkshopMapper.to_domain_from_entity(master_workshop_recorded)
