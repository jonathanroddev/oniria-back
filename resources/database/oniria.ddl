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