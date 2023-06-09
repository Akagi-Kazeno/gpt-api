/*
 Navicat Premium Data Transfer

 Source Server         : gpt
 Source Server Type    : PostgreSQL
 Source Server Version : 150003 (150003)
 Source Host           : 127.0.0.1:5432
 Source Catalog        : gpt-api
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 150003 (150003)
 File Encoding         : 65001

 Date: 09/06/2023 17:30:36
*/


-- ----------------------------
-- Table structure for chat
-- ----------------------------
DROP TABLE IF EXISTS "public"."chat";
CREATE TABLE "public"."chat"
(
    "id"                varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "model"             varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "object"            varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "created"           int4                                        NOT NULL,
    "finish_reason"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "index"             int4                                        NOT NULL,
    "content"           text COLLATE "pg_catalog"."default"         NOT NULL,
    "role"              varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "completion_tokens" int4                                        NOT NULL,
    "prompt_tokens"     int4                                        NOT NULL,
    "total_tokens"      int4                                        NOT NULL,
    "session"           varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "create_time"       timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for completion
-- ----------------------------
DROP TABLE IF EXISTS "public"."completion";
CREATE TABLE "public"."completion"
(
    "id"                varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "model"             varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "object"            varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "created"           varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "finish_reason"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "index"             varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "logprobs"          text COLLATE "pg_catalog"."default",
    "text"              text COLLATE "pg_catalog"."default"         NOT NULL,
    "completion_tokens" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "prompt_tokens"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "total_tokens"      varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "session"           varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "create_time"       timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for gpt_image
-- ----------------------------
DROP TABLE IF EXISTS "public"."gpt_image";
CREATE TABLE "public"."gpt_image"
(
    "id"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "created"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "b64_image"   text COLLATE "pg_catalog"."default"         NOT NULL,
    "session"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "create_time" timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "public"."user";
CREATE TABLE "public"."user"
(
    "user_id"         varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "user_name"       varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "password"        varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "avatar"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "role"            varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "create_time"     timestamp(6)                                NOT NULL,
    "update_time"     timestamp(6),
    "last_login_time" timestamp(6),
    "last_login_ip"   varchar(255) COLLATE "pg_catalog"."default",
    "is_delete"       varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for user_chat
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_chat";
CREATE TABLE "public"."user_chat"
(
    "id"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "session"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "message"     text COLLATE "pg_catalog"."default"         NOT NULL,
    "create_time" timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for user_chat_completion
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_chat_completion";
CREATE TABLE "public"."user_chat_completion"
(
    "id"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "session"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "message"     text COLLATE "pg_catalog"."default"         NOT NULL,
    "create_time" timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for user_completion
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_completion";
CREATE TABLE "public"."user_completion"
(
    "id"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "session"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "prompt"      text COLLATE "pg_catalog"."default"         NOT NULL,
    "create_time" timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for user_gpt_image
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_gpt_image";
CREATE TABLE "public"."user_gpt_image"
(
    "id"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "session"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "description" text COLLATE "pg_catalog"."default"         NOT NULL,
    "create_time" timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for user_web_chat
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_web_chat";
CREATE TABLE "public"."user_web_chat"
(
    "id"          varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "message"     text COLLATE "pg_catalog"."default"         NOT NULL,
    "session"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "create_time" timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Table structure for web_chat_response
-- ----------------------------
DROP TABLE IF EXISTS "public"."web_chat_response";
CREATE TABLE "public"."web_chat_response"
(
    "web_chat_id"     varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "conversation_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "end_turn"        bool                                        NOT NULL,
    "finish_details"  varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "message"         text COLLATE "pg_catalog"."default"         NOT NULL,
    "model"           varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "parent_id"       varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "recipient"       varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "session"         varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
    "create_time"     timestamp(6)                                NOT NULL
)
;

-- ----------------------------
-- Primary Key structure for table chat
-- ----------------------------
ALTER TABLE "public"."chat"
    ADD CONSTRAINT "chat_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table completion
-- ----------------------------
ALTER TABLE "public"."completion"
    ADD CONSTRAINT "completion_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table gpt_image
-- ----------------------------
ALTER TABLE "public"."gpt_image"
    ADD CONSTRAINT "gpt_image_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user
-- ----------------------------
ALTER TABLE "public"."user"
    ADD CONSTRAINT "user_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table user_chat
-- ----------------------------
ALTER TABLE "public"."user_chat"
    ADD CONSTRAINT "user_chat_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_chat_completion
-- ----------------------------
ALTER TABLE "public"."user_chat_completion"
    ADD CONSTRAINT "user_chat_completion_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_completion
-- ----------------------------
ALTER TABLE "public"."user_completion"
    ADD CONSTRAINT "user_completion_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_gpt_image
-- ----------------------------
ALTER TABLE "public"."user_gpt_image"
    ADD CONSTRAINT "user_gpt_image_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_web_chat
-- ----------------------------
ALTER TABLE "public"."user_web_chat"
    ADD CONSTRAINT "user_web_chat_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table web_chat_response
-- ----------------------------
ALTER TABLE "public"."web_chat_response"
    ADD CONSTRAINT "web_chat_response_pkey" PRIMARY KEY ("web_chat_id");
