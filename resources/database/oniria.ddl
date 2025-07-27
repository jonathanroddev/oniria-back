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

CREATE TABLE players_types (
    "name" VARCHAR(50) PRIMARY KEY,
	CONSTRAINT check_empty_name CHECK ((TRIM(BOTH FROM name) <> ''::text))
);

CREATE TABLE user_status (
    "name" VARCHAR(50) PRIMARY KEY,
	CONSTRAINT check_empty_name CHECK ((TRIM(BOTH FROM name) <> ''::text))
);

CREATE TABLE game_session (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE inventories (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE biographies (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE heroic_paths (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE characters_sheets (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "biography_uuid" UUID NOT NULL REFERENCES biographies(uuid),
    "heroic_path_uuid" UUID NOT NULL REFERENCES heroic_paths(uuid),
    "inventory_uuid" UUID NOT NULL REFERENCES inventories(uuid)
);

CREATE TABLE users (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "external_uuid" VARCHAR(50) NOT NULL,
    "player_type" VARCHAR(50) NOT NULL REFERENCES players_types(name),
    "user_status" VARCHAR(50) NOT NULL REFERENCES user_status(name),
    "plan" VARCHAR(50) NOT NULL REFERENCES plans(name),
    "game_session_uuid" UUID NOT NULL REFERENCES game_session(uuid),
    "character_sheet_uuid" UUID NOT NULL REFERENCES characters_sheets(uuid)
);

CREATE TABLE permissions_plans_player_type (
    "permission_uuid" UUID NOT NULL REFERENCES permissions(uuid),
    "plan" VARCHAR(50) NOT NULL REFERENCES plans(name),
    "player_type" VARCHAR(50) NOT NULL REFERENCES players_types(name),
    PRIMARY KEY (permission_uuid, plan, player_type)
);

CREATE TABLE experiences (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "max" INTEGER NOT NULL
);

CREATE TABLE improvements (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "max" INTEGER NOT NULL
);

CREATE TABLE renown (
    "name" VARCHAR(50) PRIMARY KEY NOT NULL,
    "level" INTEGER NOT NULL,
    "experience_uuid" UUID NOT NULL REFERENCES experiences(uuid),
    "improvement_uuid" UUID NOT NULL REFERENCES improvements(uuid)
);

CREATE TABLE characters_renown (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "character_uuid" UUID NOT NULL REFERENCES characters_sheets(uuid),
    "renown_name" VARCHAR(50) NOT NULL REFERENCES renown(name),
    "is_current" BOOLEAN NOT NULL
);

CREATE TABLE characters_renown_history (
    "character_uuid" UUID NOT NULL REFERENCES characters_sheets(uuid),
    "character_renown_uuid" UUID NOT NULL REFERENCES characters_renown(uuid),
    PRIMARY KEY (character_uuid, character_renown_uuid)
);

CREATE TABLE experiences_acquired (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "experience_uuid" UUID NOT NULL REFERENCES experiences(uuid),
    "character_renown_uuid" UUID NOT NULL REFERENCES characters_renown(uuid),
    "quantity" INTEGER NOT NULL
);

CREATE TABLE improvements_acquired (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "improvement_uuid" UUID NOT NULL REFERENCES improvements(uuid),
    "character_renown_uuid" UUID NOT NULL REFERENCES characters_renown(uuid),
    "quantity" INTEGER NOT NULL
);
