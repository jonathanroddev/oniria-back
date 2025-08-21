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
    "owner" UUID NOT NULL REFERENCES users(uuid),
    "name" VARCHAR(50) NOT NULL,
    "password" VARCHAR(250) NULL,
    "max_players" INTEGER NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
);

CREATE TABLE characters_sheets (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "user_uuid" UUID NOT NULL REFERENCES users(uuid),
    "game_session_uuid" UUID NULL REFERENCES games_sessions(uuid)

CREATE TABLE masters_workshops (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    "user_uuid" UUID NOT NULL REFERENCES users(uuid),
    "game_session_uuid" UUID NOT NULL REFERENCES games_sessions(uuid) UNIQUE,
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
    value INT NOT NULL,
    property_key VARCHAR(50)
);
