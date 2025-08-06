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

CREATE TABLE inventories (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE avatars (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE oneironauts (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
);

CREATE TABLE characters_sheets (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "user_uuid" UUID NOT NULL REFERENCES users(uuid),
    "game_session_uuid" UUID NULL REFERENCES games_sessions(uuid),
    "avatar_uuid" UUID NOT NULL REFERENCES avatars(uuid),
    "oneironaut_uuid" UUID NOT NULL REFERENCES oneironauts(uuid),
    "inventory_uuid" UUID NOT NULL REFERENCES inventories(uuid)
);

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

CREATE TABLE renown (
    "name" VARCHAR(50) PRIMARY KEY NOT NULL,
    "level" INTEGER NOT NULL
);

CREATE TABLE experiences (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "max" INTEGER NOT NULL,
    "desc" VARCHAR(50) NOT NULL,
    "renown_name" VARCHAR(50) NOT NULL REFERENCES renown(name)
);

CREATE TABLE improvements (
    "uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "max" INTEGER NOT NULL,
    "desc" VARCHAR(50) NOT NULL,
    "renown_name" VARCHAR(50) NOT NULL REFERENCES renown(name)
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
