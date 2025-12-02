CREATE TABLE resources (
	"name" VARCHAR(50) PRIMARY KEY,
	CONSTRAINT check_empty_name CHECK ((TRIM(BOTH FROM name) <> ''::text))
);

CREATE TABLE operations (
	"name" VARCHAR(50) PRIMARY KEY,
	CONSTRAINT check_empty_name CHECK ((TRIM(BOTH FROM name) <> ''::text))
);

CREATE TABLE permissions (
	"uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "resource" VARCHAR(50) NOT NULL REFERENCES resources (name),
    "operation" VARCHAR(50) NOT NULL REFERENCES operations (name),
	UNIQUE ("resource", "operation")
);

CREATE TABLE plans (
    "name" VARCHAR(50) PRIMARY KEY,
	CONSTRAINT check_empty_name CHECK ((TRIM(BOTH FROM name) <> ''::text))
);

CREATE TABLE user_status (
    "name" VARCHAR(50) PRIMARY KEY,
	CONSTRAINT check_empty_name CHECK ((TRIM(BOTH FROM name) <> ''::text))
);

CREATE TABLE games_sessions (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "name" VARCHAR(50) NOT NULL,
    "password" VARCHAR(250) NULL,
    "max_players" INTEGER NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    "master_workshop_uuid" UUID NOT NULL REFERENCES masters_workshops(uuid) UNIQUE,
);

CREATE TABLE characters_sheets (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "user_uuid" UUID NOT NULL REFERENCES users(uuid),
    "game_session_uuid" UUID NULL REFERENCES games_sessions(uuid),
    "properties" JSONB,

CREATE TABLE masters_workshops (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "owner" UUID NOT NULL REFERENCES users(uuid),
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    "properties" JSONB,
);

CREATE TABLE users (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "external_uuid" VARCHAR(50) NOT NULL,
    "dreamer_tag" VARCHAR(50) NOT NULL,
    "user_status" VARCHAR(50) NOT NULL REFERENCES user_status(name),
    "plan" VARCHAR(50) NOT NULL REFERENCES plans(name),
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    "updated_at" TIMESTAMP NOT NULL
);

CREATE TABLE permissions_plans (
    "permission_uuid" UUID NOT NULL REFERENCES permissions(uuid),
    "plan" VARCHAR(50) NOT NULL REFERENCES plans(name),
    PRIMARY KEY (permission_uuid, plan)
);

CREATE TABLE translations (
    table_name VARCHAR(50) NOT NULL,
    element_key VARCHAR(100) NOT NULL,
    property VARCHAR(50) NOT NULL,
    lang VARCHAR(5) NOT NULL,  -- ISO 639-1
    display_text TEXT NOT NULL,
    PRIMARY KEY (table_name, element_key, property, lang)
);

-- Characters Sheets related tables
CREATE TABLE renown (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL,
    "level" INTEGER NOT NULL,
    "lucidity_points" INTEGER NOT NULL,
    "max_magic_level" INTEGER NOT NULL,
    "karma_points" INTEGER NOT NULL,
    "totems_base" INTEGER NOT NULL,
    "mantras_base" INTEGER NOT NULL,
    "recipes_base" INTEGER NOT NULL,
    "books_base" INTEGER NOT NULL,
    "max_improvements" INTEGER NOT NULL,
    "max_experiences" INTEGER NOT NULL,
);

CREATE TABLE experiences (
    "key" VARCHAR(100) PRIMARY KEY NOT NULL
);

CREATE TABLE improvements (
    key VARCHAR(100) NOT NULL,
    "max" INT NOT NULL,
    renown_key VARCHAR(50) NOT NULL,
    PRIMARY KEY (key, renown_key)
);

CREATE TABLE philosophies (
    "key" VARCHAR(100) PRIMARY KEY NOT NULL
);

CREATE TABLE temperaments (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE dream_phases (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE weaknesses (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE somna_affinities (
    "key" VARCHAR(100) PRIMARY KEY NOT NULL
);

CREATE TABLE skills (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE martials (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TYPE maneuver_type AS ENUM ('common', 'advanced');

CREATE TABLE maneuvers (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL,
    "type" maneuver_type NOT NULL,
    "requires_magic" BOOLEAN DEFAULT FALSE
);

CREATE TABLE essences (
    key VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE spells (
    key VARCHAR(50) PRIMARY KEY NOT NULL,
    essence_key VARCHAR(50) NOT NULL REFERENCES essences(key),
    tier INT NOT NULL
);

CREATE TYPE recipe_type AS ENUM ('brew', 'poison');

CREATE TABLE recipes (
    key VARCHAR(50) PRIMARY KEY NOT NULL,
    type recipe_type NOT NULL
);

CREATE TYPE armor_type AS ENUM ('light', 'medium', 'heavy');

CREATE TABLE armors (
    key VARCHAR(50) PRIMARY KEY,
    type armor_type NOT NULL,
    rarity INTEGER NOT NULL,
    value INTEGER NOT NULL,
    defense INTEGER NOT NULL
);

CREATE TABLE armors_properties (
    key VARCHAR(50) PRIMARY KEY
);

CREATE TABLE armors_properties_links (
    armor_key VARCHAR(50) NOT NULL,
    property_key VARCHAR(50) NOT NULL,
    PRIMARY KEY (armor_key, property_key)
);

CREATE TYPE weapon_type AS ENUM ('melee_1_hand', 'melee_2_hands', 'ranged', 'arcane');

CREATE TABLE weapons (
    key VARCHAR(50) PRIMARY KEY,
    type weapon_type NOT NULL,
    rarity INT NOT NULL,
    range INT NOT NULL,
    value INT NOT NULL,
    attack INT NOT NULL,
    defense INT NOT NULL
);

CREATE TABLE weapons_criticals (
    key VARCHAR(50) PRIMARY KEY
);

CREATE TABLE weapons_criticals_links (
    weapon_key VARCHAR(50) NOT NULL,
    critical_key VARCHAR(50) NOT NULL,
    PRIMARY KEY (weapon_key, critical_key),
    FOREIGN KEY (weapon_key) REFERENCES weapons(key),
    FOREIGN KEY (critical_key) REFERENCES weapons_criticals(key)
);

CREATE TABLE weapons_properties (
    key VARCHAR(50) PRIMARY KEY,
    has_modifier BOOLEAN DEFAULT FALSE
);

CREATE TABLE weapons_properties_links (
    weapon_key VARCHAR(50) NOT NULL,
    property_key VARCHAR(50) NOT NULL,
    modifier INT,
    PRIMARY KEY (weapon_key, property_key),
    FOREIGN KEY (weapon_key) REFERENCES weapons(key),
    FOREIGN KEY (property_key) REFERENCES weapons_properties(key)
);

CREATE TABLE items (
    key VARCHAR(50) PRIMARY KEY,
    rarity INT NOT NULL,
    range INT,
    value INT NOT NULL
);

CREATE TYPE totem_type AS ENUM ('common', 'advanced');

CREATE TABLE totems (
    key VARCHAR(50) PRIMARY KEY,
    type totem_type NOT NULL,
    needs_awake BOOLEAN DEFAULT FALSE,
    needs_sleep BOOLEAN DEFAULT FALSE,
    lucidity_points VARCHAR(5) NOT NULL
);

CREATE TABLE mantras (
    key VARCHAR(50) PRIMARY KEY
);

CREATE TABLE books (
    key VARCHAR(50) PRIMARY KEY
);

-- Masters Workshops related tables
CREATE TYPE objective_type AS ENUM ('motive', 'action', 'target', 'need', 'status');
CREATE TABLE objectives (
    key VARCHAR(50) PRIMARY KEY,
    type objective_type NOT NULL,
    dice VARCHAR(10) NOT NULL,
    roll INT NOT NULL,

    -- To ensure uniqueness of the roll within the type
    CONSTRAINT uq_objective_type_roll UNIQUE (type, roll)
);

CREATE TYPE commission_type AS ENUM ('patron', 'condition');
CREATE TABLE commissions (
    key VARCHAR(50) PRIMARY KEY,
    type objective_type NOT NULL,
    dice VARCHAR(10) NOT NULL,
    roll INT NOT NULL,

    -- To ensure uniqueness of the roll within the type
    CONSTRAINT uq_commission_type_roll UNIQUE (type, roll)
);

CREATE TABLE factions (
    roll INT PRIMARY KEY,
    dice VARCHAR(10) NOT NULL,
    "type" VARCHAR(50) NOT NULL UNIQUE,
    ideology VARCHAR(50) NOT NULL UNIQUE,
    resource VARCHAR(50) NOT NULL UNIQUE,
    "limit" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TYPE npc_trait_type AS ENUM ('appearance', 'skin', 'facial', 'hair', 'attire', 'voice', 'attitude', 'defect', 'profession', 'problem');
CREATE TABLE npc_traits (
    key VARCHAR(50) PRIMARY KEY,
    type npc_trait_type NOT NULL,
    dice VARCHAR(10) NOT NULL,
    roll INT NOT NULL,

    -- To ensure uniqueness of the roll within the type
    CONSTRAINT uq_npc_trait_type_roll UNIQUE (type, roll)
);

CREATE TABLE npc_names (
    roll INT PRIMARY KEY,
    dice VARCHAR(10) NOT NULL DEFAULT '1d100',
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL
);

CREATE TYPE scenario_type AS ENUM ('location', 'concept');
CREATE TABLE scenarios (
    key VARCHAR(50) PRIMARY KEY,
    roll INT NOT NULL,
    dice VARCHAR(10) NOT NULL DEFAULT '1d20',
    type scenario_type NOT NULL,

    -- To ensure uniqueness of the roll within the type
    CONSTRAINT uq_scenario_type_roll UNIQUE (type, roll)
);

CREATE TYPE dungeon_aspect_type AS ENUM ('ascendancy', 'usage', 'content', 'threat', 'value', 'context');
CREATE TABLE dungeon_aspects (
    key VARCHAR(50) PRIMARY KEY,
    roll INT NOT NULL,
    dice VARCHAR(10) NOT NULL DEFAULT '1d10',
    type dungeon_aspect_type NOT NULL,

    -- To ensure uniqueness of the roll within the type
    CONSTRAINT uq_aspect_type_roll UNIQUE (type, roll)
);

CREATE TYPE conflict_entity_type AS ENUM ('entity1', 'entity2');
CREATE TABLE conflict_entities (
    roll INT NOT NULL,
    dice VARCHAR(10) NOT NULL DEFAULT '1d20',
    type conflict_entity_type NOT NULL,
    key VARCHAR(50) PRIMARY KEY,

    CONSTRAINT uq_roll_entity_type UNIQUE (roll, type)
);

CREATE TABLE random_events (
    key VARCHAR(50) NOT NULL,
    roll INT PRIMARY KEY,
    dice VARCHAR(10) NOT NULL DEFAULT '1d20',

    CONSTRAINT uq_event_roll UNIQUE (key)
);

CREATE TYPE tone_modifier_type AS ENUM ('fear', 'hope');
CREATE TABLE tone_modifiers (
    key VARCHAR(50) PRIMARY KEY,
    roll INT NOT NULL,
    dice VARCHAR(10) NOT NULL DEFAULT '1d10',
    type tone_modifier_type NOT NULL,

    CONSTRAINT uq_modifier_type_roll UNIQUE (type, roll)
);

CREATE TYPE reward_type AS ENUM ('object_type', 'origin', 'creation', 'effect', 'side_effect');
CREATE TABLE rewards (
    key VARCHAR(100) PRIMARY KEY,
    type reward_type NOT NULL,
    dice VARCHAR(10) NOT NULL,
    roll INT NOT NULL,

    CONSTRAINT uq_type_roll UNIQUE (type, roll)
);

CREATE TABLE enemies (
    key VARCHAR(50) PRIMARY KEY,

    -- Threshold (Umbral)
    threshold_min INT,
    threshold_max INT,

    -- Danger (Peligro)
    danger_min INT,
    danger_max INT,

    -- Endurance (Aguante)
    endurance_min INT,
    endurance_max INT,

    -- Stamina (Estamina)
    stamina_min INT,
    stamina_max INT,

    -- Weakness (Debilidades)
    weakness_min INT,
    weakness_max INT,

    -- Strength (Fortalezas) - NUEVO: 0-1
    strength_min INT,
    strength_max INT,

    -- Special (Special)
    special_min INT,
    special_max INT
);

CREATE TABLE enemies_subtypes (
    key VARCHAR(50) PRIMARY KEY,
    type_key VARCHAR(50) NOT NULL,

    FOREIGN KEY (type_key) REFERENCES enemies(key)
);