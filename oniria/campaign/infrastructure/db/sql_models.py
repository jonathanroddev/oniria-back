from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from oniria import Base


class Biography(Base):
    __tablename__ = "biographies"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class HeroicPath(Base):
    __tablename__ = "heroic_paths"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class Inventory(Base):
    __tablename__ = "inventories"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class CharacterSheet(Base):
    __tablename__ = "characters_sheets"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    biography_uuid = Column(
        UUID(as_uuid=True), ForeignKey("biographies.uuid"), nullable=False
    )
    heroic_path_uuid = Column(
        UUID(as_uuid=True), ForeignKey("heroic_paths.uuid"), nullable=False
    )
    inventory_uuid = Column(
        UUID(as_uuid=True), ForeignKey("inventories.uuid"), nullable=False
    )

    biography = relationship("Biography")
    heroic_path = relationship("HeroicPath")
    inventory = relationship("Inventory")


class Renown(Base):
    __tablename__ = "renown"
    name = Column(String(50), primary_key=True)
    level = Column(Integer, nullable=False)
    experience_uuid = Column(
        UUID(as_uuid=True), ForeignKey("experiences.uuid"), nullable=False
    )
    improvement_uuid = Column(
        UUID(as_uuid=True), ForeignKey("improvements.uuid"), nullable=False
    )

    experience = relationship("Experience")
    improvement = relationship("Improvement")


class CharacterRenown(Base):
    __tablename__ = "characters_renown"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    character_uuid = Column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), nullable=False
    )
    renown_name = Column(String(50), ForeignKey("renown.name"), nullable=False)
    is_current = Column(Boolean, nullable=False)

    character = relationship("CharacterSheet")
    renown = relationship("Renown")


class CharactersRenownHistory(Base):
    __tablename__ = "characters_renown_history"
    character_uuid = Column(
        UUID(as_uuid=True), ForeignKey("characters_sheets.uuid"), primary_key=True
    )
    character_renown_uuid = Column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), primary_key=True
    )


class Experience(Base):
    __tablename__ = "experiences"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    max = Column(Integer, nullable=False)


class Improvement(Base):
    __tablename__ = "improvements"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    max = Column(Integer, nullable=False)


class ExperienceAcquired(Base):
    __tablename__ = "experiences_acquired"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    experience_uuid = Column(
        UUID(as_uuid=True), ForeignKey("experiences.uuid"), nullable=False
    )
    character_renown_uuid = Column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), nullable=False
    )
    quantity = Column(Integer, nullable=False)


class ImprovementAcquired(Base):
    __tablename__ = "improvements_acquired"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    improvement_uuid = Column(
        UUID(as_uuid=True), ForeignKey("improvements.uuid"), nullable=False
    )
    character_renown_uuid = Column(
        UUID(as_uuid=True), ForeignKey("characters_renown.uuid"), nullable=False
    )
    quantity = Column(Integer, nullable=False)
