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

CREATE TABLE renown (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE experiences (
    "key" VARCHAR(50) PRIMARY KEY NOT NULL
);

CREATE TABLE improvements (
    "key" VARCHAR(100) PRIMARY KEY NOT NULL,
    "max" INTEGER NOT NULL,
    "renown_key" VARCHAR(50) NOT NULL REFERENCES renown(key)
);
