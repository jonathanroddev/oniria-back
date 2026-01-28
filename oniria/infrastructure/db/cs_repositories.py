from typing import List, Sequence, Optional, Dict
from sqlalchemy import select, UUID, update
from sqlalchemy.orm import Session, selectinload, joinedload

from oniria.infrastructure.db import CharacterSheetDB
from oniria.infrastructure.db.cs_sql_models import (
    RenownDB,
    ExperienceDB,
    ImprovementDB,
    PhilosophyDB,
    TemperamentDB,
    DreamPhaseDB,
    WeaknessDB,
    SomnaAffinityDB,
    SkillDB,
    MartialDB,
    ManeuverTypeDB,
    ManeuverDB,
    EssenceDB,
    SpellDB,
    RecipeTypeDB,
    RecipeDB,
    ArmorTypeDB,
    ArmorPropertyLinkDB,
    ArmorPropertyDB,
    ArmorDB,
    WeaponDB,
    WeaponPropertyLinkDB,
    WeaponCriticalLinkDB,
    ItemDB,
    TotemTypeDB,
    TotemDB,
    MantraDB,
    BookDB,
)


class CharacterSheetRepository:
    @staticmethod
    def create_character_sheet(
        db_session: Session, character_sheet: CharacterSheetDB
    ) -> CharacterSheetDB:
        db_session.add(character_sheet)
        db_session.commit()
        db_session.refresh(character_sheet)
        return character_sheet

    @staticmethod
    def get_character_sheet_by_uuid(
        db_session: Session, character_sheet_uuid: str
    ) -> Optional[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(uuid=character_sheet_uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_character_sheet_by_user_uuid(
        db_session: Session, user_uuid: str
    ) -> Optional[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(user_uuid=user_uuid)
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_characters_sheets_by_game_session_uuid(
        db_session: Session, game_session_uuid: str
    ) -> Sequence[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(game_session_uuid=game_session_uuid)
        result = db_session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_character_sheet_by_user_uuid_and_game_session_uuid(
        db_session: Session, user_uuid: str, game_session_uuid: str
    ) -> Optional[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(
            user_uuid=user_uuid, game_session_uuid=game_session_uuid
        )
        result = db_session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def update_properties(db_session: Session, uuid: UUID, properties: Dict):
        stmt = (
            update(CharacterSheetDB)
            .where(CharacterSheetDB.uuid == uuid)
            .values(properties=properties)
            .execution_options(synchronize_session="fetch")
        )
        db_session.execute(stmt)
        db_session.commit()

    @staticmethod
    def get_characters_sheets_by_user_uuid(
        db_session: Session, user_uuid: str
    ) -> Sequence[CharacterSheetDB]:
        stmt = select(CharacterSheetDB).filter_by(user_uuid=user_uuid)
        result = db_session.execute(stmt)
        return result.scalars().all()


class RenownRepository:
    @staticmethod
    def get_all_renowns(db_session: Session) -> Sequence[RenownDB]:
        stmt = select(RenownDB)
        result = db_session.execute(
            stmt.order_by(RenownDB.level).options(joinedload(RenownDB.improvements))
        )
        return result.unique().scalars().all()


class ExperienceRepository:
    @staticmethod
    def get_all_experiences(db_session: Session) -> Sequence[ExperienceDB]:
        stmt = select(ExperienceDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class PhilosophyRepository:
    @staticmethod
    def get_all_philosophies(db_session: Session) -> Sequence[PhilosophyDB]:
        stmt = select(PhilosophyDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class TemperamentRepository:
    @staticmethod
    def get_all_temperaments(db_session: Session) -> Sequence[TemperamentDB]:
        stmt = select(TemperamentDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class DreamPhaseRepository:
    @staticmethod
    def get_all_dream_phases(db_session: Session) -> Sequence[DreamPhaseDB]:
        stmt = select(DreamPhaseDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class WeaknessRepository:
    @staticmethod
    def get_all_weaknesses(db_session: Session) -> Sequence[WeaknessDB]:
        stmt = select(WeaknessDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class SomnaAffinityRepository:
    @staticmethod
    def get_all_somna_affinities(db_session: Session) -> Sequence[SomnaAffinityDB]:
        stmt = select(SomnaAffinityDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class SkillRepository:
    @staticmethod
    def get_all_skills(db_session: Session) -> Sequence[SkillDB]:
        stmt = select(SkillDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class MartialRepository:
    @staticmethod
    def get_all_martials(db_session: Session) -> Sequence[MartialDB]:
        stmt = select(MartialDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class ManeuverRepository:
    @staticmethod
    def get_all_maneuvers(db_session: Session) -> Sequence[ManeuverDB]:
        stmt = select(ManeuverDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class SpellRepository:
    @staticmethod
    def get_all_spells(db_session: Session) -> Sequence[SpellDB]:
        stmt = select(SpellDB).options(joinedload(SpellDB.essence))
        result = db_session.execute(stmt)
        return result.unique().scalars().all()


class EssenceRepository:
    @staticmethod
    def get_all_essences(db_session: Session) -> Sequence[EssenceDB]:
        stmt = select(EssenceDB).options(joinedload(EssenceDB.spells))
        result = db_session.execute(stmt)
        essences = result.unique().scalars().all()
        for essence in essences:
            essence.spells.sort(key=lambda s: s.tier)
        return essences


class RecipeRepository:
    @staticmethod
    def get_all_recipes(db_session: Session) -> Sequence[RecipeDB]:
        stmt = select(RecipeDB)
        result = db_session.execute(stmt)
        return result.unique().scalars().all()


class ArmorRepository:
    @staticmethod
    def get_all_armors(db_session: Session) -> Sequence[ArmorDB]:
        stmt = select(ArmorDB).options(
            selectinload(ArmorDB.armors_properties_links).joinedload(
                ArmorPropertyLinkDB.property
            )
        )
        result = db_session.execute(stmt)
        return result.unique().scalars().all()


class WeaponRepository:
    @staticmethod
    def get_all_weapons(db_session: Session) -> Sequence[WeaponDB]:
        stmt = select(WeaponDB).options(
            selectinload(WeaponDB.weapons_properties_links).joinedload(
                WeaponPropertyLinkDB.property
            ),
            selectinload(WeaponDB.weapons_criticals_links).joinedload(
                WeaponCriticalLinkDB.critical
            ),
        )
        result = db_session.execute(stmt)
        return result.unique().scalars().all()


class ItemRepository:
    @staticmethod
    def get_all_items(db_session: Session) -> Sequence[ItemDB]:
        stmt = select(ItemDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class TotemRepository:
    @staticmethod
    def get_all_totems(db_session: Session) -> Sequence[TotemDB]:
        stmt = select(TotemDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class MantraRepository:
    @staticmethod
    def get_all_mantras(db_session: Session) -> Sequence[MantraDB]:
        stmt = select(MantraDB)
        result = db_session.execute(stmt)
        return result.scalars().all()


class BookRepository:
    @staticmethod
    def get_all_books(db_session: Session) -> Sequence[BookDB]:
        stmt = select(BookDB)
        result = db_session.execute(stmt)
        return result.scalars().all()
