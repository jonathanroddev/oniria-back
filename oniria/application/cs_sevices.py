import uuid
from gettext import translation
from typing import List, Sequence, Optional

from google.auth.metrics import token_request_id_token_mds
from sqlalchemy.orm import Session

from oniria.application.mw_sevices import GameSessionService
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
    ItemMapper,
    TotemByTypeMapper,
    MantraMapper,
    BookMapper,
)
from oniria.domain import (
    NotFoundException,
    CharacterSheet,
    GameSession,
    UnauthorizedException,
    ConflictException,
    ForbiddenException,
)
from oniria.interfaces import (
    ExperienceDTO,
    RenownDTO,
    CSBootstrapDTO,
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
    ItemDTO,
    TotemByTypeDTO,
    MantraDTO,
    BookDTO,
    CharacterSheetRequest,
    CharacterSheetUpdatePropertiesRequest,
)
from oniria.application.cs_mappers import (
    ExperienceMapper,
    RenownMapper,
)
from oniria.application.mappers import GameSessionMapper, CharacterSheetMapper
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
    ItemRepository,
    TotemRepository,
    MantraRepository,
    BookRepository,
)
from oniria.infrastructure.db.repositories import (
    TranslationRepository,
    CharacterSheetRepository,
    GameSessionRepository,
    MasterWorkshopRepository,
)
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
    ItemDB,
    TotemDB,
    MantraDB,
    BookDB,
)
from oniria.infrastructure.db.sql_models import (
    TranslationDB,
    CharacterSheetDB,
    GameSessionDB,
    MasterWorkshopDB,
)
from oniria.domain import User


class CSBootstrapService:
    @staticmethod
    def get_bootstrap_data(db_session: Session, lang: str = "es") -> CSBootstrapDTO:
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
        items: Sequence[ItemDB] = ItemRepository.get_all_items(db_session)
        totems: Sequence[TotemDB] = TotemRepository.get_all_totems(db_session)
        mantras: Sequence[MantraDB] = MantraRepository.get_all_mantras(db_session)
        books: Sequence[BookDB] = BookRepository.get_all_books(db_session)
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
        return CSBootstrapDTO(
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
            items=[
                ItemMapper.from_entity_to_dto(item, translations_map["items"])
                for item in items
            ],
            totems=TotemByTypeMapper.from_entities_to_dto(
                totems, translations_map["totems"]
            ),
            mantras=[
                MantraMapper.from_entity_to_dto(mantra, translations_map["mantras"])
                for mantra in mantras
            ],
            books=[
                BookMapper.from_entity_to_dto(book, translations_map["books"])
                for book in books
            ],
        )


class CharacterSheetService:
    @staticmethod
    def create_character_sheet(
        user: User,
        db_session: Session,
        character_sheet_request: CharacterSheetRequest,
    ) -> CharacterSheet:
        game_session: GameSession = GameSessionService.get_game_session_by_name(
            db_session, character_sheet_request.game_session.name
        )
        # TODO: Consider limiting the number of attempts to avoid brute force attacks
        if game_session.password and (
            not character_sheet_request.game_session.password
            or not GameSessionService.verify_password(
                character_sheet_request.game_session.password, game_session.password
            )
        ):
            raise UnauthorizedException(
                "Password is required for this game session or it is invalid"
            )
        character_sheet_exists = CharacterSheetRepository.get_character_sheet_by_user_uuid_and_game_session_uuid(
            db_session, user.uuid, game_session.uuid
        )
        if character_sheet_exists:
            raise ConflictException(
                "Character sheet already exists for this user in this game session"
            )
        characters_sheets_on_this_game_session = (
            CharacterSheetRepository.get_characters_sheets_by_game_session_uuid(
                db_session, game_session.uuid
            )
        )
        if len(characters_sheets_on_this_game_session) >= game_session.max_players:
            raise ConflictException(
                "Maximum number of players reached for this game session"
            )
        character_sheet_db = CharacterSheetDB(
            uuid=uuid.uuid4(),
            user_uuid=user.uuid,
            game_session_uuid=game_session.uuid,
            properties=character_sheet_request.properties,
        )
        character_sheet_recorded = CharacterSheetRepository.create_character_sheet(
            db_session, character_sheet_db
        )
        return CharacterSheetMapper.to_domain_from_entity(character_sheet_recorded)

    @staticmethod
    def update_character_sheet_properties(
        user: User,
        db_session: Session,
        character_sheet_uuid: str,
        character_sheet_request: CharacterSheetUpdatePropertiesRequest,
    ) -> CharacterSheet:
        character_sheet_db: CharacterSheetDB = (
            CharacterSheetRepository.get_character_sheet_by_uuid(
                db_session, character_sheet_uuid
            )
        )
        if not character_sheet_db:
            raise NotFoundException("Character sheet not found")
        game_session: GameSessionDB = GameSessionRepository.get_game_session_by_uuid(
            db_session, str(character_sheet_db.game_session.uuid)
        )
        if (str(user.uuid) not in str(character_sheet_db.user_uuid)) and (
            str(user.uuid) not in str(game_session.owner)
        ):
            raise ForbiddenException(
                "User is not allowed to modify this character sheet"
            )
        character_sheet_db.properties = character_sheet_request.properties
        CharacterSheetRepository.update_properties(
            db_session, character_sheet_db.uuid, character_sheet_request.properties
        )
        return CharacterSheetMapper.to_domain_from_entity(character_sheet_db)

    @staticmethod
    def get_characters_sheets_by_master_workshop_and_game_session(
        db_session: Session,
        master_workshop_uuid: str,
        game_session_uuid: str,
        user: User,
    ) -> List[CharacterSheet]:
        master_workshop: MasterWorkshopDB = (
            MasterWorkshopRepository.get_master_workshop_by_uuid_and_owner(
                db_session, master_workshop_uuid, user.uuid
            )
        )
        if not master_workshop:
            raise NotFoundException(
                f"No master workshop found with UUID: {master_workshop_uuid} or user {user.uuid} is not the owner"
            )
        game_session: GameSession = GameSessionService.get_game_session_by_uuid(
            db_session,
            game_session_uuid,
            user,
        )
        if not game_session:
            raise NotFoundException(
                f"No game session found with UUID: {game_session_uuid} or user {user.uuid} is not the owner"
            )
        character_sheets_entities: Sequence[CharacterSheetDB] = (
            CharacterSheetRepository.get_characters_sheets_by_game_session_uuid(
                db_session, game_session.uuid
            )
        )
        if character_sheets_entities:
            return [
                CharacterSheetMapper.to_domain_from_entity(sheet)
                for sheet in character_sheets_entities
            ]
        raise NotFoundException("No character sheets found for this game session")
